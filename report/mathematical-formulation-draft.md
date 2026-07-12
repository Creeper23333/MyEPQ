# Mathematical Formulation Draft

This section defines the main quantities used in the project so that the forecasting task is mathematically clear.

## Logarithmic Return

Daily logarithmic return is defined as:

```text
r_t = ln(P_t / P_{t-1})
```

where `P_t` is the closing price on day `t`. Logarithmic returns are used because they are standard in financial modelling and make percentage-style changes easier to work with across time.

## Realised Volatility Proxy

The project uses a 30-day rolling standard deviation of daily log returns as a proxy for realised volatility:

```text
RV_t = stdev(r_{t-29}, r_{t-28}, ..., r_t)
```

This is not the true latent volatility of Bitcoin. Instead, it is an observable proxy calculated from daily returns. That limitation is important and should be discussed when evaluating forecast quality.

## Forecast Target

The models do not forecast the current value of realised volatility. They forecast the next day's realised volatility:

```text
y_t = RV_{t+1}
```

This shift is necessary so that the models use information available at day `t` to forecast a future volatility value rather than reproducing the present one.

## GARCH(1,1)

The traditional statistical model uses the standard GARCH(1,1) variance equation:

```text
sigma_t^2 = omega + alpha * epsilon_{t-1}^2 + beta * sigma_{t-1}^2
```

Here, `sigma_t^2` is the conditional variance, `epsilon_{t-1}` is the previous return shock, and `omega`, `alpha`, and `beta` are model parameters. In this project, the fitted one-step-ahead variance is converted into a 30-day realised-volatility-style forecast so that it can be compared with the other models on the same target.

## Error Metrics

Forecast accuracy is evaluated using:

```text
MAE = mean(|y_t - yhat_t|)
MSE = mean((y_t - yhat_t)^2)
RMSE = sqrt(MSE)
```

MAE shows the average absolute size of the forecast error. MSE and RMSE penalise larger misses more strongly, which is useful when volatility changes sharply.
