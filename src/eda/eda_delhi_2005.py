
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the dataset
df = pd.read_csv("data/processed/delhi_daily_2005.csv")

df["date"] = pd.to_datetime(df["date"])

# 2. Basic dataset information
print("\n--- DATASET OVERVIEW ---")
print(df.head())
print("\nShape:", df.shape)
print("\nData types:")
print(df.dtypes)

# 3. Statistical summary
print("\n--- STATISTICAL SUMMARY ---")
print(df["tmax"].describe())

# 4. Check missing values and duplicates
print("\n--- DATA QUALITY ---")
print("Missing values:", df.isnull().sum())
print("Duplicate dates:", df["date"].duplicated().sum())

# 5. Monthly temperature analysis
df["month"] = df["date"].dt.month

monthly = df.groupby("month")["tmax"].agg(
    ["mean", "min", "max"]
)

print("\n--- MONTHLY TEMPERATURE ---")
print(monthly.round(2))

# 6. Heat day analysis (Delhi threshold: 40°C)
heat_days = df[df["tmax"] >= 40]

print("\n--- HEAT DAY ANALYSIS ---")
print("Total heat days:", len(heat_days))
print(heat_days[["date", "tmax"]])

print("\n--- MONTHLY HEAT DAY COUNTS ---")

heat_days_by_month = (
    df[df["tmax"] >= 40]
    .groupby("month")
    .size()
    .reindex(range(1, 13), fill_value=0)
)

print(heat_days_by_month)

# 7. Hottest and coldest days
print("\n--- TOP 10 HOTTEST DAYS ---")
print(df.nlargest(10, "tmax")[["date", "tmax"]])

print("\n--- TOP 10 COLDEST DAYS ---")
print(df.nsmallest(10, "tmax")[["date", "tmax"]])

# 8. Temperature distribution
plt.figure(figsize=(10, 5))
plt.hist(df["tmax"], bins=20, edgecolor="black")
plt.title("Delhi Daily Maximum Temperature Distribution - 2005")
plt.xlabel("Temperature (°C)")
plt.ylabel("Number of Days")
plt.tight_layout()
plt.savefig("reports/figures/delhi_temperature_distribution_2005.png")
plt.show()

# 9. Daily temperature trend
plt.figure(figsize=(12, 5))
plt.plot(df["date"], df["tmax"])
plt.axhline(y=40, linestyle="--", label="Heat Day Threshold (40°C)")
plt.title("Delhi Daily Maximum Temperature - 2005")
plt.xlabel("Date")
plt.ylabel("Maximum Temperature (°C)")
plt.legend()
plt.tight_layout()
plt.savefig("reports/figures/delhi_temperature_trend_2005.png")
plt.show()

# 10. Monthly average temperature
plt.figure(figsize=(10, 5))
plt.plot(monthly.index, monthly["mean"], marker="o")
plt.title("Average Monthly Maximum Temperature - Delhi 2005")
plt.xlabel("Month")
plt.ylabel("Average Tmax (°C)")
plt.xticks(range(1, 13))
plt.tight_layout()
plt.savefig("reports/figures/delhi_monthly_average_2005.png")
plt.show()

print("\nEDA completed successfully!")
