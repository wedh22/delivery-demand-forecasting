"""Cross-district robustness evaluation for high-coverage districts."""
from pathlib import Path
import numpy as np
import pandas as pd
from data_schema import load_orders
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

RAW = Path("data/raw/delivery_orders.csv")
OUT = Path("results")
OUT.mkdir(exist_ok=True)

DISTRICTS = ["동작구", "관악구", "영등포구", "구로구", "금천구"]
FEATURES = ["hour","dayofweek","month","is_weekend","lag_1h","lag_24h","lag_168h"]

def score(y, p):
    return (
        mean_absolute_error(y,p),
        np.sqrt(mean_squared_error(y,p)),
        r2_score(y,p),
    )

raw = load_orders(RAW)
raw["timestamp"] = raw["date"] + pd.to_timedelta(raw["hour"], unit="h")
rows=[]

for district in DISTRICTS:
    x=(raw.loc[raw["district"].eq(district)]
          .groupby("timestamp",as_index=False)["order_count"].sum()
          .sort_values("timestamp"))
    x["hour"]=x.timestamp.dt.hour
    x["dayofweek"]=x.timestamp.dt.dayofweek
    x["month"]=x.timestamp.dt.month
    x["is_weekend"]=(x.dayofweek>=5).astype(int)

    base=x[["timestamp","order_count"]]
    for lag in (1,24,168):
        past=base.copy()
        past["timestamp"] += pd.Timedelta(hours=lag)
        past=past.rename(columns={"order_count":f"lag_{lag}h"})
        x=x.merge(past,on="timestamp",how="left",validate="one_to_one")

    x=x.dropna(subset=FEATURES+["order_count"])
    cut=int(len(x)*.8)
    tr,te=x.iloc[:cut],x.iloc[cut:]

    models={
        "Naive24": te["lag_24h"].to_numpy(),
    }
    lin=LinearRegression().fit(tr[FEATURES],tr["order_count"])
    models["Linear"]=lin.predict(te[FEATURES])
    rf=RandomForestRegressor(n_estimators=300,min_samples_leaf=2,
                             random_state=42,n_jobs=-1)
    rf.fit(tr[FEATURES],tr["order_count"])
    models["RandomForest"]=rf.predict(te[FEATURES])

    for name,pred in models.items():
        mae,rmse,r2=score(te["order_count"],pred)
        rows.append({
            "district":district,"model":name,"n_model":len(x),
            "n_test":len(te),"test_start":te.timestamp.min(),
            "test_end":te.timestamp.max(),"MAE":mae,"RMSE":rmse,"R2":r2
        })

pd.DataFrame(rows).to_csv(OUT/"cross_district_validation.csv",index=False)
print(pd.DataFrame(rows).round(4).to_string(index=False))
