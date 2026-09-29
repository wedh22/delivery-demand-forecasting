"""Build a leakage-aware hourly model table after coverage review.

Important: run coverage_audit.py first and explicitly choose a district whose
coverage is acceptable for the pilot analysis.
"""

from pathlib import Path
import pandas as pd
from data_schema import load_orders

RAW = Path("data/raw/delivery_orders.csv")
OUT = Path("data/processed/model_table.csv")
PILOT_DISTRICT = "동작구"

df = load_orders(RAW)

if PILOT_DISTRICT == "REPLACE_AFTER_COVERAGE_AUDIT":
    raise ValueError("Choose PILOT_DISTRICT from results/coverage_by_district.csv first.")

df = df.loc[df["district"].eq(PILOT_DISTRICT)].copy()
df["timestamp"] = df["date"] + pd.to_timedelta(df["hour"], unit="h")

hourly = (
    df.groupby("timestamp", as_index=False)["order_count"]
      .sum()
      .sort_values("timestamp")
)

# Critical rule: do not reindex to a complete hourly grid yet.
# A missing timestamp may mean missing collection rather than zero demand.
hourly["district"] = PILOT_DISTRICT
hourly["hour"] = hourly["timestamp"].dt.hour
hourly["dayofweek"] = hourly["timestamp"].dt.dayofweek
hourly["month"] = hourly["timestamp"].dt.month
hourly["is_weekend"] = (hourly["dayofweek"] >= 5).astype(int)

# shift(N rows) is only a true N-hour lag when timestamps are contiguous.
# Therefore, create lag values by timestamp self-join instead.
base = hourly[["timestamp", "order_count"]].copy()
for lag in (1, 24, 168):
    past = base.copy()
    past["timestamp"] = past["timestamp"] + pd.Timedelta(hours=lag)
    past = past.rename(columns={"order_count": f"lag_{lag}h"})
    hourly = hourly.merge(past, on="timestamp", how="left", validate="one_to_one")

OUT.parent.mkdir(parents=True, exist_ok=True)
hourly.to_csv(OUT, index=False)
print(hourly.head())
print(hourly.isna().sum())
