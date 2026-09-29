# 01. Data Preprocessing

This notebook documents the reproducible preprocessing design for the 2026 rebuild.

> The raw datasets are not stored in this repository. File names and column mappings must be adapted to the locally obtained source files.

## 1. Analysis unit
The initial modeling unit is **district × date × hour**. The target is the hourly delivery order count.

## 2. Core principles
- Parse date/time explicitly.
- Aggregate orders before joining auxiliary datasets.
- Join datasets only on documented keys.
- Do not interpret a missing timestamp as zero demand until data coverage has been checked.
- Create lag variables only after chronological sorting.
- Do not use variables that would be unknown at forecast time.

## 3. Python template

```python
import pandas as pd
import numpy as np

# Replace this path with the locally obtained raw delivery-order file.
orders = pd.read_csv("../data/raw/delivery_orders.csv")

required = ["date", "hour", "district", "order_count"]
missing = [c for c in required if c not in orders.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

orders["date"] = pd.to_datetime(orders["date"])
orders["hour"] = pd.to_numeric(orders["hour"], errors="coerce")

hourly = (
    orders.groupby(["district", "date", "hour"], as_index=False)["order_count"]
          .sum()
          .sort_values(["district", "date", "hour"])
)

hourly["timestamp"] = hourly["date"] + pd.to_timedelta(hourly["hour"], unit="h")
hourly["dayofweek"] = hourly["timestamp"].dt.dayofweek
hourly["month"] = hourly["timestamp"].dt.month
hourly["is_weekend"] = (hourly["dayofweek"] >= 5).astype(int)

# Lag features are generated separately within each district.
for lag in [1, 24, 168]:
    hourly[f"lag_{lag}h"] = hourly.groupby("district")["order_count"].shift(lag)

print(hourly.head())
print(hourly.isna().sum())
```

## 4. Coverage checks before modeling

```python
coverage = (
    hourly.groupby("district")
          .agg(
              first_timestamp=("timestamp", "min"),
              last_timestamp=("timestamp", "max"),
              observed_hours=("timestamp", "nunique"),
              total_orders=("order_count", "sum"),
          )
          .sort_values("observed_hours", ascending=False)
)

coverage["possible_hours"] = (
    (coverage["last_timestamp"] - coverage["first_timestamp"])
    .dt.total_seconds()
    .div(3600)
    .add(1)
)

coverage["coverage_rate"] = coverage["observed_hours"] / coverage["possible_hours"]
coverage
```

## 5. Weather join template

Weather variables must first be mapped to their official metadata. Do not guess column meanings from legacy column names.

```python
# Example only after official column mapping has been verified.
# weather = pd.read_csv("../data/raw/weather.csv")
# weather["timestamp"] = pd.to_datetime(weather["timestamp"])
# model_df = hourly.merge(
#     weather,
#     on=["district", "timestamp"],
#     how="left",
#     validate="many_to_one",
# )
```

## 6. Output
After coverage and join validation, save only a locally processed modeling table. Large processed files remain excluded from GitHub.

```python
# model_df.to_csv("../data/processed/model_table.csv", index=False)
```
