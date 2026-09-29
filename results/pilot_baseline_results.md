# Pilot Baseline Results — Dongjak-gu

## Scope
The first frozen pilot uses **Dongjak-gu, Seoul**, selected because it has the highest hourly observation coverage among the 25 districts in the supplied delivery-order dataset.

- Raw observation span: 2019-07-17 10:00 to 2021-07-31 23:00
- Hourly coverage: approximately **84.31%**
- Total observed orders: **259,203**
- Rows remaining after exact timestamp-aligned 1h/24h/168h lag requirements: **12,486**

The district was selected by coverage before comparing model scores.

## Chronological holdout
After lag construction:
- Train: 2019-07-24 11:00 → 2021-02-22 15:00 (9,988 observations)
- Test: 2021-02-22 16:00 → 2021-07-31 23:00 (2,498 observations)

## Results

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Naive 24h | 5.1133 | 9.3772 | 0.8093 |
| Linear Regression | 4.4351 | 7.2347 | 0.8865 |
| Random Forest | **4.0676** | **6.3335** | **0.9130** |

## Interpretation
On this pilot holdout, Random Forest produced the lowest MAE and RMSE and the highest R² among the three tested approaches. This is a **pilot result for the supplied Dongjak-gu observations**, not evidence that the model generalizes to all Seoul districts or future data.

## Important limitations
- The source dataset has incomplete hourly coverage; missing timestamps were **not** automatically treated as zero orders.
- District coverage varies substantially, so district totals should not be interpreted as complete measures of true Seoul-wide demand.
- The current result uses calendar and historical-demand lag features only.
- Weather and other external variables must be evaluated on the same timestamp sample before claiming incremental value.
- No causal interpretation is made from these forecasting results.

## Reproduction note
Lag values were aligned by exact timestamp (t-1h, t-24h, t-168h), rather than by simple row position, so gaps in the source data do not silently turn row lags into incorrect time lags.
