# Current Model Results Summary

## Dataset and Validation

- Data source: Hyperliquid BTC daily perpetual-futures candles.
- Latest refresh: 2026-07-13; latest returned complete candle: 2026-07-12.
- Primary target: next-day 30-day realised volatility, not annualised.
- Primary frame: 1,188 rows; 950 train and 238 test observations.
- Validation: fixed chronological 80/20 holdout, not random and not walk-forward refitting.
- Robustness target: next-day 14-day realised volatility.

## Corrected Primary Performance

| Rank | Model | Category | MAE | MSE | RMSE |
| --- | --- | --- | --- | --- | --- |
| 1 | GARCH(1,1) | Traditional statistical | 0.00047808 | 0.00000099 | 0.00099637 |
| 2 | Lagged linear regression | Interpretable lag-feature model | 0.00074798 | 0.00000201 | 0.00141843 |
| 3 | Rolling historical volatility | Benchmark | 0.00063564 | 0.00000209 | 0.00144481 |
| 4 | LSTM | Machine learning | 0.00106690 | 0.00000339 | 0.00184029 |
| 5 | Random Forest | Machine learning | 0.00122445 | 0.00000452 | 0.00212715 |

GARCH improves RMSE by 31.0% relative to rolling historical volatility. Machine learning does not produce an accuracy advantage: LSTM and Random Forest are 27.4% and 47.2% worse than rolling by RMSE.

## Method Correction

The modelling audit found that earlier GARCH predictions were extracted by reset dataframe row number after feature engineering removed incomplete early rows. The pipeline now maps forecasts to test observations by date and rejects missing or duplicate mappings. This correction changed GARCH from the earlier invalid last-place result to the valid first-place result. Other model predictions were unaffected.

## Robustness

| Window | Winner | Winner RMSE | Rolling RMSE | Improvement over rolling |
| --- | --- | --- | --- | --- |
| 14 days | GARCH(1,1) | 0.00179214 | 0.00278701 | 35.7% |
| 30 days | GARCH(1,1) | 0.00099637 | 0.00144481 | 31.0% |

All five models retain the same rank at both windows: GARCH, linear regression, rolling historical volatility, LSTM, and Random Forest. This supports ranking stability across the two tested target definitions, but it does not prove stability across different assets or market regimes.

## Multi-Dimensional Interpretation

GARCH has the strongest current balance: first-place accuracy at both windows, three interpretable parameters, deterministic fitting, and moderate local runtime. Rolling historical volatility is the most transparent but less accurate. Linear regression is fast and coefficient-based but only narrowly improves RMSE over rolling and has worse MAE. Random Forest supplies global feature importance but no directional or prediction-level explanation. LSTM records its 6,049-parameter architecture and training history but remains the least directly interpretable.

The current local run measured roughly 0.6 seconds to fit GARCH and several seconds for each machine-learning implementation. These timings are implementation- and hardware-specific, so the exact values should be taken from `model_computational_profile.csv` rather than presented as universal algorithm benchmarks.

## Evidence Files

- `code/outputs/model_performance.csv`
- `code/outputs/model_predictions.csv`
- `code/outputs/model_multidimensional_comparison.csv`
- `code/outputs/model_computational_profile.csv`
- `code/outputs/model_robustness_by_window.csv`
- `code/outputs/random_forest_feature_importance.csv`
- `code/outputs/linear_regression_coefficients.csv`
- `code/outputs/garch_parameters.json`
- `code/outputs/lstm_training_summary.json`
- `code/outputs/lstm_training_history.csv`
- `code/outputs/model_run_metadata.json`
- `code/outputs/volatility_forecast_comparison.png`
- `code/outputs/model_summary.md`

## Close-Out Direction

The final report should use the corrected GARCH result and make the implementation audit explicit. Further model expansion is lower priority than final report editing, presentation construction, and transfer of the updated production log into the official form.
