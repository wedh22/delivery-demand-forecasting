# 04. Weather Experiment

This experiment asks a narrow question:

> Does verified weather information improve out-of-sample delivery-demand forecasting beyond calendar and lag features?

## Design
The baseline and weather models must use:
- the same district(s)
- the same timestamps
- the same chronological train/test boundary
- the same evaluation metrics

This prevents apparent improvement caused only by comparing different samples.

## Candidate weather variables
Only fields verified against the original metadata will be used, such as temperature, precipitation, and wind-related variables. Legacy column names will not be interpreted by guesswork.

## Comparison
- Model A: calendar + lag features
- Model B: Model A + verified weather features

Results will be reported even if weather produces no improvement.
