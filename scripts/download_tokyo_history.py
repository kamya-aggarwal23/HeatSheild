
from pathlib import Path
import calendar
import time

import cdsapi
import numpy as np
import xarray as xr


# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

START_YEAR = 2005
END_YEAR = 2025

DATASET = "reanalysis-era5-land"
VARIABLE = ["2m_temperature"]

# Tokyo bounding box: North, West, South, East
AREA = [35.8, 139.6, 35.6, 139.8]

HOURS = [f"{hour:02d}:00" for hour in range(24)]

MAX_RETRIES = 3


# ==========================================
# 2. VALIDATE DOWNLOADED NETCDF FILE
# ==========================================

def validate_file(file_path, expected_hours):

    try:
        with xr.open_dataset(file_path, engine="netcdf4") as ds:

            if "t2m" not in ds:
                return False

            if "valid_time" not in ds.coords:
                return False

            timestamps = ds["valid_time"].values

            if len(timestamps) != expected_hours:
                return False

            differences = np.diff(timestamps)

            if not np.all(
                differences == np.timedelta64(1, "h")
            ):
                return False

            if bool(ds["t2m"].isnull().any().item()):
                return False

            if (
                ds["t2m"].sizes.get("latitude", 0) == 0
                or ds["t2m"].sizes.get("longitude", 0) == 0
            ):
                return False

        return True

    except Exception as error:
        print("Validation error:", error)
        return False


# ==========================================
# 3. DOWNLOAD ONE MONTH
# ==========================================

def download_month(client, year, month):

    month_name = f"{month:02d}"

    file_name = f"tokyo_hourly_{year}_{month_name}.nc"

    output_path = RAW_DATA_DIR / file_name
    temp_path = RAW_DATA_DIR / f"temp_{file_name}"

    number_of_days = calendar.monthrange(year, month)[1]
    expected_hours = number_of_days * 24

    # Skip an existing valid file
    if output_path.exists():

        if validate_file(output_path, expected_hours):
            print("Already downloaded and valid:", file_name)
            return True

        print("Existing file is invalid. Re-downloading.")

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

    # Retry failed downloads
    for attempt in range(1, MAX_RETRIES + 1):

        try:
            print(f"\nDownloading Tokyo {year}-{month_name}")
            print(f"Attempt {attempt}/{MAX_RETRIES}")

            if temp_path.exists():
                temp_path.unlink()

            client.retrieve(
                DATASET,
                request
            ).download(str(temp_path))

            if not validate_file(temp_path, expected_hours):
                raise ValueError("Downloaded file failed validation.")

            temp_path.replace(output_path)

            print("SUCCESS:", file_name)
            return True

        except Exception as error:

            print("Download failed:", error)

            if temp_path.exists():
                temp_path.unlink()

            if attempt < MAX_RETRIES:
                wait_time = 2 ** attempt
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

    print("FAILED:", file_name)
    return False


# ==========================================
# 4. MAIN PROCESS — JANUARY TEST ONLY
# ==========================================

def main():

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    client = cdsapi.Client()

    successful = 0
    failed = []

    total_months = 20 * 12

    print("Starting Tokyo historical collection")
    print("Period: 2006–2025")
    print("Monthly files:", total_months)

    for year in range(2006, 2026):

        print(f"\n========== YEAR {year} ==========")

        for month in range(1, 13):

            result = download_month(client, year, month)

            if result:
                successful += 1
            else:
                failed.append(f"{year}-{month:02d}")

    print("\n========== FINAL SUMMARY ==========")
    print("Successful or skipped:", successful)
    print("Failed:", len(failed))
    print("Failed months:", failed)


if __name__ == "__main__":
    main()
