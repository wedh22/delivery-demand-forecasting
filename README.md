# Delivery Demand Forecasting

Machine Learning-Based Delivery Demand Forecasting

## Overview
This repository revisits and extends an undergraduate capstone project originally conducted in 2022. The original project explored delivery-demand forecasting and its possible use in delivery operations and pricing decisions.

The 2026 revision rebuilds the analysis from the raw data, with a stronger focus on reproducible preprocessing, time-aware validation, model comparison, and honest interpretation of limitations.

## Research question
Can hourly delivery demand be forecast using calendar information, historical demand patterns, and external variables such as weather?

## Current scope
- Target: hourly delivery order count
- Pilot area: Guro-gu, Seoul
- Core predictors: hour, day of week, weekend indicator, month, and lagged demand
- Candidate external predictors: weather and other variables that would be available at prediction time
- Validation: chronological train/test split rather than random splitting
- Metrics: MAE, RMSE, and R²

## Modeling plan
1. Naive time-series baseline
2. Linear Regression
3. Random Forest
4. Additional tree-based models if they provide a justified improvement
5. Incremental feature experiments to test whether external data actually improves forecasting

## Important methodology note
Variables that are only known after the target time should not be used as forecasting inputs. For example, same-hour realized average order value may be useful for descriptive analysis, but using it as a predictor of same-hour order count can introduce information leakage. It will therefore not be included in the main forecasting model unless a valid forecast-time version can be constructed.

## Project history
### Original Capstone (2022)
The undergraduate project explored machine-learning-based delivery demand analysis and its possible connection to rider supply and delivery-fee decisions.

### Revisited & Extended Project (2026)
The project is being rebuilt from the original raw files. The revision focuses on:
- reconstructing the dataset using explicit join keys
- checking missing periods and regional coverage
- preventing data leakage
- using time-aware validation
- comparing simple and nonlinear models
- testing external variables incrementally
- documenting limitations instead of overstating results

## Repository structure
```text
.
├── README.md
├── data/
│   └── README.md
├── notebooks/
├── figures/
├── requirements.txt
└── .gitignore
```

## Data
Large raw datasets are not committed to this repository. The `data/README.md` file documents the data structure, provenance notes, and reproducibility plan.

## Status
Work in progress. Results will be added only after the preprocessing and evaluation pipeline is reproducible.
