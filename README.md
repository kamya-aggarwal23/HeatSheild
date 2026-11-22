# HeatShield

A machine learning-based heat forecasting system that predicts next-day maximum temperatures and identifies heat days across different climatic regions.

## Project Overview

HeatShield initially focuses on two cities:

- Delhi, India
- Tokyo, Japan

The project uses historical weather data to forecast the next day's maximum temperature. The predicted temperature is then used to determine whether the following day qualifies as a Heat Day according to the project's city-specific thresholds.

## Data Collection Methodology

- **Data Source:** Open-Meteo Historical Weather API
- **Dataset:** ERA5-Land
- **Variable:** Hourly 2-metre air temperature (`temperature_2m`)
- **Period:** 2005–2025
- **Collection Frequency:** Hourly
- **Final Output:** Daily maximum temperature in °C

Hourly timestamps are initially collected in UTC. They are converted to each city's local timezone before grouping observations by local calendar date and calculating daily maximum temperature.

## Project Structure

```text
HeatShield/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── requirements/
│   ├── common/
│   └── cities/
│       ├── delhi/
│       └── tokyo/
└── src/
    └── data_collection/
```

## Machine Learning Approach

1. Historical weather data collection
2. Data understanding and preprocessing
3. Exploratory data analysis
4. Feature engineering
5. Chronological train-test split and baseline models
6. Linear Regression and Random Forest
7. Evaluation and error analysis
8. Prediction pipeline

## Collaboration

- Kamya: Delhi research and implementation.
- Sarthak: Tokyo research and implementation.
- Both contributors collaborate on common methodology, model evaluation and integration.

## Project Status

Currently working on Day 2: Historical hourly weather data collection and daily maximum-temperature aggregation.