
from pathlib import Path
import xarray as xr
import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

YEAR = 2005
CITY_LAT = 28.58
CITY_LON = 77.20
TIMEZONE = "Asia/Kolkata"

# Monthly files plus the December 2004 boundary file
files = [
    RAW_DIR / "delhi_boundary_2004-12-31.nc"
]

files += sorted(
    RAW_DIR.glob(f"delhi_hourly_{YEAR}_*.nc")
)

if len(files) != 13:
    raise ValueError(f"Expected 13 files, found {len(files)}")

print("Combining 12 monthly files and boundary file...")

datasets = [xr.open_dataset(file) for file in files]

try:
    ds = xr.concat(datasets, dim="valid_time").sortby("valid_time")

    # Select nearest Delhi grid point
    point = ds.sel(
        latitude=CITY_LAT,
        longitude=CITY_LON,
        method="nearest"
    )

    print(
        "Selected grid point:",
        float(point.latitude.values),
        float(point.longitude.values)
    )

    # Kelvin to Celsius
    temperature = point["t2m"] - 273.15

    df = temperature.to_dataframe(
        name="temperature_c"
    ).reset_index()

    # Convert UTC to Delhi local time
    df["valid_time"] = (
        pd.to_datetime(df["valid_time"])
        .dt.tz_localize("UTC")
        .dt.tz_convert(TIMEZONE)
    )

    df["date"] = df["valid_time"].dt.date

    # Keep only 2005 local calendar dates
    start_date = pd.Timestamp("2005-01-01").date()
    end_date = pd.Timestamp("2005-12-31").date()

    df = df[
        (df["date"] >= start_date) &
        (df["date"] <= end_date)
    ].copy()

    # Check hourly coverage for every local date
    daily_counts = df.groupby("date").agg(
        hourly_records=("temperature_c", "size"),
        missing_values=("temperature_c", lambda x: x.isna().sum())
    )

    incomplete = daily_counts[
        (daily_counts["hourly_records"] != 24) |
        (daily_counts["missing_values"] != 0)
    ]

    if not incomplete.empty:
        print("\nIncomplete local dates:")
        print(incomplete)
        raise ValueError("Some local days do not have 24 valid readings.")

    # Calculate daily Tmax
    daily = (
        df.groupby("date")["temperature_c"]
        .max()
        .reset_index()
        .rename(columns={"temperature_c": "tmax"})
    )

    daily["tmax"] = daily["tmax"].round(2)

    # Final checks
    expected_dates = pd.date_range(
        "2005-01-01", "2005-12-31", freq="D"
    ).date

    if len(daily) != 365:
        raise ValueError(f"Expected 365 days, got {len(daily)}")

    if list(daily["date"]) != list(expected_dates):
        raise ValueError("Date sequence is incomplete or incorrect.")

    if daily["tmax"].isna().any():
        raise ValueError("Missing daily Tmax values found.")

    # Save
    output_file = PROCESSED_DIR / "delhi_daily_2005.csv"
    daily.to_csv(output_file, index=False)

    print("\n--- FINAL VALIDATION ---")
    print("Daily records:", len(daily))
    print("Missing values:", daily["tmax"].isna().sum())
    print("Duplicate dates:", daily["date"].duplicated().sum())
    print("First date:", daily["date"].min())
    print("Last date:", daily["date"].max())
    print("Minimum Tmax:", daily["tmax"].min())
    print("Maximum Tmax:", daily["tmax"].max())

    print("\nFirst five rows:")
    print(daily.head())

    print("\nSaved:", output_file)
    print("Processing completed successfully!")

finally:
    for dataset in datasets:
        dataset.close()
