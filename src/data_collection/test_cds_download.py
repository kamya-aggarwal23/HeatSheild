
from pathlib import Path
import cdsapi

# HeatShield: Delhi ERA5-Land hourly temperature test

dataset = "reanalysis-era5-land"

request = {
    "variable": ["2m_temperature"],
    "year": "2005",
    "month": "01",
    "day": ["01"],
    "time": [
        "00:00", "01:00", "02:00", "03:00",
        "04:00", "05:00", "06:00", "07:00",
        "08:00", "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00", "15:00",
        "16:00", "17:00", "18:00", "19:00",
        "20:00", "21:00", "22:00", "23:00"
    ],
    "data_format": "netcdf",
    "download_format": "unarchived",
    "area": [28.6, 77.1, 28.5, 77.2]
}

# Create output directory if it doesn't exist
output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "delhi_test_2005-01-01.nc"

print("Connecting to Copernicus Climate Data Store...")
client = cdsapi.Client()

print("Requesting Delhi hourly temperature data...")
client.retrieve(dataset, request, str(output_file))

print(f"\nDownload completed: {output_file}")
print(f"File size: {output_file.stat().st_size / 1024:.2f} KB")

