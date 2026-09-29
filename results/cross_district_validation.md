# Cross-District Validation Results

The frozen forecasting pipeline was evaluated independently in the five highest-coverage districts selected before model-score comparison.

| District | Naive R² | Linear R² | RF R² | Lowest MAE model |
|---|---:|---:|---:|---|
| Dongjak-gu | 0.8093 | 0.8865 | **0.9130** | Random Forest (4.0676) |
| Gwanak-gu | 0.7059 | 0.8601 | **0.8826** | Random Forest (7.5026) |
| Yeongdeungpo-gu | 0.5604 | **0.7309** | 0.6062 | Linear (5.4660) |
| Guro-gu | 0.7267 | **0.8532** | 0.8250 | Linear (12.4288) |
| Geumcheon-gu | 0.6830 | 0.8120 | **0.8242** | Random Forest (7.0012) |

## Interpretation
The historical-demand feature set generalizes beyond Dongjak-gu in the limited sense that both learned models outperform the naive 24-hour baseline by R² in every tested district. However, **Random Forest is not consistently the best model**: Linear Regression performs better in Yeongdeungpo-gu and Guro-gu.

This is an important robustness result. The Dongjak-gu pilot should not be presented as evidence that one nonlinear model is universally superior. District-level demand structure and legacy data coverage differ, and the simpler linear model can be more robust in some holdout periods.

## Conclusion
Keep both Linear Regression and Random Forest in the project. The cross-district experiment supports the value of time-aware historical demand features more strongly than it supports a single universal model choice.

These results are predictive holdout results on the supplied historical observations, not deployment-level or Seoul-wide causal claims.
