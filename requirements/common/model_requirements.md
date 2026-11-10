# HeatShield V1 — Common Model Requirements

## 1. Project Objective

Develop a machine-learning system that predicts the next day's maximum temperature using historical daily weather observations.

## 2. Prediction Type

- Machine Learning Task: Supervised Learning
- Primary Task: Regression
- Prediction Frequency: Daily
- Prediction Horizon: 1 day ahead

## 3. Initial Input Features

The initial model will use 8 consecutive daily maximum-temperature observations.

| Feature | Description |
|---|---|
| Lag 1 | Today's maximum temperature |
| Lag 2 | Previous day's maximum temperature |
| Lag 3 | Maximum temperature 2 days ago |
| Lag 4 | Maximum temperature 3 days ago |
| Lag 5 | Maximum temperature 4 days ago |
| Lag 6 | Maximum temperature 5 days ago |
| Lag 7 | Maximum temperature 6 days ago |
| Lag 8 | Maximum temperature 7 days ago |

## 4. Mathematical Representation

\[
T_{\max}(t+1)=f(T_{\max}(t),T_{\max}(t-1),...,T_{\max}(t-7))
\]

Where:
- t represents the current day.
- t+1 represents the next day.
- f represents the machine-learning model.
- The output is the predicted maximum temperature in °C.

## 5. Expected Output

1. Predicted maximum temperature (°C).
2. Heat severity classification based on the predicted temperature and city-specific thresholds.

## 6. Baseline Models

Before implementing advanced machine-learning models, the following baselines will be evaluated:

- **Persistence Model:** Assumes tomorrow's maximum temperature will be equal to today's maximum temperature.
- **Ridge Regression:** A linear regression model with L2 regularization, using the same 8 lag features.

These baselines will help determine whether more complex models provide meaningful improvements.

## 7. Model Evaluation

The model will initially be evaluated using:

- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- Extreme-heat MAE (prediction error on extreme-heat days)
- Classification Recall (ability to identify extreme-heat days correctly)

Model performance will be compared against the baseline models.

## 8. Validation Strategy

- Use chronological Train/Validation/Test splitting.
- Never shuffle time-series data during splitting.
- Prevent future-data leakage during feature engineering and preprocessing.
- Fit preprocessing transformations using training data only.
- Evaluate final model performance on unseen future dates.

## 9. Initial Scope Limitations

- Daily predictions only.
- One-day-ahead prediction only.
- Maximum temperature as the initial input feature.
- No hourly forecasting.
- No humidity-based heat index.
- No advanced heat-risk recommendations.

## 10. Future Improvements

- Additional weather variables.
- Seasonal and calendar features.
- Hourly temperature prediction.
- City-specific heat-risk classification improvements.
- Improved model architectures.

**Note:** These are common V1 requirements. City-specific datasets, weather patterns and classification thresholds will be documented separately.