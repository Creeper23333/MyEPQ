# Model Selection and Evaluation Plan

## Final Core Models

| Model | Role in project | Reason for inclusion | Main limitation |
| --- | --- | --- | --- |
| Rolling historical volatility | Naive benchmark | Simple, transparent, easy to reproduce | Assumes recent past volatility is enough to predict near future volatility |
| GARCH(1,1) | Traditional statistical model | Standard volatility model; captures volatility clustering | Assumes a specific conditional variance structure |
| Random Forest regression | First machine learning model | Captures non-linear relationships and provides feature importance | Does not naturally model sequence order unless lagged features are engineered |
| LSTM | Deep learning model | Designed for sequential data and long-term dependencies | Harder to interpret and more likely to overfit in a small project |

## Baseline Decision

The baseline should be rolling historical volatility, because it gives a transparent minimum standard: if a complex model cannot beat a simple rolling-window forecast, it is not useful for the project. GARCH(1,1) should be treated as the main traditional statistical model, not merely as a baseline, because it is theoretically designed for conditional volatility.

## Forecast Target

The project will forecast realised volatility calculated from Hyperliquid Bitcoin perpetual futures log returns. Because the project uses daily OHLCV candles, realised volatility will be an estimated proxy rather than the true unobservable volatility. This limitation should be discussed in the methodology and evaluation.

## Validation Plan

Use a chronological split or walk-forward validation. Do not use a random train-test split because that would mix future and past observations.

Recommended first version:

1. Download Hyperliquid BTC daily candles with the public `candleSnapshot` info endpoint.
2. Calculate daily log returns.
3. Calculate rolling realised volatility using a 30-day window.
4. Use earlier observations for training and later observations for testing.
5. Forecast one-step-ahead realised volatility.
6. Compare predictions using MAE, MSE, and RMSE.

## Comparison Dimensions

| Dimension | How it will be assessed | Why it matters |
| --- | --- | --- |
| Accuracy | MAE, MSE, RMSE | Directly answers whether forecasts are closer to realised volatility |
| Interpretability | Can the model's reasoning be explained clearly? | Important for critical evaluation and risk-management trust |
| Computational practicality | Time and difficulty to fit/tune/reproduce | Important because the EPQ is small-scale |
| Robustness | Whether performance is stable across time periods | Crypto markets change rapidly |
| Practical usefulness | Whether the forecast would affect a risk decision | Prevents the project from becoming only a metrics exercise |

## Expected Critical Discussion

The final report should avoid assuming that the most complex model is best. A possible final conclusion could be:

> Machine learning may improve Bitcoin volatility forecasting accuracy, but the improvement must be large and stable enough to justify reduced interpretability and higher implementation cost. If the advantage is small, GARCH(1,1) or rolling historical volatility may remain more practical.
