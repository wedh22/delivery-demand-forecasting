# Weather Experiment Results — Dongjak-gu

## Question
Does adding the available weather fields improve hourly delivery-demand forecasting beyond calendar and exact timestamp-aligned lag features?

## Fair-comparison sample
Weather coverage ends earlier than the full delivery-order pilot. Therefore, baseline and weather models were re-evaluated on the **same weather-overlap sample** rather than comparing weather models against the earlier full-period baseline.

- Modeling rows: **6,088**
- Sample: **2019-07-24 11:00 → 2020-07-31 23:00**
- Chronological 80/20 split
- Test begins: **2020-05-24 20:00**

## Results

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Base Linear | 4.2399 | 5.7297 | 0.7366 |
| + Weather Linear | 4.2403 | 5.7166 | 0.7378 |
| Base Random Forest | **3.6439** | **5.0058** | **0.7990** |
| + Weather Random Forest | 3.7288 | 5.1330 | 0.7886 |

## Interpretation
Weather produced essentially neutral results for Linear Regression: RMSE and R² improved slightly while MAE worsened slightly. For Random Forest, adding the available weather fields **reduced holdout performance** on all three metrics.

Accordingly, this experiment does **not** support a claim that the available weather variables improve the current Random Forest demand forecast.

## Important caveat
One numeric field in the legacy weather source has not yet been mapped confidently to official metadata. It is therefore kept generically identified in the analysis rather than being given a guessed semantic label. The result should be treated as a legacy-data experiment until the source metadata are verified.

## Why these R² values differ from the full pilot
The earlier Dongjak-gu pilot used delivery observations through July 2021. This weather experiment is restricted to the period where weather and order data overlap, ending July 2020. The scores are therefore not directly comparable to the full-period pilot score.

## Next step
Keep the simpler calendar + lag Random Forest as the current forecasting baseline. Evaluate additional features only when they are available at prediction time and can be aligned without leakage.
