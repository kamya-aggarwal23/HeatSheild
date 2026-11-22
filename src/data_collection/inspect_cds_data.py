
import xarray as xr
import pandas as pd

file_path = "data/raw/delhi_test_2005-01-01.nc"

# Delhi reference coordinates
city_lat = 28.58
city_lon = 77.20

ds = xr.open_dataset(file_path)

# Select the nearest grid point
point = ds.sel(
    latitude=city_lat,
    longitude=city_lon,
    method="nearest"
)

# Extract temperature and convert Kelvin to Celsius
temperature = point["t2m"] - 273.15

# Convert to a pandas DataFrame
df = temperature.to_dataframe(name="temperature_c").reset_index()

print("\n--- SELECTED GRID POINT ---")
print("Latitude:", float(point.latitude.values))
print("Longitude:", float(point.longitude.values))

print("\n--- HOURLY TEMPERATURES ---")
print(df[["valid_time", "temperature_c"]].to_string(index=False))

print("\n--- VALIDATION ---")
print("Number of hourly readings:", len(df))
print("Missing values:", df["temperature_c"].isna().sum())
print("Daily maximum:", round(df["temperature_c"].max(), 2), "°C")

ds.close()
