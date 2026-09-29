# Reproducibility Contract

This repository separates **reported results** from exploratory code. The frozen Dongjak-gu pilot is defined by the following choices:

- pilot district: Dongjak-gu, selected by hourly coverage before model comparison;
- missing timestamps are not filled with zero;
- lags are joined by exact timestamps at t-1h, t-24h, and t-168h;
- rows missing any required model feature are excluded;
- chronological 80/20 train/test split;
- predictors: hour, day of week, month, weekend indicator, and the three demand lags;
- Linear Regression uses the same numeric feature table as Random Forest;
- Random Forest: 300 trees, min_samples_leaf=2, random_state=42;
- permutation importance: frozen holdout, negative MAE scoring, 10 repeats, random_state=42.

The expected frozen pilot metrics are:

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Naive 24h | 5.1133 | 9.3772 | 0.8093 |
| Linear Regression | 4.4351 | 7.2347 | 0.8865 |
| Random Forest | 4.0676 | 6.3335 | 0.9130 |

A reproduction should be treated as successful only if it rebuilds these values from the legitimately obtained legacy source data under the same software/data assumptions. Small differences caused by library-version behavior should be documented rather than silently overwritten.
