"""Baseline forecasting models for hourly delivery demand.

Run this after producing data/processed/model_table.csv.
The table must be chronologically sorted and contain:
timestamp, order_count, hour, dayofweek, month, is_weekend,
lag_1h, lag_24h, lag_168h.
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA = Path("data/processed/model_table.csv")
OUT = Path("results")
OUT.mkdir(exist_ok=True)

FEATURES = [
    "hour", "dayofweek", "month", "is_weekend",
    "lag_1h", "lag_24h", "lag_168h",
]
TARGET = "order_count"


def metrics(y_true, y_pred):
    return {
        "MAE": float(mean_absolute_error(y_true, y_pred)),
        "RMSE": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "R2": float(r2_score(y_true, y_pred)),
    }


df = pd.read_csv(DATA, parse_dates=["timestamp"]).sort_values("timestamp")
df = df.dropna(subset=[TARGET] + FEATURES).copy()

# Chronological 80/20 split: future observations are never used for training.
cut = int(len(df) * 0.8)
train, test = df.iloc[:cut], df.iloc[cut:]

X_train, y_train = train[FEATURES], train[TARGET]
X_test, y_test = test[FEATURES], test[TARGET]

# Naive baseline: yesterday at the same hour.
results = {"Naive_24h": metrics(y_test, test["lag_24h"])}

# Keep the feature representation identical to the frozen pilot:
# calendar fields and exact timestamp lags are used as numeric predictors.
linear = LinearRegression()
linear.fit(X_train, y_train)
results["LinearRegression"] = metrics(y_test, linear.predict(X_test))

rf = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    n_jobs=-1,
    min_samples_leaf=2,
)
rf.fit(X_train, y_train)
results["RandomForest"] = metrics(y_test, rf.predict(X_test))

pd.DataFrame(results).T.to_csv(OUT / "baseline_metrics.csv")
with open(OUT / "baseline_metrics.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(pd.DataFrame(results).T.round(4))
print(f"Train: {train['timestamp'].min()} -> {train['timestamp'].max()}")
print(f"Test : {test['timestamp'].min()} -> {test['timestamp'].max()}")
