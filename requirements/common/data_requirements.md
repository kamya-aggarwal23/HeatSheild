# HeatShield V1 — Common Data Requirements

## 1. Objective

To collect consistent historical hourly 2-metre air temperature data for Delhi, India and Tokyo, Japan, and derive daily maximum temperatures for next-day heat prediction.

## 2. Data Source

- Provider: Open-Meteo Historical Weather API
- API Endpoint: https://archive-api.open-meteo.com/v1/archive
- Dataset: ERA5-Land
- Model identifier: `era5_land`
- Historical data period: 1 January 2005 to 31 December 2025
- Collection frequency: Hourly
- Final output frequency: Daily

Both cities must use the same dataset and weather variable.

## 3. Cities and Locations

| City | Country | Time Zone |
|---|---|---|
| Delhi | India | Asia/Kolkata |
| Tokyo | Japan | Asia/Tokyo |

City-specific coordinates will be maintained in their respective city requirement files.

## 4. Required Weather Variable

| Parameter | Value |
|---|---|
| Variable | `temperature_2m` |
| Description | Air temperature at 2 metres above ground |
| Collection frequency | Hourly |
| Unit | °C |
| Dataset | ERA5-Land |

Only this variable will be collected for the initial V1 dataset.

## 5. Hourly Data Collection

- Download hourly `temperature_2m` observations.
- Request timestamps in UTC.
- Preserve the original hourly timestamps and temperature values.
- Store raw hourly observations separately for each city.
- Do not calculate daily maximum temperatures using UTC calendar dates.

## 6. Timezone Conversion and Daily Aggregation

The hourly timestamps must be converted from UTC to the respective city's local timezone before daily aggregation.

Processing sequence:

1. Read hourly observations and UTC timestamps.
2. Convert UTC timestamps to the city's local timezone.
3. Extract the local calendar date.
4. Group observations by local calendar date.
5. Calculate the maximum hourly temperature for each local date.
6. Save the resulting daily dataset.

The final statistic is the maximum hourly 2-metre temperature recorded during each local calendar day.

## 7. Final Dataset Structure

Each city's processed dataset must contain:

| Column | Description | Unit |
|---|---|---|
| date | Local calendar date | YYYY-MM-DD |
| temperature_2m_max | Maximum hourly 2-metre temperature for that local date | °C |

Both cities must follow the same column naming convention and units.

## 8. Data Storage

Raw hourly datasets:

- `data/raw/delhi_hourly_2005_2025.csv`
- `data/raw/tokyo_hourly_2005_2025.csv`

Processed daily datasets:

- `data/processed/delhi_daily_2005_2025.csv`
- `data/processed/tokyo_daily_2005_2025.csv`

Raw hourly data must remain unchanged after collection. Timezone conversion and aggregation must produce separate processed datasets.

## 9. Data Quality Requirements

The collected and processed datasets must be checked for:

- Missing hourly observations.
- Missing local calendar dates.
- Duplicate timestamps.
- Duplicate local dates in processed datasets.
- Incorrect or inconsistent units.
- Invalid temperature values.
- Chronological ordering.
- Correct UTC-to-local timezone conversion.
- Expected hourly observations per local day.

Any missing or invalid observations must be investigated and documented before model development.

## 10. Data Consistency

- Both cities must use Open-Meteo Historical Weather API.
- Both cities must use ERA5-Land.
- Both cities must use hourly `temperature_2m`.
- Both datasets must cover the same intended historical period.
- Temperatures must be recorded in Celsius.
- Daily aggregation must use each city's local calendar date.
- The same processing methodology must be applied to both cities.

## 11. Limitations

- ERA5-Land is reanalysis data and may differ from actual ground-station observations.
- Its approximately 0.1° spatial resolution represents gridded weather conditions rather than measurements at every individual location.
- Missing hourly observations can affect the calculated daily maximum.
- The final daily dataset depends on correct timezone conversion and aggregation.

## 12. Future Improvements

- Add humidity and other weather variables if required.
- Explore additional heat-risk indicators.
- Compare ERA5-Land with other historical datasets.
- Introduce additional features during feature engineering.

**Final V1 data output:** Daily maximum 2-metre temperature in °C, calculated from hourly ERA5-Land observations using each city's local calendar day.