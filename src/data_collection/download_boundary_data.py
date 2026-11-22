
from pathlib import Path
import cdsapi

dataset = "reanalysis-era5-land"

request = {
    "variable": ["2m_temperature"],
    "year": "2004",
    "month": ["12"],
    "day": ["31"],
    "time": [
        "19:00", "20:00", "21:00",
        "22:00", "23:00"
    ],
    "data_format": "netcdf",
    "download_format": "unarchived",
    "area": [28.7, 77.1, 28.5, 77.3]
}

output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "delhi_boundary_2004-12-31.nc"

client = cdsapi.Client()

print("Downloading Delhi boundary observations...")

client.retrieve(dataset, request, str(output_file))

print("Download successful:", output_file)
