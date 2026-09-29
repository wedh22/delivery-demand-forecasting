"""Audit hourly observation coverage before interpreting missing timestamps.

This script does NOT fill missing hours with zero. It measures coverage by
district and exports a report for selecting defensible pilot areas.
"""

from pathlib import Path
import pandas as pd
from data_schema import load_orders

DATA = Path("data/raw/delivery_orders.csv")
OUT = Path("results")
OUT.mkdir(exist_ok=True)

df = load_orders(DATA)
df["timestamp"] = df["date"] + pd.to_timedelta(df["hour"], unit="h")

hourly = (
    df.groupby(["district", "timestamp"], as_index=False)["order_count"]
      .sum()
      .sort_values(["district", "timestamp"])
)

rows = []
for district, g in hourly.groupby("district"):
    start, end = g["timestamp"].min(), g["timestamp"].max()
    expected = pd.date_range(start, end, freq="h")
    observed = pd.DatetimeIndex(g["timestamp"].unique())
    missing_hours = expected.difference(observed)

    rows.append({
        "district": district,
        "first_timestamp": start,
        "last_timestamp": end,
        "observed_hours": len(observed),
        "possible_hours": len(expected),
        "missing_hours": len(missing_hours),
        "coverage_rate": len(observed) / len(expected),
        "total_orders": g["order_count"].sum(),
    })

report = pd.DataFrame(rows).sort_values(
    ["coverage_rate", "observed_hours"], ascending=False
)
report.to_csv(OUT / "coverage_by_district.csv", index=False)

# Missing-time examples are exported for inspection, not automatically imputed.
pilot = report.iloc[0]["district"]
g = hourly.loc[hourly["district"].eq(pilot)]
expected = pd.date_range(g["timestamp"].min(), g["timestamp"].max(), freq="h")
missing = expected.difference(pd.DatetimeIndex(g["timestamp"].unique()))
pd.DataFrame({"missing_timestamp": missing}).to_csv(
    OUT / "pilot_missing_timestamps.csv", index=False
)

print(report.to_string(index=False))
print(f"\nHighest-coverage district: {pilot}")
print("Missing hours were NOT converted to zero demand.")
