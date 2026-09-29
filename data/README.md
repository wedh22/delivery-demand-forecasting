# Data

Raw project data are intentionally not committed to GitHub because the original files are large and redistribution rights must be checked before publication.

## Current data groups
- Delivery orders: date, hour, category, region/district, order count
- Average order value: date, hour, category, region/district, average order value
- Weather: date/time, district, precipitation-related fields, temperature, wind and related fields
- Regional auxiliary data: population, household/housing characteristics, and delivery-distance summaries

## Reproducibility policy
The 2026 rebuild will document the source and join keys for every dataset used in the final model. Only variables that would be available at prediction time will be used as forecasting predictors.

## Planned modeling unit
Pilot analysis: district × date × hour, with hourly delivery order count as the target.
