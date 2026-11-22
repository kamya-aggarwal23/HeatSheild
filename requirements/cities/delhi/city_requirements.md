\# Delhi — City Requirements

## 1. City Information

- City: Delhi
- Country: India
- Timezone: Asia/Kolkata
- Assigned Developer: Kamya
- Weather Station Reference: New Delhi (Safdarjung)
- Latitude: 28.58° N
- Longitude: 77.20° E

## 2. Historical Weather Patterns

Delhi experiences significant seasonal variations in temperature and rainfall.

### Summer Season
- Summer generally begins around April and continues until June.
- May and June experience very high temperatures.
- Hot and dry conditions are common during the pre-monsoon period.
- Maximum temperatures can reach or exceed 40°C during extreme summer conditions.

### Monsoon Season
- The southwest monsoon generally arrives around late June or early July.
- July and August receive a major share of Delhi's annual rainfall.
- Humidity increases during this period.
- Maximum temperatures generally decrease compared with peak pre-monsoon summer.

### Winter Season
- Winter generally occurs from December to February.
- January is among the coldest months.
- Cold waves and dense fog can occur.
- Minimum temperatures can fall considerably during cold spells.

### Spring and Post-Monsoon
- February and March represent the transition towards summer.
- September and October represent the transition away from the monsoon.
- October generally experiences lower rainfall and gradually decreasing temperatures.

## 3. Data Collection Requirements

- Dataset: ERA5-Land
- Data Source: Open-Meteo Historical Weather API
- API Endpoint: https://archive-api.open-meteo.com/v1/archive
- API Model Identifier: `era5_land`
- Variable: `temperature_2m`
- Variable Description: Hourly air temperature at 2 metres above ground
- Collection Frequency: Hourly
- Temperature Unit: °C
- Start Date: 2005-01-01
- End Date: 2025-12-31
- Requested Timezone: UTC

### Timezone Conversion and Daily Aggregation

ERA5-Land hourly timestamps will initially be collected in UTC.

The following processing sequence must be applied:

1. Read the hourly temperature observations and UTC timestamps.
2. Convert UTC timestamps to `Asia/Kolkata`.
3. Extract the local calendar date.
4. Group hourly observations by local calendar date.
5. Calculate the maximum hourly temperature for each local date.
6. Save the resulting daily maximum-temperature dataset.

Daily maximum temperatures must be calculated after timezone conversion, not by grouping observations using UTC dates.

## 4. Potential Temperature Influencing Factors

The following factors may influence Delhi's daily maximum temperature:

- Recent daily maximum temperatures
- Seasonal variations
- Previous days' temperature patterns
- Day of the year
- Humidity
- Rainfall
- Wind speed
- Cloud cover

For the initial V1 model, eight consecutive daily maximum-temperature observations will be considered as input features.

Other weather variables may be investigated in future versions depending on data availability and model performance.

## 5. Extreme Heat Characteristics

Delhi is located in the northern Indian plains and experiences severe summer heat.

According to India Meteorological Department (IMD) criteria:

- A heat-wave consideration threshold for plains is a maximum temperature of 40°C or above.
- A heat wave based on departure from normal is declared when the maximum temperature is 4.5°C to 6.4°C above normal.
- A severe heat wave based on departure from normal is declared when the departure is greater than 6.4°C.
- Based on actual maximum temperature, heat wave conditions correspond to 45°C or above, and severe heat wave conditions to 47°C or above.

The official declaration also considers station coverage and persistence criteria.

For HeatShield, an appropriate city-specific project classification must be finalized separately. A simple temperature threshold should not be presented as an official IMD heat-wave declaration.

## 6. Research Sources

1. India Meteorological Department (IMD)
   - https://mausam.imd.gov.in/

2. Regional Meteorological Centre, New Delhi
   - https://rmcnewdelhi.imd.gov.in/

3. IMD Safdarjung Climatological Data
   - https://rmcnewdelhi.imd.gov.in/rwfc/uploads/safdarjung2.pdf

4. Tokyo Climate Center — New Delhi/Safdarjung Climate Normals
   - https://www.data.jma.go.jp/tcc/tcc/products/climate/normal/parts/NrmMonth_e.php?stn=42182

5. Delhi Disaster Management Authority
   - https://ddma.delhi.gov.in/

## 7. Initial Observations

- Delhi experiences strong seasonal temperature variations.
- May and June are particularly important months for extreme heat analysis.
- Monsoon rainfall is concentrated mainly in July and August.
- Temperature patterns differ significantly between pre-monsoon and monsoon periods.
- Winter conditions include low temperatures and frequent fog.
- Historical temperature and seasonal patterns should be considered when developing a next-day forecasting model.

These observations are preliminary and will be further investigated using the collected and processed dataset.

## 8. V1 Model Features

The initial V1 model will use eight consecutive daily maximum-temperature observations.

Potential input features:

- Lag 1: Today's maximum temperature
- Lag 2: Previous day's maximum temperature
- Lag 3: Maximum temperature two days ago
- Lag 4: Maximum temperature three days ago
- Lag 5: Maximum temperature four days ago
- Lag 6: Maximum temperature five days ago
- Lag 7: Maximum temperature six days ago
- Lag 8: Maximum temperature seven days ago

Target variable:

- Next day's maximum temperature in degrees Celsius.

Potential future features:

- Humidity
- Rainfall
- Wind speed
- Cloud cover
- Seasonal and calendar features

These additional features will be considered after examining the collected dataset.

## 9. Expected Output Files

Raw hourly dataset:
- `data/raw/delhi_hourly_2005_2025.csv`

Processed daily dataset:
- `data/processed/delhi_daily_2005_2025.csv`

The processed dataset must contain one daily maximum-temperature observation per local calendar date.

---

**Status:** Updated city requirements for hourly ERA5-Land data collection.

**Next Step:** Implement and validate Delhi hourly data collection and local-time daily aggregation.
