
# HeatShield V1 — Project Scope

## 1. Project Objective

HeatShield is a machine-learning project that predicts the next day's maximum temperature using historical daily weather data and identifies whether the upcoming day qualifies as a Heat Day.

V1 focuses on two cities with different climatic conditions:

- Delhi, India
- Tokyo, Japan

The project will initially develop and evaluate a separate prediction model for each city.

## 2. Primary Goal

Help identify upcoming extreme-heat days by predicting tomorrow's maximum temperature and converting that prediction into a city-specific Heat Day classification.

## 3. Prediction Tasks

HeatShield V1 has two related outputs: predicted maximum temperature and a derived Heat Day classification. A secondary city-specific severity category will also be provided where defined.

### A. Regression — Temperature Prediction

Predict the next day's maximum temperature in degrees Celsius (°C).

### B. Classification — Heat Day Detection

Convert the predicted maximum temperature into a binary classification:

- 0 — Not a Heat Day
- 1 — Heat Day

This classification is derived from the regression model's predicted temperature using the respective city's threshold.

## 4. City-Specific Heat Day Definitions

The initial V1 thresholds are project-defined absolute temperature thresholds.

| City | Predicted Tmax Threshold |
|---|---|
| Delhi | Maximum temperature >= 40°C |
| Tokyo | Maximum temperature >= 35°C |

A predicted temperature below the city's threshold is classified as Not a Heat Day.

These are simplified project thresholds, not complete official heatwave declaration criteria.

## 5. Secondary Output — Temperature Severity

In addition to the binary Heat Day flag, HeatShield may display a temperature severity category.

### Tokyo

| Maximum Temperature | Severity |
|---|---|
| Below 25°C | Normal |
| 25°C to below 30°C | Warm |
| 30°C to below 35°C | Hot |
| 35°C and above | Extremely Hot |

### Delhi

City-specific severity bands will be finalized separately after reviewing Delhi's climate characteristics.

The secondary severity output does not replace the primary binary Heat Day classification.

## 6. Initial Model Inputs

The initial baseline model will use eight consecutive daily maximum-temperature observations:

- Today's maximum temperature.
- Maximum temperatures from the previous seven days.

Additional weather variables and seasonal features may be investigated in later feature-engineering stages.

Only information available up to the prediction date may be used as model input.

## 7. Prediction Frequency and Horizon

- Frequency: Daily
- Forecast horizon: One day ahead
- Prediction target: Next day's maximum temperature
- Initial approach: One separate model per city.

A combined multi-city model is outside the initial V1 scope.

## 8. Model Evaluation

Regression performance will be evaluated using:

- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)

Heat Day detection will be evaluated using:

- Precision
- Recall
- Confusion Matrix

The primary project goal is to achieve at least 98% recall on Heat Days, while maintaining precision as high as possible.

The 98% recall target is aspirational and must be evaluated honestly on unseen future data.

## 9. Validation Strategy

- Use chronological training, validation and testing datasets.
- Do not randomly shuffle time-series observations.
- Prevent future-data leakage.
- Evaluate final performance on unseen future dates.

## 10. V1 Limitations

- Daily predictions only.
- One-day-ahead forecasting only.
- Separate initial models for Delhi and Tokyo.
- Maximum temperature as the initial model input.
- No hourly forecasting.
- No humidity-based heat index.
- No advanced heat-risk recommendations.
- No combined multi-city model.

## 11. Future Improvements

- Additional weather variables such as humidity, rainfall and wind.
- Seasonal and calendar features.
- Improved city-specific heat classification.
- Combined multi-city forecasting.
- Hourly forecasting.
- Advanced model architectures and heat-risk recommendations.

## 12. V1 Success Criteria

HeatShield V1 will be evaluated based on:

1. Reliable next-day maximum-temperature prediction.
2. Performance compared with simple baseline models.
3. Heat Day recall, targeting at least 98%.
4. Precision and false-alarm analysis.
5. Honest evaluation on unseen future dates.
