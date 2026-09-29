# Model Diagnostics Plan

The next stage moves beyond a single performance score and asks **where the model works, where it fails, and which historical signals it relies on**.

## Diagnostics to produce
1. **Actual vs predicted demand over time** on the untouched chronological test period.
2. **Absolute-error distribution** and the largest-error timestamps.
3. **Error by hour of day** to identify systematic weak periods.
4. **Permutation importance** on the holdout set.

## Why permutation importance?
Impurity-based Random Forest importance can favor continuous or high-cardinality variables. Permutation importance measures how much holdout performance deteriorates when one feature is shuffled, so it is used as the primary diagnostic here.

Importance is still **not causal evidence**. A lag feature can be highly predictive because it captures recurring demand patterns without causing future demand.

## Guardrails
- Diagnostics are computed on the same frozen test period used for evaluation.
- Test data are not used to tune the model after inspecting errors.
- Large errors are described rather than removed unless a documented data-quality issue is found.
- Feature importance is reported as predictive reliance, not causal influence.
