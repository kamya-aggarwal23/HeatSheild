
from pathlib import Path
import calendar
import xarray as xr
import pandas as pd

DATA_DIR = Path("data/raw")
YEAR = 2005

for city in ["delhi", "tokyo"]:
    print(f"\n{'=' * 45}")
    print(f"VALIDATING {city.upper()} — {YEAR}")
    print("=" * 45)

    all_passed = True

    for month in range(1, 13):
        filename = DATA_DIR / f"{city}_hourly_{YEAR}_{month:02d}.nc"

        with xr.open_dataset(filename) as ds:
            times = pd.DatetimeIndex(ds["valid_time"].values)
            temperature = ds["t2m"]

            expected_hours = (
                calendar.monthrange(YEAR, month)[1] * 24
            )

            differences = times.to_series().diff().dropna()

            checks = {
                "correct_hours": len(times) == expected_hours,
                "continuous": differences.eq(
                    pd.Timedelta(hours=1)
                ).all(),
                "no_duplicates": times.duplicated().sum() == 0,
                "no_missing_values": (
                    int(temperature.isnull().sum().values) == 0
                ),
                "valid_grid": (
                    len(ds.latitude) > 0 and len(ds.longitude) > 0
                )
            }

            passed = all(checks.values())
            all_passed = all_passed and passed

            print(
                f"{YEAR}-{month:02d}: "
                f"{'PASS' if passed else 'FAIL'} | "
                f"{len(times)} hours | "
                f"Grid: {len(ds.latitude)}x{len(ds.longitude)}"
            )

    print("\nFINAL RESULT:", "PASS" if all_passed else "CHECK REQUIRED")
