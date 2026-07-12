# Conclusion Draft

This project set out to test whether machine learning models, specifically Random Forest and LSTM, could improve Bitcoin volatility forecasting compared with traditional statistical models such as rolling historical volatility and GARCH(1,1). Based on the current Hyperliquid BTC daily dataset and the refreshed first-pass modelling results, the answer is limited rather than strongly positive.

The best current RMSE is produced by lagged linear regression, with rolling historical volatility very close behind. Random Forest does not outperform these simpler models, and GARCH(1,1) performs worst on the current realised-volatility target. This means the project does not currently support the claim that machine learning automatically improves Bitcoin volatility forecasting.

The wider conclusion is more important than the ranking alone. For this project, model complexity has not yet produced a large enough gain to justify reduced interpretability and extra implementation cost. Simpler persistence-based or lag-feature models remain highly competitive, which suggests that practical usefulness and explainability should be weighed alongside accuracy.

This does not mean machine learning is ineffective in all settings. The literature shows that neural networks and other advanced models can outperform traditional approaches when the data, features, target definition, and tuning are more favourable. However, the current EPQ evidence suggests that for a small-scale, transparent, and reproducible daily-volatility study, the advantage of machine learning is not strong enough to be treated as proven.

The most defensible final answer is therefore that machine learning can improve Bitcoin volatility forecasting in some circumstances, but in this project's current implementation it has not clearly surpassed simpler alternatives. Future improvements could include a different realised-volatility window, richer explanatory features, or more extensive tuning of the implemented LSTM, but these should be treated as extensions rather than assumptions.
