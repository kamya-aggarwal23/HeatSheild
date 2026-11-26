
from pathlib import Path
import xarray as xr

# Locate NetCDF files in our raw data folder
raw_folder = Path("data/raw")
nc_files = list(raw_folder.glob("*.nc"))

# Ensure exactly one file is found
if len(nc_files) != 1:
    raise ValueError(f"Expected one NetCDF file, found {len(nc_files)}")

file_path = nc_files[0]

print("Opening:", file_path.name)

# Open the weather dataset
ds = xr.open_dataset(file_path)

# Display dataset information
print("\n--- DATASET INFORMATION ---")
print(ds)

print("\n--- DIMENSIONS ---")
print(ds.dims)

print("\n--- COORDINATES ---")
print(ds.coords)

print("\n--- DATA VARIABLES ---")
print(ds.data_vars)

print("\n--- GLOBAL ATTRIBUTES ---")
print(ds.attrs)


# Inspect temperature variable metadata
print("\n--- TEMPERATURE METADATA ---")
print(ds["t2m"].attrs)

# Print the first five hourly temperatures
print("\n--- FIRST FIVE TEMPERATURE VALUES ---")
print(ds["t2m"].values[:5])

# Print geographical coordinates
print("\n--- LOCATION ---")
print("Latitude:", ds.latitude.values)
print("Longitude:", ds.longitude.values)

# Print temperature statistics
print("\n--- TEMPERATURE STATISTICS ---")
print("Minimum:", float(ds["t2m"].min().values))
print("Maximum:", float(ds["t2m"].max().values))


ds.close()
