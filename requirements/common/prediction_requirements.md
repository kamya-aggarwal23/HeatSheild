
# HeatShield V1 — Common Prediction Requirements

## 1. Prediction Objective

The system will predict the next day's maximum temperature (Tmax) for Delhi and Tokyo using historical daily weather observations.

## 2. Prediction Frequency and Horizon

- Prediction frequency: Daily
- Prediction horizon: One day ahead
- Target variable: Next day's maximum temperature (°C)
- A separate model will initially be developed for each city.

## 3. Model Input

The initial model will use eight consecutive daily maximum-temperature observations.

| Input Feature | Description |
|---|---|
| Lag 1 | Today's maximum temperature |
| Lag 2 | Previous day's maximum temperature |
| Lag 3 | Maximum temperature 2 days ago |
| Lag 4 | Maximum temperature 3 days ago |
| Lag 5 | Maximum temperature 4 days ago |
| Lag 6 | Maximum temperature 5 days ago |
| Lag 7 | Maximum temperature 6 days ago |
| Lag 8 | Maximum temperature 7 days ago |

## 4. Expected Prediction Output

The system will generate:

1. **Predicted Tmax:** Forecast maximum temperature for the next day in °C.
2. **Heat Day Classification:** Binary output indicating whether the predicted temperature crosses the city's defined Heat Day threshold.
   - 1 = Heat Day
   - 0 = Not a Heat Day
3. **Severity Category:** An additional city-specific temperature category derived from predicted Tmax, where defined.

## 5. City-Specific Heat Day Thresholds

| City | Heat Day Threshold |
|---|---|
| Delhi | Predicted Tmax ≥ 40°C |
| Tokyo | Predicted Tmax ≥ 35°C |

These are project-defined thresholds for V1 classification and should not be interpreted as official heatwave declarations.

## 6. Severity Classification

Tokyo's initial severity categories:

| Predicted Tmax | Category |
|---|---|
| Below 25°C | Normal |
| 25°C to below 30°C | Warm |
| 30°C to below 35°C | Hot |
| 35°C or above | Extremely Hot |

Delhi's severity categories will be defined separately after further research.

## 7. Model Development

The following models will be evaluated:

- Persistence Baseline: Tomorrow's Tmax is assumed to be equal to today's Tmax.
- Seasonal Average Baseline: Prediction based on historical seasonal temperature averages.
- Ridge Regression: Linear model with L2 regularization.
- Linear Regression.
- Random Forest Regressor.
- Gradient Boosting (optional, depending on time).

All models will initially use the same input features for fair comparison.

## 8. Prediction Evaluation

The following metrics will be used:

### Regression Metrics
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- Extreme-Heat MAE

### Classification Metrics
- Precision
- Recall
- Confusion Matrix

The project aims for at least 98% Heat Day Recall while maintaining reasonable Precision. This is an aspirational target, not a guaranteed result.

## 9. Validation Requirements

- Use chronological Train/Validation/Test splitting.
- Do not randomly shuffle time-series observations.
- Avoid future-data leakage.
- Use only information available at prediction time.
- Evaluate the final model on unseen future dates.
- Perform error analysis for both cities.

## 10. Prediction Constraints

- Predictions will be made one day ahead only.
- Only daily maximum temperature will be used in the initial model.
- Humidity-based heat index is outside the initial scope.
- Predictions will be generated independently for Delhi and Tokyo.
- Classification will be derived from predicted Tmax.

## 11. Future Improvements

- Experiment with additional weather variables.
- Add seasonal and calendar-based features.
- Explore more advanced forecasting models.
- Improve city-specific heat classification.
- Develop a simple prediction interface.
