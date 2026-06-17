# First Model Results Summary

## Dataset and Split

- Data source: Hyperliquid BTC daily perpetual futures candles.
- Processed file: `data/processed/hyperliquid_BTC_1d_volatility.csv`
- Forecast target: next-day 30-day realised volatility, not annualised.
- Model frame rows: 1163.
- Training period: 2023-04-11 to 2025-10-26.
- Test period: 2025-10-27 to 2026-06-16.

## First-Pass Performance

| Rank | Model | Category | MAE | MSE | RMSE |
| --- | --- | --- | --- | --- | --- |
| 1 | Lagged linear regression | Interpretable lag-feature model | 0.00076728 | 0.00000208 | 0.00144239 |
| 2 | Rolling historical volatility | Benchmark | 0.00065181 | 0.00000215 | 0.00146692 |
| 3 | Random Forest | Machine learning | 0.00127180 | 0.00000469 | 0.00216639 |
| 4 | GARCH(1,1) | Traditional statistical | 0.01021477 | 0.00017326 | 0.01316280 |

The first-pass results do not show a clear machine-learning advantage. The best RMSE is produced by lagged linear regression, while the transparent rolling-volatility benchmark is extremely close. The lightweight Random Forest performs worse than both of these simpler approaches. This supports a more critical final discussion: model complexity does not automatically improve forecasting accuracy.

## Interpretation

The strongest result is not that machine learning wins, but that recent realised volatility is highly informative for next-day realised volatility. Rolling historical volatility is difficult to beat because the target itself is a rolling volatility measure. This means the project should discuss whether the evaluation target favours persistence-based models.

The Random Forest's most important features are also volatility persistence features, especially 30-day rolling return standard deviation, current realised volatility, and recent realised-volatility lags. This is useful for interpretability because it shows that the model is mainly learning continuity in volatility rather than discovering a completely new nonlinear structure.

GARCH(1,1) underperforms in this first pass. One possible reason is that GARCH estimates a conditional daily return variance, while the project target is a next-day 30-day realised-volatility estimate. The script converts the one-step GARCH variance into a 30-day realised-volatility forecast, but the result still appears less aligned with the rolling target than direct lag-based models.

## Evidence Files

- `code/outputs/model_performance.csv`
- `code/outputs/model_predictions.csv`
- `code/outputs/random_forest_feature_importance.csv`
- `code/outputs/garch_parameters.json`
- `code/outputs/volatility_forecast_comparison.png`
- `code/outputs/model_summary.md`

## Next Modelling Steps

1. Add a stronger Random Forest implementation using scikit-learn if package installation is allowed.
2. Try a small LSTM prototype if TensorFlow or PyTorch can be added.
3. Test robustness with a different realised-volatility window, such as 14 days or 60 days.
4. Consider whether the target should be next-day absolute return or future realised volatility over a forward-looking window.
