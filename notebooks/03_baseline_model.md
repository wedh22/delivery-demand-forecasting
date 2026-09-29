# 03. Baseline Model

This stage compares three forecasting approaches under the **same chronological holdout period**:

1. Naive baseline — previous day's same-hour demand
2. Linear Regression
3. Random Forest

The executable version is `src/baseline_model.py`.

## Why chronological splitting?
The task predicts future delivery demand. A random split can place later observations in training while earlier observations are in testing, which can make evaluation unrealistically optimistic. The pipeline therefore sorts by timestamp and reserves the final 20% as the test period.

## Features
- hour
- day of week
- month
- weekend indicator
- 1-hour lag
- 24-hour lag
- 168-hour lag

The target is hourly delivery order count.

## Evaluation
- MAE
- RMSE
- R²

No performance number is documented here until the processed dataset and exact coverage rules are finalized and the script can reproduce the result.

## Leakage rule
Same-hour realized variables that are unavailable at forecast time are excluded. External variables will be tested separately only after their timestamps and availability are verified.
