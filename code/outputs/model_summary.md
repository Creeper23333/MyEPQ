# First Volatility Model Results

Generated: 2026-07-12T22:29:38+00:00

## Dataset

- Source file: `data/processed/hyperliquid_BTC_1d_volatility.csv`
- Model frame rows: 1188
- Train rows: 950 (2023-04-11 to 2025-11-15)
- Test rows: 238 (2025-11-16 to 2026-07-11)
- Forecast target: next-day 30-day realised volatility, not annualised

## Result

Best first-pass model by RMSE: **Lagged linear regression** with RMSE `0.00141843`.

| Rank | Model | Category | MAE | MSE | RMSE |
| --- | --- | --- | --- | --- | --- |
| 1 | Lagged linear regression | Interpretable lag-feature model | 0.00074798 | 0.00000201 | 0.00141843 |
| 2 | Rolling historical volatility | Benchmark | 0.00063564 | 0.00000209 | 0.00144481 |
| 3 | LSTM | Machine learning | 0.00106690 | 0.00000339 | 0.00184029 |
| 4 | Random Forest | Machine learning | 0.00121584 | 0.00000443 | 0.00210549 |
| 5 | GARCH(1,1) | Traditional statistical | 0.00987357 | 0.00016712 | 0.01292761 |

## Notes

- Rolling historical volatility is the transparent benchmark.
- GARCH(1,1) is fitted by grid-search maximum likelihood with variance targeting, then converted into a 30-day realised-volatility forecast using the most recent 29 observed returns plus the one-step-ahead conditional variance.
- Random Forest is a lightweight in-repo implementation because the current environment does not include scikit-learn.
- LSTM is fitted using PyTorch on rolling 30-day sequences of core market features. Early stopping selected epoch 8 using a chronological validation split.


## Output Files

- `code/outputs/model_performance.csv`
- `code/outputs/model_predictions.csv`
- `code/outputs/random_forest_feature_importance.csv`
- `code/outputs/garch_parameters.json`
- `code/outputs/lstm_training_summary.json`
- `code/outputs/volatility_forecast_comparison.png`
