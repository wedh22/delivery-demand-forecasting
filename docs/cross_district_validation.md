# Cross-District Validation Protocol

The next validation stage tests whether the forecasting pipeline is useful beyond the single Dongjak-gu pilot.

## Candidate districts
Use the next highest-coverage districts from the pre-model coverage audit:
- Gwanak-gu
- Yeongdeungpo-gu
- Guro-gu
- Geumcheon-gu

Dongjak-gu remains the frozen pilot and is not re-selected based on model score.

## Evaluation rule
For each district independently:
1. Aggregate to district × timestamp.
2. Keep missing timestamps missing; do not fill them with zero.
3. Build exact timestamp-aligned 1h, 24h, and 168h demand lags.
4. Drop rows without the required lag history.
5. Use the final 20% of observations as the chronological holdout.
6. Compare Naive-24h, Linear Regression, and Random Forest with the same metrics.
7. Report every district result, including weak results.

## Interpretation
This is a robustness check, not proof of deployment-level generalization. Districts have different coverage, date patterns, and demand distributions. Performance differences may reflect both real demand structure and legacy data collection differences.

No district will be excluded merely because its model score is low.
