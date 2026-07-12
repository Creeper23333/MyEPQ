# Current Volatility Model Results

Generated: 2026-07-12T23:17:23+00:00

## Dataset

- Source file: `data/processed/hyperliquid_BTC_1d_volatility.csv`
- Model frame rows: 1188
- Train rows: 950 (2023-04-11 to 2025-11-15)
- Test rows: 238 (2025-11-16 to 2026-07-11)
- Forecast target: next-day 30-day realised volatility, not annualised
- Validation: fixed chronological 80/20 holdout; no random shuffling and no walk-forward refitting

## Result

Best current model by RMSE: **GARCH(1,1)** with RMSE `0.00099637`.

| Rank | Model | Category | MAE | MSE | RMSE |
| --- | --- | --- | --- | --- | --- |
| 1 | GARCH(1,1) | Traditional statistical | 0.00047808 | 0.00000099 | 0.00099637 |
| 2 | Lagged linear regression | Interpretable lag-feature model | 0.00074798 | 0.00000201 | 0.00141843 |
| 3 | Rolling historical volatility | Benchmark | 0.00063564 | 0.00000209 | 0.00144481 |
| 4 | LSTM | Machine learning | 0.00106690 | 0.00000339 | 0.00184029 |
| 5 | Random Forest | Machine learning | 0.00122445 | 0.00000452 | 0.00212715 |

## Notes

- Rolling historical volatility is the transparent benchmark.
- GARCH(1,1) is fitted by grid-search maximum likelihood with variance targeting, then converted into a 30-day realised-volatility forecast using recent observed returns plus the one-step-ahead conditional variance.
- Random Forest is a lightweight in-repo implementation because the current environment does not include scikit-learn.
- LSTM is fitted using PyTorch on rolling 30-day sequences of core market features. Early stopping selected epoch 8 using a chronological validation split.

## Computational Practicality

Timings are from one local CPU run and are implementation-specific, so they indicate relative project cost rather than universal benchmark speed.

| Model | Fit seconds | Predict seconds | Complexity |
| --- | --- | --- | --- |
| Rolling historical volatility | 0.000000 | 0.000016 | 0 fitted parameters |
| GARCH(1,1) | 0.619200 | 0.009327 | 3 fitted parameters |
| Lagged linear regression | 0.000277 | 0.000031 | 27 coefficients including intercept |
| Random Forest | 5.216042 | 0.037448 | 18036 tree nodes across forest |
| LSTM | 3.843683 | 0.006044 | 6049 trainable parameters |

## Robustness Across Target Windows

| Window | Rank | Model | RMSE | Difference from rolling benchmark |
| --- | --- | --- | --- | --- |
| 14 days | 1 | GARCH(1,1) | 0.00179214 | -35.697% |
| 14 days | 2 | Lagged linear regression | 0.00262221 | -5.913% |
| 14 days | 3 | Rolling historical volatility | 0.00278701 | 0.000% |
| 14 days | 4 | LSTM | 0.00360202 | 29.243% |
| 14 days | 5 | Random Forest | 0.00391877 | 40.608% |
| 30 days | 1 | GARCH(1,1) | 0.00099637 | -31.038% |
| 30 days | 2 | Lagged linear regression | 0.00141843 | -1.826% |
| 30 days | 3 | Rolling historical volatility | 0.00144481 | 0.000% |
| 30 days | 4 | LSTM | 0.00184029 | 27.372% |
| 30 days | 5 | Random Forest | 0.00212715 | 47.226% |

## Output Files

- `code/outputs/model_performance.csv`
- `code/outputs/model_predictions.csv`
- `code/outputs/random_forest_feature_importance.csv`
- `code/outputs/linear_regression_coefficients.csv`
- `code/outputs/garch_parameters.json`
- `code/outputs/lstm_training_summary.json`
- `code/outputs/lstm_training_history.csv`
- `code/outputs/model_computational_profile.csv`
- `code/outputs/model_multidimensional_comparison.csv`
- `code/outputs/model_robustness_by_window.csv`
- `code/outputs/model_run_metadata.json`
- `code/outputs/volatility_forecast_comparison.png`
- `code/outputs/model_summary.md`
