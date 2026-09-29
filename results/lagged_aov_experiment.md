# Lagged Average Order Value Experiment — Dongjak-gu

## Question
Can historical average order value add predictive information without using same-hour realized values that would be unavailable at forecast time?

## Leakage control
The contemporaneous average order value is **not** used. Only exact timestamp-aligned values from:
- 24 hours earlier
- 168 hours earlier

are added to the baseline features.

The source average-order-value table is aggregated to district × hour by taking the simple mean across available categories. This is a pragmatic legacy-data feature and should not be interpreted as a transaction-weighted district average.

## Fair-comparison sample
Because the average-order-value data end earlier than the delivery-order data, all models are re-evaluated on the same rows.

- Modeling rows: **9,102**
- Sample: **2019-07-24 11:00 → 2021-01-01 23:00**
- Train rows: **7,281**
- Test rows: **1,821**
- Test period: **2020-10-13 08:00 → 2021-01-01 23:00**
- Chronological 80/20 split

## Results

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Base Linear | 9.0435 | 14.1149 | 0.8769 |
| Linear + lagged AOV | **9.0402** | **14.1083** | **0.8770** |
| Base Random Forest | 11.4681 | 18.5825 | 0.7867 |
| RF + lagged AOV | **11.0612** | **17.9146** | **0.8017** |

## Interpretation
The lagged average-order-value features provide almost no change for Linear Regression. They improve Random Forest on this restricted holdout, but Random Forest still underperforms Linear Regression on the same sample.

This experiment therefore does **not** justify replacing the current full-period pilot model. It shows that historical order-value information may contain some incremental signal for a nonlinear model, while also demonstrating that model rankings can change across evaluation periods.

## Important limitations
- The average-order-value table ends before the full delivery-order dataset, so these scores are not directly comparable to the full-period pilot scores.
- The district-hour AOV feature is a simple mean of category-level averages because transaction-level weights are unavailable in this table.
- The experiment establishes predictive association only; it does not imply that order value causes demand.
- Same-hour realized AOV remains excluded from the forecasting model because of leakage risk.

## Decision
Keep lagged AOV as an optional experimental feature rather than a required production feature. The main baseline remains calendar + exact timestamp-aligned historical demand lags until broader validation is completed.
