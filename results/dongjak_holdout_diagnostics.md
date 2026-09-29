# Dongjak-gu Holdout Diagnostics

Diagnostics use the same frozen Dongjak-gu Random Forest baseline and chronological test period as the main pilot.

- Modeling rows: 12,486
- Test rows: 2,498
- Test period: 2021-02-22 16:00 → 2021-07-31 23:00
- Random Forest: 300 trees, min_samples_leaf=2, random_state=42

## Permutation importance
Importance is measured as the increase in holdout MAE after shuffling one feature (10 repeats).

| Feature | Mean MAE increase |
|---|---:|
| lag_1h | **5.8779** |
| lag_24h | **1.9446** |
| hour | **0.9220** |
| lag_168h | 0.2759 |
| dayofweek | 0.1364 |
| month | 0.0092 |
| is_weekend | 0.0089 |

The model relies most strongly on demand one hour earlier, followed by the previous-day same-hour demand. This is predictive reliance, **not causal importance**.

## Error by hour
The highest holdout MAE occurs at 19:00 (6.3625), followed by 18:00 (5.8933) and 20:00 (5.5106). Several high-error hours coincide with evening demand peaks, suggesting that sharp demand changes are harder to forecast.

## Largest individual errors
The largest absolute error occurs on 2021-03-16 18:00: observed 10 orders vs predicted 72.19. The same date also appears at 19:00 and 20:00 among the largest errors, so this cluster should be investigated as a possible unusual event, coverage discontinuity, or source-data issue rather than automatically removed.

2021-03-01 also appears multiple times with unusually high observed demand. These observations remain in the holdout.

## Interpretation
The diagnostics strengthen two conclusions:
1. recent historical demand carries most of the predictive signal;
2. large misses cluster at particular timestamps and peak-demand hours.

No large-error observation is deleted solely because it hurts model performance.
