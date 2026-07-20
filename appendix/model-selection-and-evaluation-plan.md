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

Use a frozen forecast-origin cutoff of 2025-11-16 as the primary design. It was initially selected near an 80/20 boundary, but it remains fixed when new rows are appended so old test observations never move into training. Do not use a random split because that would mix future and past observations. Supplement the primary result with four expanding-window rolling-origin folds; this block-level refitting is implemented, but it must not be described as daily online retraining.

Recommended implemented version:

1. Download Hyperliquid BTC daily candles with the public `candleSnapshot` info endpoint.
2. Calculate daily log returns.
3. Calculate rolling realised volatility using a 30-day window.
4. Use earlier observations for training and later observations for testing.
5. Forecast one-step-ahead realised volatility.
6. Compare predictions using MAE, MSE, and RMSE across rolling historical volatility, GARCH(1,1), lagged linear regression, Random Forest, and LSTM.
7. Record fit time, prediction time, model size, and model-specific explanation evidence.
8. Repeat the full comparison for 14-day and 30-day realised-volatility targets.
9. Split the 30-day target test period into two equal chronological halves and compare ranking stability.
10. Use a paired circular 30-day moving-block bootstrap to estimate uncertainty in each model's RMSE difference relative to rolling historical volatility.
11. Split the primary target into low-, medium-, and high-volatility terciles and record RMSE plus mean bias within each regime.
12. Run four expanding-window rolling-origin folds and export both fold-level and concatenated performance.
13. Export Random Forest OOB coverage/RMSE and repeated holdout permutation importance alongside impurity importance.
14. Rerun the LSTM with seeds 7, 42, and 101 to check whether its conclusion depends on one initialisation.
15. Dynamically remove the rolling-return standard deviation that is identical to the active realised-volatility predictor.
16. Estimate the primary GARCH standard-deviation target as `E[s]` with 80-point Gauss-Hermite quadrature, while retaining `sqrt(E[s^2])` as a reported sensitivity.
17. Re-run the current method on an earlier data cut to distinguish new-data sensitivity from code-version changes.

## Comparison Dimensions

| Dimension | How it will be assessed | Why it matters |
| --- | --- | --- |
| Accuracy | MAE, MSE, RMSE | Directly answers whether forecasts are closer to realised volatility |
| Interpretability | Can the model's reasoning be explained clearly? | Important for critical evaluation and risk-management trust |
| Computational practicality | Time and difficulty to fit/tune/reproduce | Important because the EPQ is small-scale |
| Robustness | Whether rankings persist across 14/30-day targets, both test halves, four expanding-window folds and three target-volatility regimes; paired moving-block bootstrap interval versus rolling | Crypto markets change rapidly, and one point estimate can overstate confidence |
| Model diagnostics | RF OOB versus chronological-test error, RF permutation importance and LSTM multi-seed stability | Distinguishes training-period fit, cross-period generalisation, feature dependence and optimisation randomness |
| Practical usefulness | Whether the forecast would affect a risk decision | Prevents the project from becoming only a metrics exercise |

## Current Critical Direction

The corrected and robustness-tested results support a critical close-out. The report should avoid assuming that the most complex model is best. The current most defensible conclusion is:

> For the tested Hyperliquid BTC daily-volatility targets, GARCH(1,1) provides the strongest accuracy at both 14 and 30 days, in both halves of the 30-day test period, in all four expanding-window test folds and across low-, medium-, and high-volatility target regimes, while retaining a compact interpretable structure. Its advantage over the rolling benchmark also remains below zero across the paired moving-block bootstrap interval. Random Forest and LSTM do not deliver an accuracy gain that justifies their extra structural complexity in this implementation.
