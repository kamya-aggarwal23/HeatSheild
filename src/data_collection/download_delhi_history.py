
import calendar
import time
from pathlib import Path

import cdsapi
import numpy as np
import xarray as xr


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

START_YEAR = 2006
END_YEAR = 2025

DATASET = "reanalysis-era5-land"

# Delhi bounding box:
# North, West, South, East
AREA = [28.7, 77.1, 28.5, 77.3]

VARIABLE = ["2m_temperature"]

HOURS = [
    f"{hour:02d}:00"
    for hour in range(24)
]

MAX_RETRIES = 3


# --------------------------------------------------
# 2. VALIDATE A DOWNLOADED NETCDF FILE
# --------------------------------------------------

def validate_file(file_path, expected_hours):

    try:
        with xr.open_dataset(
            file_path,
            engine="netcdf4"
        ) as ds:

            # Check temperature variable
            if "t2m" not in ds:
                return False

            # Check time coordinate
            if "valid_time" not in ds.coords:
                return False

            timestamps = ds["valid_time"].values

            # Check expected number of hourly records
            if len(timestamps) != expected_hours:
                return False

            # Check hourly continuity
            differences = np.diff(timestamps)

            if not np.all(
                differences == np.timedelta64(1, "h")
            ):
                return False

            # Check for missing temperature values
            missing_values = int(
                ds["t2m"].isnull().sum().item()
            )

            if missing_values > 0:
                return False

            # Check that spatial data exists
            if (
                ds["t2m"].sizes.get("latitude", 0) == 0
                or ds["t2m"].sizes.get("longitude", 0) == 0
            ):
                return False

        return True

    except Exception:
        return False


# --------------------------------------------------
# 3. DOWNLOAD ONE MONTH
# --------------------------------------------------

def download_month(client, year, month):

    month_name = f"{month:02d}"

    file_name = (
        f"delhi_hourly_{year}_{month_name}.nc"
    )

    output_path = RAW_DATA_DIR / file_name

    # Temporary file: only becomes final after validation
    temp_path = RAW_DATA_DIR / (
        f"delhi_hourly_{year}_{month_name}.tmp.nc"
    )

    number_of_days = calendar.monthrange(
        year, month
    )[1]

    expected_hours = number_of_days * 24

    # ----------------------------------------------
    # Check whether a valid file already exists
    # ----------------------------------------------

    if output_path.exists():

        if validate_file(output_path, expected_hours):

            print(f"SKIP: {file_name} already valid")
            return True

        print(f"INVALID: {file_name}. Downloading again.")

        output_path.unlink()

    # ----------------------------------------------
    # Prepare CDS request
    # ----------------------------------------------

    request = {
        "variable": VARIABLE,
        "year": str(year),
        "month": month_name,
        "day": [
            f"{day:02d}"
            for day in range(1, number_of_days + 1)
        ],
        "time": HOURS,
        "data_format": "netcdf",
        "download_format": "unarchived",
        "area": AREA
    }

    # ----------------------------------------------
    # Retry download if something fails
    # ----------------------------------------------

    for attempt in range(1, MAX_RETRIES + 1):

        try:

            print(
                f"\nDownloading Delhi {year}-{month_name}"
            )

            print(
                f"Attempt {attempt}/{MAX_RETRIES}"
            )

            # Remove incomplete temporary file
            if temp_path.exists():
                temp_path.unlink()

            client.retrieve(
                DATASET,
                request
            ).download(str(temp_path))

            # Validate before saving permanently
            if not validate_file(
                temp_path,
                expected_hours
            ):

                raise ValueError(
                    "Downloaded file failed validation."
                )

            # Move validated file into final location
            temp_path.replace(output_path)

            print(f"SUCCESS: {file_name}")

            return True

        except Exception as error:

            print(f"FAILED: {error}")

            if temp_path.exists():
                temp_path.unlink()

            if attempt < MAX_RETRIES:

                wait_time = 2 ** attempt

                print(
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

    print(f"GAVE UP: {file_name}")

    return False


# --------------------------------------------------
# 4. MAIN DOWNLOAD PROCESS
# --------------------------------------------------

def main():

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    client = cdsapi.Client()

    successful = 0
    failed = []

    total_months = (
        (END_YEAR - START_YEAR + 1) * 12
    )

    print("\nStarting Delhi historical data download")
    print(f"Years: {START_YEAR}-{END_YEAR}")
    print(f"Total monthly files: {total_months}")

    for year in range(START_YEAR, END_YEAR + 1):

        print(f"\n========== YEAR {year} ==========")

        for month in range(1, 13):

            result = download_month(
                client,
                year,
                month
            )

            if result:
                successful += 1

            else:
                failed.append(
                    f"{year}-{month:02d}"
                )

    # ----------------------------------------------
    # Final report
    # ----------------------------------------------

    print("\n========== DOWNLOAD SUMMARY ==========")

    print("Successful/skipped files:", successful)
    print("Failed months:", len(failed))

    if failed:

        print("\nMonths needing attention:")

        for month in failed:
            print(month)

    else:

        print(
            "\nAll Delhi monthly files are available "
            "and passed validation."
        )


if __name__ == "__main__":
    main()
