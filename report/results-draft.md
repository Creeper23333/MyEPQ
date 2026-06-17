# Results Draft

## First-Pass Result Table

| Rank | Model | Category | MAE | MSE | RMSE |
| --- | --- | --- | --- | --- | --- |
| 1 | Lagged linear regression | Interpretable lag-feature model | 0.00076728 | 0.00000208 | 0.00144239 |
| 2 | Rolling historical volatility | Benchmark | 0.00065181 | 0.00000215 | 0.00146692 |
| 3 | Random Forest | Machine learning | 0.00127180 | 0.00000469 | 0.00216639 |
| 4 | GARCH(1,1) | Traditional statistical | 0.01021477 | 0.00017326 | 0.01316280 |

The first-pass results do not support a simple claim that machine learning improves Bitcoin volatility forecasting. The lowest RMSE is achieved by lagged linear regression, while rolling historical volatility is extremely close. Random Forest, the first machine learning model, performs worse than both simpler lag-based models.

## Accuracy Discussion

The rolling benchmark performs strongly because the forecast target is itself based on a rolling volatility measure. If volatility is persistent, today's 30-day realised volatility will naturally be a strong predictor of tomorrow's 30-day realised volatility. This means that beating the benchmark is difficult, and small differences in RMSE should not be overinterpreted.

Lagged linear regression slightly improves RMSE compared with rolling historical volatility, but its MAE is slightly worse. This mixed result means it is not enough to claim that the linear model is simply "best"; the conclusion depends on which error metric is prioritised.

Random Forest underperforms in this first run. This may be because the model is currently a lightweight implementation and has not been tuned extensively. It may also suggest that the relationship between lagged volatility and next-day realised volatility is already captured by simple persistence models.

GARCH(1,1) performs worst in this first pass. One reason may be that GARCH forecasts conditional daily variance, while the evaluation target is next-day 30-day realised volatility. Although the script converts the GARCH forecast into a 30-day realised-volatility estimate, this conversion may still not match the rolling target as directly as lag-based models do.

## Interpretability Discussion

The results strengthen the interpretability side of the project. Rolling historical volatility is the easiest model to explain and nearly matches the best RMSE. Lagged linear regression is also relatively interpretable because it uses explicit lagged features. Random Forest is less transparent, although feature importance shows that it mainly relies on volatility persistence features such as 30-day rolling return standard deviation and recent realised-volatility lags.

## Provisional Conclusion

At this stage, the project should not conclude that machine learning improves volatility forecasting. A more defensible provisional conclusion is that simple persistence-based models are highly competitive for next-day 30-day realised volatility on this Hyperliquid BTC dataset. Machine learning may still become useful after tuning, adding richer features, or changing the forecast target, but the first-pass evidence does not justify claiming that it is superior.
