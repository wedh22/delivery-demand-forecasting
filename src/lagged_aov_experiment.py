"""Compare baseline demand features with leakage-safe lagged average order value.

Expected local files are intentionally not committed. Adapt column names only
to the documented source schema.
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def metrics(y, p):
    return {
        "MAE": mean_absolute_error(y, p),
        "RMSE": np.sqrt(mean_squared_error(y, p)),
        "R2": r2_score(y, p),
    }

# Critical rule:
# NEVER use contemporaneous realized average order value to predict the same
# timestamp's order count. Create AOV features by exact timestamp alignment.
#
# Example after district-hour AOV aggregation:
# for lag in (24, 168):
#     past = aov[["timestamp", "avg_order_value"]].copy()
#     past["timestamp"] += pd.Timedelta(hours=lag)
#     past = past.rename(columns={"avg_order_value": f"aov_lag_{lag}h"})
#     model_df = model_df.merge(past, on="timestamp", how="left",
#                               validate="one_to_one")
#
# Evaluate baseline and augmented models on the intersection of complete rows
# so any difference is caused by features rather than a changed test sample.
