# Delhi Weather Dataset – Data Validation Report

## 1. Dataset Overview

- **City:** Delhi, India
- **Data Source:** Open-Meteo Historical Weather API
- **Weather Model:** ERA5
- **Period:** 1 January 2005 – 31 December 2025
- **Total Records:** 7,670
- **Total Columns:** 7 (Date + 6 weather variables)

## 2. Missing Value Check

Checked all columns using Pandas `isnull().sum()`.

**Result:** Zero missing values in all columns.

## 3. Duplicate Date Check

Checked duplicate dates using Pandas `duplicated()`.

**Result:** Zero duplicate dates.

## 4. Statistical Summary

Used Pandas `describe()` to examine the numerical variables.

| Variable | Minimum | Maximum |
|---|---:|---:|
| Maximum Temperature | 10.3°C | 46.5°C |
| Minimum Temperature | 2.4°C | 35.3°C |
| Mean Temperature | 5.9°C | 40.0°C |
| Precipitation | 0 mm | 115.4 mm |
| Maximum Wind Speed | 4.3 km/h | 33.7 km/h |
| Mean Relative Humidity | 14% | 99% |

## 5. Temperature Consistency Check

Verified the following conditions:

- Maximum temperature ≥ Minimum temperature.
- Mean temperature ≤ Maximum temperature.
- Mean temperature ≥ Minimum temperature.

**Result:** Zero violations across all three conditions.

## 6. Humidity and Precipitation Check

- Relative humidity below 0%: 0 records.
- Relative humidity above 100%: 0 records.
- Negative precipitation: 0 records.

**Result:** All checks passed.

## 7. Conclusion

The Delhi weather dataset passed all the basic data-quality checks performed.

The dataset is ready for further exploratory data analysis and preprocessing, subject to subsequent checks for unusual observations and data suitability.

**Output File:** `data/raw/delhi_daily_2005_2025.csv`