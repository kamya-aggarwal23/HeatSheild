
# HeatShield V1 — Common Data Requirements

## 1. Objective
To collect and prepare consistent historical daily weather data for Delhi, India and Tokyo, Japan for next-day maximum temperature forecasting.

## 2. Data Source
- Source: Open-Meteo Historical Weather API
- API Endpoint: https://archive-api.open-meteo.com/v1/archive
- Data Type: Historical weather data
- Frequency: Daily
- Proposed Date Range: 1 January 2005 to 31 December 2025
- The final date range will depend on data availability and consistency for both cities.

## 3. Cities and Locations

| City | Country | Time Zone |
|---|---|---|
| Delhi | India | Asia/Kolkata |
| Tokyo | Japan | Asia/Tokyo |

City-specific coordinates and weather station details will be maintained in their respective city requirement files.

## 4. Required Weather Variables

| Variable | API Variable Name | Unit |
|---|---|---|
| Maximum Temperature | temperature_2m_max | °C |
| Minimum Temperature | temperature_2m_min | °C |
| Mean Temperature | temperature_2m_mean | °C |
| Total Precipitation | precipitation_sum | mm |
| Maximum Wind Speed | wind_speed_10m_max | km/h |
| Mean Relative Humidity | relative_humidity_2m_mean | % |

These variables will be collected for initial analysis and possible future feature engineering.

**Note:** The initial baseline model will use only eight consecutive daily maximum-temperature observations as input features. Collecting additional variables does not mean they will all be used in the initial model.

## 5. Common Dataset Structure

Each city's dataset should contain the following columns:

| Column | Description |
|---|---|
| date | Date of observation |
| temperature_2m_max | Daily maximum temperature |
| temperature_2m_min | Daily minimum temperature |
| temperature_2m_mean | Daily mean temperature |
| precipitation_sum | Total daily precipitation |
| wind_speed_10m_max | Maximum daily wind speed |
| relative_humidity_2m_mean | Mean daily relative humidity |

Both datasets must follow the same column naming convention and units.

## 6. Data Storage

Raw datasets will be stored separately:

- data/raw/delhi_daily_2005_2025.csv
- data/raw/tokyo_daily_2005_2025.csv

Processed datasets will be stored in the processed data directory after cleaning.

Raw data must remain unchanged.

## 7. Data Quality Requirements

The collected datasets must be checked for:

- Missing dates and missing values.
- Duplicate records.
- Incorrect or inconsistent units.
- Invalid temperature values.
- Chronological ordering of dates.
- Consistent date formats.

Any missing or invalid observations must be handled carefully and documented.

## 8. Data Consistency

- Both cities must use the same data source.
- The same selected historical weather/reanalysis model should be used for both cities wherever available.
- Both datasets should follow the same date range as far as possible.
- All temperatures must be recorded in Celsius.
- Dates must follow the local timezone of each city.

### Data Source and Model Consistency Rules

1. Both Delhi and Tokyo datasets must be collected using Open-Meteo Historical Weather API.
2. Both cities must use the same selected historical weather/reanalysis model.
3. Do not use different models for the two cities without discussing and documenting the reason.
4. Before downloading the data, both team members must confirm the selected model, date range, variables and units.
5. Record the selected model and API parameters in the data collection documentation.

## 9. Limitations

- Historical data availability may vary between cities.
- Reanalysis data may differ from actual ground-station observations.
- Missing observations may affect model performance.
- The initial model focuses on daily maximum temperature rather than hourly weather conditions.

## 10. Future Improvements

- Add additional weather variables as model features.
- Compare different historical weather datasets.
- Include seasonal and calendar-based features.
- Explore more detailed weather indicators for heat-risk prediction.

**Note:** The selected data source, model, date range and variable availability must be verified during data collection before finalizing the datasets.
