# Model Selection and Evaluation Plan

## Current Core Comparison

| Model | Role in project | Reason for inclusion | Main limitation |
| --- | --- | --- | --- |
| Rolling historical volatility | Naive benchmark | Simple, transparent, easy to reproduce | Assumes recent past volatility is enough to predict near future volatility |
| GARCH(1,1) | Traditional statistical model | Standard volatility model; captures volatility clustering | Assumes a specific conditional variance structure |
| Lagged linear regression | Interpretable feature-based comparison | Tests whether simple lagged features already explain most of the target | Still depends on engineered persistence features |
| Random Forest regression | First machine learning model | Captures non-linear relationships and provides feature importance | Does not naturally model sequence order unless lagged features are engineered |
| LSTM | Sequence-based machine learning model | Uses rolling sequences of core market features to test whether recurrent learning adds value | Harder to interpret and more time-consuming to train than the simpler models |

## Baseline Decision

The baseline should be rolling historical volatility, because it gives a transparent minimum standard: if a complex model cannot beat a simple rolling-window forecast, it is not useful for the project. GARCH(1,1) should be treated as the main traditional statistical model, not merely as a baseline, because it is theoretically designed for conditional volatility.

## Forecast Target

The project will forecast realised volatility calculated from Hyperliquid Bitcoin perpetual futures log returns. Because the project uses daily OHLCV candles, realised volatility will be an estimated proxy rather than the true unobservable volatility. This limitation should be discussed in the methodology and evaluation.

## Validation Plan

Use a chronological split or walk-forward validation. Do not use a random train-test split because that would mix future and past observations.

Recommended implemented version:

1. Download Hyperliquid BTC daily candles with the public `candleSnapshot` info endpoint.
2. Calculate daily log returns.
3. Calculate rolling realised volatility using a 30-day window.
4. Use earlier observations for training and later observations for testing.
5. Forecast one-step-ahead realised volatility.
6. Compare predictions using MAE, MSE, and RMSE across rolling historical volatility, GARCH(1,1), lagged linear regression, Random Forest, and LSTM.

## Comparison Dimensions

| Dimension | How it will be assessed | Why it matters |
| --- | --- | --- |
| Accuracy | MAE, MSE, RMSE | Directly answers whether forecasts are closer to realised volatility |
| Interpretability | Can the model's reasoning be explained clearly? | Important for critical evaluation and risk-management trust |
| Computational practicality | Time and difficulty to fit/tune/reproduce | Important because the EPQ is small-scale |
| Robustness | Whether performance is stable across time periods | Crypto markets change rapidly |
| Practical usefulness | Whether the forecast would affect a risk decision | Prevents the project from becoming only a metrics exercise |

## Current Critical Direction

The refreshed first-pass results support a more critical close-out. The report should avoid assuming that the most complex model is best. The current most defensible conclusion is:

> For this Hyperliquid BTC daily-volatility target, simple persistence-based and interpretable lag-feature models remain highly competitive. The implemented LSTM improves on the Random Forest but still does not beat the strongest simple baselines, so machine learning should only be judged superior if it delivers a clear, stable improvement that justifies extra implementation complexity.
