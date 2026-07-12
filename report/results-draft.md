# Results Draft

## First-Pass Result Table

| Rank | Model | Category | MAE | MSE | RMSE |
| --- | --- | --- | --- | --- | --- |
| 1 | Lagged linear regression | Interpretable lag-feature model | 0.00074798 | 0.00000201 | 0.00141843 |
| 2 | Rolling historical volatility | Benchmark | 0.00063564 | 0.00000209 | 0.00144481 |
| 3 | LSTM | Machine learning | 0.00106690 | 0.00000339 | 0.00184029 |
| 4 | Random Forest | Machine learning | 0.00121584 | 0.00000443 | 0.00210549 |
| 5 | GARCH(1,1) | Traditional statistical | 0.00987357 | 0.00016712 | 0.01292761 |

The first-pass results do not support a simple claim that machine learning improves Bitcoin volatility forecasting. The lowest RMSE is achieved by lagged linear regression, while rolling historical volatility is extremely close. The implemented LSTM performs better than the Random Forest, but it still does not beat the two strongest simple models.

## Accuracy Discussion

The rolling benchmark performs strongly because the forecast target is itself based on a rolling volatility measure. If volatility is persistent, today's 30-day realised volatility will naturally be a strong predictor of tomorrow's 30-day realised volatility. This means that beating the benchmark is difficult, and small differences in RMSE should not be overinterpreted.

Lagged linear regression slightly improves RMSE compared with rolling historical volatility, but its MAE is slightly worse. This mixed result means it is not enough to claim that the linear model is simply "best"; the conclusion depends on which error metric is prioritised.

The LSTM result is important because it shows that sequence modelling does add some value compared with the Random Forest. However, the improvement is not large enough to overturn the main result. The LSTM still underperforms compared with lagged linear regression and the rolling-volatility benchmark, which suggests that the strongest predictive signal is still persistence in recent realised volatility.

Random Forest underperforms in this refreshed run. This may be because the model is currently a lightweight implementation and has not been tuned extensively. It may also suggest that the relationship between lagged volatility and next-day realised volatility is already captured by simple persistence models.

GARCH(1,1) performs worst in this first pass. One reason may be that GARCH forecasts conditional daily variance, while the evaluation target is next-day 30-day realised volatility. Although the script converts the GARCH forecast into a 30-day realised-volatility estimate, this conversion may still not match the rolling target as directly as lag-based models do.

## Interpretability Discussion

The results strengthen the interpretability side of the project. Rolling historical volatility is the easiest model to explain and nearly matches the best RMSE. Lagged linear regression is also relatively interpretable because it uses explicit lagged features. Random Forest is less transparent, although feature importance shows that it mainly relies on volatility persistence features such as 30-day rolling return standard deviation and recent realised-volatility lags. The LSTM is even harder to interpret directly, which makes its remaining performance gap relative to the best simple models especially important.

## Provisional Conclusion

At this stage, the project should not conclude that machine learning improves volatility forecasting. A more defensible provisional conclusion is that simple persistence-based models are highly competitive for next-day 30-day realised volatility on this Hyperliquid BTC dataset. Machine learning may still become useful after tuning, adding richer features, or changing the forecast target, but the first-pass evidence does not justify claiming that it is superior.

## Close-Out Direction

The most efficient close-out path is to build the final report around this critical result rather than to keep expanding model complexity further. Because the LSTM is now implemented, the report can discuss both a tree-based and a recurrent machine-learning model while still defending the conclusion that greater complexity did not yet produce the best overall forecast.
