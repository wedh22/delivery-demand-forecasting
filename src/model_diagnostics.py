"""Diagnostics for the frozen Random Forest baseline.

Run after the model table has been built. Produces prediction/error tables,
plots, and permutation importance on the chronological holdout.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error

DATA = Path("data/processed/model_table.csv")
OUT = Path("results")
FIG = Path("figures")
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

features = ["hour","dayofweek","month","is_weekend","lag_1h","lag_24h","lag_168h"]
df = pd.read_csv(DATA, parse_dates=["timestamp"]).sort_values("timestamp")
df = df.dropna(subset=["order_count"] + features).copy()
cut = int(len(df) * .8)
train, test = df.iloc[:cut], df.iloc[cut:].copy()

model = RandomForestRegressor(
    n_estimators=300, random_state=42, n_jobs=-1, min_samples_leaf=2
)
model.fit(train[features], train["order_count"])
test["prediction"] = model.predict(test[features])
test["error"] = test["order_count"] - test["prediction"]
test["abs_error"] = test["error"].abs()
test.to_csv(OUT / "dongjak_test_predictions.csv", index=False)

# Actual vs predicted
plt.figure(figsize=(12,4))
plt.plot(test["timestamp"], test["order_count"], label="Actual", linewidth=1)
plt.plot(test["timestamp"], test["prediction"], label="Predicted", linewidth=1)
plt.xlabel("Timestamp"); plt.ylabel("Orders")
plt.title("Actual vs Predicted — Chronological Holdout")
plt.legend(); plt.tight_layout()
plt.savefig(FIG / "dongjak_actual_vs_predicted.png", dpi=160)
plt.close()

# Error by hour
err_hour = test.groupby("hour", as_index=False)["abs_error"].mean()
err_hour.to_csv(OUT / "dongjak_mae_by_hour.csv", index=False)
plt.figure(figsize=(9,4))
plt.bar(err_hour["hour"], err_hour["abs_error"])
plt.xlabel("Hour"); plt.ylabel("Mean absolute error")
plt.title("Holdout Error by Hour")
plt.tight_layout()
plt.savefig(FIG / "dongjak_mae_by_hour.png", dpi=160)
plt.close()

# Largest errors: retain them for diagnosis rather than silently deleting them.
test.nlargest(25, "abs_error")[
    ["timestamp","order_count","prediction","error","abs_error"]
].to_csv(OUT / "dongjak_largest_errors.csv", index=False)

# Permutation importance on untouched holdout.
pi = permutation_importance(
    model, test[features], test["order_count"],
    scoring="neg_mean_absolute_error", n_repeats=10, random_state=42, n_jobs=-1
)
importance = pd.DataFrame({
    "feature": features,
    "mae_increase_mean": pi.importances_mean,
    "mae_increase_std": pi.importances_std,
}).sort_values("mae_increase_mean", ascending=False)
importance.to_csv(OUT / "permutation_importance.csv", index=False)

print("Holdout MAE:", mean_absolute_error(test["order_count"], test["prediction"]))
print(importance)
