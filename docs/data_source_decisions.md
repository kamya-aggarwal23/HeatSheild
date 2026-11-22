# HeatShield — Data Source Decisions

## 1. Selected Data Source

- Provider: Open-Meteo
- API: Historical Weather API
- Endpoint: https://archive-api.open-meteo.com/v1/archive
- Selected Dataset: ERA5-Land
- API Model Identifier: `era5_land`

## 2. Reason for Selection

ERA5-Land provides hourly historical land-surface weather data with approximately 0.1° spatial resolution.

It supports the hourly 2-metre temperature variable required for the initial HeatShield V1 dataset.

## 3. Collection Configuration

| Parameter | Decision |
|---|---|
| Model | ERA5-Land |
| Variable | `temperature_2m` |
| Frequency | Hourly |
| Unit | °C |
| Start date | 2005-01-01 |
| End date | 2025-12-31 |
| Requested timezone | UTC |

## 4. City Configuration

| City | Latitude | Longitude | Local Timezone |
|---|---:|---:|---|
| Delhi | 28.58 | 77.20 | Asia/Kolkata |
| Tokyo | 35.68 | 139.69 | Asia/Tokyo |

## 5. UTC-to-Local-Time Processing

ERA5 hourly timestamps are handled as UTC timestamps.

For each city:

1. Collect hourly temperature observations in UTC.
2. Convert timestamps to the city's local timezone.
3. Extract the local calendar date.
4. Group observations by local calendar date.
5. Calculate the maximum hourly temperature for each date.

Timezone conversion must happen before daily aggregation to avoid assigning observations to incorrect calendar dates.

## 6. Storage Decisions

Raw hourly data:

- `data/raw/delhi_hourly_2005_2025.csv`
- `data/raw/tokyo_hourly_2005_2025.csv`

Processed daily data:

- `data/processed/delhi_daily_2005_2025.csv`
- `data/processed/tokyo_daily_2005_2025.csv`

Raw hourly data must remain unchanged.

## 7. Validation Requirements

- Verify API response and temperature units.
- Check hourly timestamp continuity.
- Identify missing and duplicate timestamps.
- Verify timezone conversion.
- Check local calendar-day coverage.
- Validate daily maximum aggregation.
- Document incomplete or missing observations.

## 8. Final Decision

Both cities will use ERA5-Land hourly `temperature_2m` observations from 2005 through 2025.

The final V1 dataset will contain daily maximum 2-metre temperature calculated using each city's local calendar day.

**Status:** Selected methodology documented. Full data collection and validation pending.