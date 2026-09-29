# Coverage & Missing-Time Protocol

This protocol is fixed **before** reporting final model performance.

## Why this matters
The legacy delivery dataset does not necessarily contain a record for every district-hour. An absent row can mean either:
1. true zero demand, or
2. missing / unavailable data collection.

Those cases cannot be treated as equivalent without evidence.

## Rules
1. Aggregate raw orders to district × timestamp.
2. Measure observed hours against all possible hours between each district's first and last timestamp.
3. Inspect missing-time patterns before choosing a pilot district.
4. Do **not** automatically impute absent hours as zero.
5. Do not select a district merely because it produces the best model score; selection must be based on data coverage and defensible scope.
6. Create 1h/24h/168h lags using timestamp alignment rather than simple row shifting when gaps exist.
7. Freeze the pilot scope and preprocessing rules before the final holdout evaluation.
8. Report the exact train/test dates with final metrics.

## Reproducible scripts
- `src/coverage_audit.py`: produces the district coverage report.
- `src/build_model_table.py`: creates the pilot model table after the district is explicitly chosen.
- `src/baseline_model.py`: evaluates the frozen model table chronologically.

## What is intentionally not decided yet
A numeric coverage threshold is not invented in advance. The distribution of coverage and the pattern of missing timestamps must be inspected first. The chosen rule and rationale will then be documented before final evaluation.
