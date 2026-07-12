# Methodology Draft

## Data Source and Scope

The project uses Hyperliquid BTC daily perpetual-futures candles from the public information API. The raw archive is stored in `data/raw/hyperliquid_BTC_1d_candles.csv`, with request details in `data/raw/hyperliquid_BTC_1d_metadata.json`. The latest refresh requested on 2026-07-13 returned 1,233 daily candles from 2023-02-26 through 2026-07-12. Earlier API rows were excluded because they reported zero volume and trade count and therefore did not represent the same active exchange market.

The candle fields are open, high, low, close, volume, and trade count. Closing price is used to create one consistent return observation per day. Hyperliquid was selected instead of Yahoo Finance because it provides exchange-level data for the BTC perpetual-futures market actually studied. This also limits generalisation: the sample is not identical to Bitcoin spot data from another exchange.

## Returns and Volatility Targets

Daily logarithmic return is:

```text
r_t = ln(P_t / P_{t-1})
```

The primary realised-volatility proxy is the sample standard deviation of the latest 30 daily log returns:

```text
RV_t(30) = stdev(r_{t-29}, ..., r_t)
```

The forecasting target attached to information date `t` is `RV_(t+1)`. Features at date `t` therefore forecast the next day's updated rolling-volatility value. Values are not annualised. A 14-day version is calculated from the same return series for robustness testing. Daily rolling volatility is an observable proxy for latent volatility, not a high-frequency realised-variance measure.

## Features

The feature-based models use current realised volatility; current and lagged log returns; absolute returns; lagged realised volatility at 1, 2, 3, 7, and 14 days; log-transformed volume and trade count; and 7-day, 14-day, and 30-day rolling return summaries. Log transforms reduce the scale difference in activity variables. Model inputs are standardised using means and standard deviations estimated only from the training period. Test information is not used to fit the scaler.

For the 14-day robustness run, the current realised-volatility input and target are replaced with their 14-day versions. The remaining market and rolling-summary features, model settings, random seed, and chronological split rule remain unchanged.

## Validation Design

The modelling frame is split once in chronological order: the earliest 80% is used for fitting and the latest 20% for out-of-sample evaluation. The primary 30-day frame contains 1,188 observations, with 950 training rows from 2023-04-11 to 2025-11-15 and 238 test rows from 2025-11-16 to 2026-07-11.

This is a fixed chronological holdout, not a random split and not a walk-forward refitting procedure. It prevents future rows from entering model fitting while keeping the project computationally manageable. Within the training period, LSTM reserves the final 15% of available training sequences as a chronological validation segment for early stopping. The validation segment is not the final test set.

The 14-day frame begins earlier because its rolling target needs fewer initial observations. It contains training observations from 2023-03-28 to 2025-11-12 and test observations from 2025-11-13 to 2026-07-11. The slight date difference is reported in the robustness output rather than hidden.

## Models

### Rolling Historical Volatility

The benchmark predicts that tomorrow's rolling realised volatility equals today's. It has no fitted parameters and directly tests whether a complex model can improve on volatility persistence.

### GARCH(1,1)

GARCH conditional variance is:

```text
sigma_t^2 = omega + alpha * epsilon_(t-1)^2 + beta * sigma_(t-1)^2
```

`omega` represents baseline variance, `alpha` the reaction to recent return shocks, and `beta` variance persistence. Parameters are selected through deterministic coarse-to-fine grid-search maximum likelihood with variance targeting, using returns available through the training end date. For each information date, the one-step conditional-variance forecast is combined with the known recent returns to estimate the next rolling realised-volatility value. Forecasts are stored against source dates and mapped to test dates explicitly; missing or duplicate date mappings cause the run to fail.

### Lagged Linear Regression

The linear model uses a closed-form ridge-stabilised solution on standardised lagged and rolling features. The very small penalty improves numerical stability when related rolling features are correlated. All 26 feature coefficients plus the intercept are exported. Coefficients show association and direction on the standardised scale, but they are not causal effects.

### Random Forest

The Random Forest is a project-local regression implementation with 160 bootstrapped trees, maximum depth 7, minimum leaf size 10, random feature selection, and seed 42. It captures nonlinear splits and interactions. Impurity-reduction feature importance is exported as global explanation evidence. This measure does not identify causal direction or fully explain an individual prediction.

### LSTM

The PyTorch LSTM receives rolling 30-observation sequences of nine market and volatility features. It contains one recurrent layer with 32 hidden units followed by a small regression head. Adam optimisation, target scaling, weight decay, chronological validation, and early stopping are used to limit overfitting. The trained primary model contains 6,049 trainable parameters. Its architecture and training history are reproducible evidence, but they do not make its hidden-state reasoning directly interpretable.

## Evaluation Framework

Accuracy is measured on the untouched chronological test period using:

```text
MAE = mean(|y_t - yhat_t|)
MSE = mean((y_t - yhat_t)^2)
RMSE = sqrt(MSE)
```

MAE describes average absolute error, while RMSE gives greater weight to large misses. Results are also expressed relative to the rolling benchmark's RMSE so that the practical size of an improvement is visible.

Interpretability is assessed using model-specific evidence rather than an artificial universal score: the rolling rule, GARCH parameters, linear coefficients, Random Forest feature importance, and documented LSTM structure and limitations. The exported comparison labels interpretability as high, medium, or low and explains the evidence and limitation behind each label.

Computational practicality is measured using local fit and prediction time from the same pipeline run. Structural scale is reported as fitted parameters, coefficients, tree nodes, or trainable neural-network parameters. These units are not directly interchangeable and the timing is hardware-dependent, so the values support comparison within this project rather than universal claims about algorithm speed.

Robustness is assessed by rerunning all five models for both 14-day and 30-day realised-volatility targets and comparing rank and RMSE relative to the rolling benchmark. This is a target-definition check, not a complete regime-stability or multi-market study.

## Reproducibility and Evidence

The code is organised under `code/epq_pipeline/` into data, features, models, reporting, and pipeline layers. Generated evidence includes predictions, performance metrics, coefficients, feature importance, GARCH parameters, LSTM history, computational profiles, the multi-dimensional comparison, robustness results, run metadata, and a chart. Unit tests cover data processing, time splitting, scaling, sequence creation, metrics, model structure, output metadata, and strict forecast-date alignment.
