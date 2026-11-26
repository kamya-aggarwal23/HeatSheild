
from pathlib import Path
import calendar

import numpy as np
import xarray as xr


# ==========================================
# CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

START_YEAR = 2005
END_YEAR = 2025

EXPECTED_LAT = [35.8, 35.7, 35.6]
EXPECTED_LON = [139.6, 139.7, 139.8]


# ==========================================
# VALIDATE ONE MONTH
# ==========================================

def validate_file(file_path, year, month):

    errors = []

    days = calendar.monthrange(year, month)[1]
    expected_hours = days * 24

    try:
        with xr.open_dataset(file_path, engine="netcdf4") as ds:

            if "t2m" not in ds:
                errors.append("Missing temperature variable")
                return errors

            if "valid_time" not in ds.coords:
                errors.append("Missing time coordinate")
                return errors

            timestamps = ds["valid_time"].values

            # Record count
            if len(timestamps) != expected_hours:
                errors.append("Incorrect hourly record count")

            # Exact date boundaries
            expected_start = np.datetime64(
                f"{year}-{month:02d}-01T00:00"
            )

            if month == 12:
                next_month = np.datetime64(
                    f"{year + 1}-01-01T00:00"
                )
            else:
                next_month = np.datetime64(
                    f"{year}-{month + 1:02d}-01T00:00"
                )

            expected_end = next_month - np.timedelta64(1, "h")

            if timestamps[0] != expected_start:
                errors.append("Incorrect first timestamp")

            if timestamps[-1] != expected_end:
                errors.append("Incorrect last timestamp")

            # Duplicate timestamps
            if len(np.unique(timestamps)) != len(timestamps):
                errors.append("Duplicate timestamps")

            # Hourly continuity
            if not np.all(
                np.diff(timestamps) == np.timedelta64(1, "h")
            ):
                errors.append("Missing or irregular hourly timestamps")

            # Missing temperature values
            if not np.isfinite(ds["t2m"].values).all():
                errors.append("Missing or invalid temperature values")

            # Geographic coordinates
            if not np.allclose(ds.latitude.values, EXPECTED_LAT):
                errors.append("Incorrect latitude coordinates")

            if not np.allclose(ds.longitude.values, EXPECTED_LON):
                errors.append("Incorrect longitude coordinates")

            # Temperature units
            if ds["t2m"].attrs.get("units") != "K":
                errors.append("Unexpected temperature units")

    except Exception as error:
        errors.append(f"File reading error: {error}")

    return errors


# ==========================================
# VALIDATE ALL MONTHS
# ==========================================

def main():

    passed = 0
    failed = 0
    missing = []

    print("\nTOKYO DATASET VALIDATION")
    print("========================")

    for year in range(START_YEAR, END_YEAR + 1):

        for month in range(1, 13):

            filename = f"tokyo_hourly_{year}_{month:02d}.nc"
            file_path = RAW_DIR / filename

            if not file_path.exists():
                print(f"MISSING: {filename}")
                missing.append(filename)
                failed += 1
                continue

            errors = validate_file(file_path, year, month)

            if errors:
                print(f"FAILED: {filename}")
                for error in errors:
                    print("  -", error)
                failed += 1
            else:
                print(f"PASSED: {filename}")
                passed += 1

    print("\n========== FINAL REPORT ==========")
    print("Passed:", passed)
    print("Failed:", failed)
    print("Missing files:", len(missing))
    print("Total expected:", 252)

    if failed == 0:
        print("\nALL MONTHLY FILES PASSED VALIDATION.")
    else:
        print("\nCHECK FAILED FILES BEFORE PROCESSING.")


if __name__ == "__main__":
    main()
