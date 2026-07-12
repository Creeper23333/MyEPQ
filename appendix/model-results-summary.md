# First Model Results Summary

## Dataset and Split

- Data source: Hyperliquid BTC daily perpetual futures candles.
- Processed file: `data/processed/hyperliquid_BTC_1d_volatility.csv`
- Latest refresh date: 2026-07-13
- Latest available daily candle in the refreshed dataset: 2026-07-12
- Forecast target: next-day 30-day realised volatility, not annualised.
- Model frame rows: 1188.
- Training period: 2023-04-11 to 2025-11-15.
- Test period: 2025-11-16 to 2026-07-11.

## First-Pass Performance

| Rank | Model | Category | MAE | MSE | RMSE |
| --- | --- | --- | --- | --- | --- |
| 1 | Lagged linear regression | Interpretable lag-feature model | 0.00074798 | 0.00000201 | 0.00141843 |
| 2 | Rolling historical volatility | Benchmark | 0.00063564 | 0.00000209 | 0.00144481 |
| 3 | LSTM | Machine learning | 0.00106690 | 0.00000339 | 0.00184029 |
| 4 | Random Forest | Machine learning | 0.00121584 | 0.00000443 | 0.00210549 |
| 5 | GARCH(1,1) | Traditional statistical | 0.00987357 | 0.00016712 | 0.01292761 |

The refreshed first-pass results still do not show a clear machine-learning advantage over the best simple models. The best RMSE is produced by lagged linear regression, while the transparent rolling-volatility benchmark is extremely close. The implemented LSTM improves on the Random Forest but still does not surpass the two strongest simple baselines. This supports a more critical final discussion: model complexity does not automatically improve forecasting accuracy.

## Interpretation

The strongest result is not that machine learning wins, but that recent realised volatility is highly informative for next-day realised volatility. Rolling historical volatility is difficult to beat because the target itself is a rolling volatility measure. This means the project should discuss whether the evaluation target favours persistence-based models.

The Random Forest's most important features are also volatility persistence features, especially current realised volatility, 30-day rolling return standard deviation, and recent realised-volatility lags. This is useful for interpretability because it shows that the model is mainly learning continuity in volatility rather than discovering a completely new nonlinear structure.

The implemented LSTM performs better than the Random Forest but still remains behind the lagged linear regression and rolling benchmark. This suggests that sequence modelling does capture some useful structure, but not enough to overturn the main conclusion. The result is still valuable because it means the project now compares both a tree-based and a recurrent machine-learning model against the simpler alternatives.

GARCH(1,1) underperforms in this first pass. One possible reason is that GARCH estimates a conditional daily return variance, while the project target is a next-day 30-day realised-volatility estimate. The script converts the one-step GARCH variance into a 30-day realised-volatility forecast, but the result still appears less aligned with the rolling target than direct lag-based models.

## Evidence Files

- `code/outputs/model_performance.csv`
- `code/outputs/model_predictions.csv`
- `code/outputs/random_forest_feature_importance.csv`
- `code/outputs/garch_parameters.json`
- `code/outputs/lstm_training_summary.json`
- `code/outputs/volatility_forecast_comparison.png`
- `code/outputs/model_summary.md`

## Next Close-Out Steps

1. Fold the refreshed metrics into the main report sections.
2. Use the implemented LSTM result in the comparative analysis rather than treating it as only future work.
3. If time allows, run one small robustness check such as a different realised-volatility window.
4. Convert the current findings into presentation slides and final production-log commentary.
