# 02. Exploratory Data Analysis

The purpose of this stage is to understand the data before choosing a final forecasting model. No causal claim should be made from these descriptive plots alone.

## Questions
1. Is the observation coverage stable over time?
2. Which districts have enough observations for modeling?
3. What hourly and weekly demand patterns are visible?
4. Are there structural changes across months or years?
5. How concentrated is demand by delivery category?
6. Do weather variables show useful associations after their metadata are verified?

## Python template

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/processed/model_table.csv", parse_dates=["timestamp"])

# Hour-of-day pattern
hourly_pattern = df.groupby("hour", as_index=False)["order_count"].mean()

plt.figure(figsize=(9, 4))
plt.plot(hourly_pattern["hour"], hourly_pattern["order_count"], marker="o")
plt.xlabel("Hour")
plt.ylabel("Mean order count")
plt.title("Mean Delivery Demand by Hour")
plt.tight_layout()
plt.show()

# Day-of-week pattern
dow_pattern = df.groupby("dayofweek", as_index=False)["order_count"].mean()

plt.figure(figsize=(9, 4))
plt.bar(dow_pattern["dayofweek"], dow_pattern["order_count"])
plt.xlabel("Day of week (Mon=0)")
plt.ylabel("Mean order count")
plt.title("Mean Delivery Demand by Day of Week")
plt.tight_layout()
plt.show()

# Demand through time
daily = df.set_index("timestamp")["order_count"].resample("D").sum()

plt.figure(figsize=(11, 4))
plt.plot(daily.index, daily.values)
plt.xlabel("Date")
plt.ylabel("Daily order count")
plt.title("Delivery Demand Over Time")
plt.tight_layout()
plt.show()
```

## Data-quality checks

```python
# Missing values
print(df.isna().mean().sort_values(ascending=False).head(20))

# Duplicate modeling keys
keys = ["district", "timestamp"]
print("Duplicate keys:", df.duplicated(keys).sum())

# Target distribution
print(df["order_count"].describe())
```

## Interpretation rules
- Large district differences may reflect data collection coverage, not only true demand differences.
- Missing hours must not automatically be filled with zero.
- Weather correlations are descriptive unless evaluated in an out-of-sample forecasting experiment.
- Model performance will be evaluated on future observations using chronological splitting.
