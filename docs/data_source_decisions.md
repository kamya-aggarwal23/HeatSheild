
# HeatShield V1 — Data Source Decision

## 1. Selected Historical Dataset

- Provider: Open-Meteo
- API: Historical Weather API
- Selected Dataset: ERA5
- Data Type: Historical Reanalysis
- Frequency: Daily
- Cell Selection: Land

## 2. Historical Date Range

- Start Date: 2005-01-01
- End Date: 2025-12-31

## 3. City Configuration

| Parameter | Delhi | Tokyo |
|---|---|---|
| Latitude | 28.58 | 35.68 |
| Longitude | 77.20 | 139.69 |
| Timezone | Asia/Kolkata | Asia/Tokyo |

## 4. Selected Weather Variables

| Variable | API Name | Unit |
|---|---|---|
| Maximum Temperature | temperature_2m_max | °C |
| Minimum Temperature | temperature_2m_min | °C |
| Mean Temperature | temperature_2m_mean | °C |
| Precipitation | precipitation_sum | mm |
| Maximum Wind Speed | wind_speed_10m_max | km/h |
| Mean Relative Humidity | relative_humidity_2m_mean | % |

## 5. API Validation

Test requests were performed for:

- 1 January 2005
- 31 December 2025

Both Delhi and Tokyo successfully returned all six requested variables.

The returned timezone matched each city's local timezone.

The returned grid coordinates differed slightly from the requested coordinates because ERA5 uses a spatial grid.

## 6. Reason for Selection

ERA5 was selected because:

- It provides global coverage.
- It supports all six required variables.
- It covers the proposed 2005–2025 historical period.
- It allows both cities to use a consistent historical dataset.

## 7. Team Decision

Both team members agreed to use ERA5 for Delhi and Tokyo.

## 8. Pending Verification

- Verify complete date coverage.
- Check missing dates and missing values.
- Check duplicate records.
- Verify units and column consistency.
- Document any data quality issues.
