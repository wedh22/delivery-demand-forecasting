"""Shared schema loader for the legacy Korean delivery-order CSV."""
from pathlib import Path
import pandas as pd

RAW = Path("data/raw/delivery_orders.csv")

ALIASES = {
    "date": ["date", "날짜"],
    "hour": ["hour", "시간대별 시간"],
    "district": ["district", "시군구명"],
    "order_count": ["order_count", "주문 건수"],
}

def load_orders(path=RAW):
    df = pd.read_csv(path, encoding="utf-8-sig")
    rename = {}
    for canonical, candidates in ALIASES.items():
        hit = next((c for c in candidates if c in df.columns), None)
        if hit is None:
            raise ValueError(f"Missing {canonical}; accepted columns: {candidates}")
        rename[hit] = canonical
    df = df.rename(columns=rename)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["hour"] = pd.to_numeric(df["hour"], errors="coerce")
    df["order_count"] = pd.to_numeric(df["order_count"], errors="coerce")
    return df.dropna(subset=["date","hour","district","order_count"])
