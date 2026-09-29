# Investigation of Large Holdout Errors

This note investigates two dates highlighted by the frozen Dongjak-gu holdout diagnostics. External context is treated as a **hypothesis source**, not as proof of causality.

## 2021-03-16 — unusually low observed demand
At 18:00, the frozen holdout contains:
- observed orders: 10
- Random Forest prediction: 72.19
- absolute error: 62.19

The same date also appears among the largest errors at 19:00 and 20:00. Historical Seoul weather records indicate light rain/mist on March 16, but this alone does not explain the sharp multi-hour drop.

### Current interpretation
**Unresolved.** Before treating this as a real demand shock, inspect:
1. category-level order counts for Dongjak-gu during those hours;
2. whether many categories disappear simultaneously;
3. neighboring timestamps and neighboring districts;
4. any source-data collection discontinuity.

The observations remain in the holdout and are not removed.

## 2021-03-01 — unusually high observed demand
Multiple hours on March 1 appear among large positive residuals. Historical weather reports show rain/snow in Seoul and unusually heavy precipitation in the capital region around March 1–2.

### Current interpretation
Adverse weather is a plausible contextual hypothesis for elevated delivery demand, but the project does **not** claim that weather caused the residuals. A valid test would require timestamp-aligned weather coverage for this holdout period and controlled comparison.

## Research lesson
Large residuals should trigger investigation rather than automatic outlier deletion. External events can suggest hypotheses, while the order-source structure must be checked before deciding whether an observation represents real behavior or a data-quality problem.
