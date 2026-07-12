# Conclusion Draft

This project asked how Random Forest and LSTM compare with rolling historical volatility and GARCH(1,1) when Bitcoin volatility forecasts are evaluated by accuracy, interpretability, computational practicality, and robustness.

For the primary next-day 30-day realised-volatility target, GARCH(1,1) produces the lowest RMSE (`0.00099637`) and MAE (`0.00047808`). It also ranks first for the alternative 14-day target, with RMSE `0.00179214`. Lagged linear regression and rolling historical volatility rank second and third at both windows. LSTM performs better than Random Forest, but both machine-learning models remain behind the statistical and interpretable alternatives.

The answer is therefore that machine learning does not provide the best overall trade-off in this implementation. GARCH combines the strongest tested accuracy with three interpretable parameters and moderate local fitting time. Rolling historical volatility is even simpler, while lagged linear regression provides auditable coefficients. LSTM and Random Forest add nonlinear or sequential capacity, but their lower interpretability and much larger fitted structures are not compensated by an accuracy improvement.

This conclusion is bounded rather than universal. The study uses daily Hyperliquid BTC perpetual-futures candles, one chronological holdout, and 14-day and 30-day realised-volatility proxies. Intraday data, sentiment features, alternative hyperparameters, other market regimes, or walk-forward refitting could change the ranking. The defensible conclusion is not that machine learning can never work, but that it has not justified its additional complexity under the conditions tested here.

The method audit also became part of the project's value. Correcting GARCH forecasts from row-index selection to strict date alignment changed the ranking and demonstrated why reproducibility checks matter. The final project is therefore stronger as a critical evaluation: it records not only which model won, but how the result was validated and why the wider trade-off matters.
