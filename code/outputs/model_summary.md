# First Volatility Model Results

Generated: 2026-06-17T12:23:54+00:00

## Dataset

- Source file: `data/processed/hyperliquid_BTC_1d_volatility.csv`
- Model frame rows: 1163
- Train rows: 930 (2023-04-11 to 2025-10-26)
- Test rows: 233 (2025-10-27 to 2026-06-16)
- Forecast target: next-day 30-day realised volatility, not annualised

## Result

Best first-pass model by RMSE: **Lagged linear regression** with RMSE `0.00144239`.

| Rank | Model | Category | MAE | MSE | RMSE |
| --- | --- | --- | --- | --- | --- |
| 1 | Lagged linear regression | Interpretable lag-feature model | 0.00076728 | 0.00000208 | 0.00144239 |
| 2 | Rolling historical volatility | Benchmark | 0.00065181 | 0.00000215 | 0.00146692 |
| 3 | Random Forest | Machine learning | 0.00127180 | 0.00000469 | 0.00216639 |
| 4 | GARCH(1,1) | Traditional statistical | 0.01021477 | 0.00017326 | 0.01316280 |

## Notes

- Rolling historical volatility is the transparent benchmark.
- GARCH(1,1) is fitted by grid-search maximum likelihood with variance targeting, then converted into a 30-day realised-volatility forecast using the most recent 29 observed returns plus the one-step-ahead conditional variance.
- Random Forest is a lightweight in-repo implementation because the current environment does not include scikit-learn.
- LSTM is not included in this first pass because the current environment does not include TensorFlow or PyTorch. It should remain a planned extension unless a neural-network package is added.

## Output Files

- `code/outputs/model_performance.csv`
- `code/outputs/model_predictions.csv`
- `code/outputs/random_forest_feature_importance.csv`
- `code/outputs/garch_parameters.json`
- `code/outputs/volatility_forecast_comparison.png`
