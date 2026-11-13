import requests
import pandas as pd
from pathlib import Path

API_URL = "https://archive-api.open-meteo.com/v1/archive"

PARAMETERS = {
    "latitude": 28.58,
    "longitude": 77.20,
    "start_date": "2005-01-01",
    "end_date": "2025-12-31",
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "temperature_2m_mean",
        "precipitation_sum",
        "wind_speed_10m_max",
        "relative_humidity_2m_mean"
    ],
    "timezone": "Asia/Kolkata",
    "models": "era5",
    "cell_selection": "land"
}
response = requests.get(API_URL, params=PARAMETERS, timeout=120)
response.raise_for_status()
weather_data = response.json()
daily_data = weather_data["daily"]
df = pd.DataFrame(daily_data)
# Get the project root directory
project_root = Path(__file__).resolve().parents[2]

# Create the raw data folder
raw_data_dir = project_root / "data" / "raw"
raw_data_dir.mkdir(parents=True, exist_ok=True)

# Define the output CSV file path
output_file = raw_data_dir / "delhi_daily_2005_2025.csv"

# Save the DataFrame as a CSV file
df.to_csv(output_file, index=False)

# Display basic information
print("Delhi weather data collected successfully!")
print("Total records:", len(df))
print("Date range:", df["time"].min(), "to", df["time"].max())
print("Dataset shape:", df.shape)

# Display first five rows
print(df.head())