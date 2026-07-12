# Methodology Draft

## Data Source

The project uses Hyperliquid BTC daily perpetual futures candles from the public information API. The raw data is stored in `data/raw/hyperliquid_BTC_1d_candles.csv`, and metadata about the request is stored in `data/raw/hyperliquid_BTC_1d_metadata.json`. In the refreshed pull requested on 2026-07-13, the API returned daily candles from 2023-02-26 to the latest available daily candle on 2026-07-12. The start date was chosen because candles before 2023-02-26 returned zero volume and zero trade count in the API pull, making them less suitable as exchange trading data.

The public candle data includes open, high, low, close, volume, and trade count. The modelling uses the close price because it provides one price per day and allows a consistent daily return series.

## Data Processing

Daily logarithmic returns are calculated as:

```text
r_t = ln(P_t / P_{t-1})
```

where `P_t` is the daily close price. Realised volatility is estimated using a 30-day rolling standard deviation of log returns. This produces a volatility target that is simple to calculate and easy to explain, although it is only a proxy for true latent volatility.

The forecast target is next-day 30-day realised volatility. This means that the models use information available at day `t` to forecast the realised volatility value at day `t + 1`.

## Code Architecture

The analysis code is now organised as a packaged workflow under `code/epq_pipeline/` rather than as large monolithic scripts. The main layers are:

- `data/` for Hyperliquid API access and dataset construction
- `features/` for lagged features, rolling summaries, scaling, and LSTM sequence creation
- `models/` for GARCH(1,1), lagged linear regression, Random Forest, LSTM, and evaluation metrics
- `reporting/` for markdown summaries, run metadata, and chart exports
- `pipeline/` for the command-level entry points that run the data refresh and model comparison

This structure improves reproducibility because each stage of the workflow can be tested, refreshed, and explained separately.

## Validation Design

The data is split chronologically rather than randomly. This avoids training on future information and better reflects a real forecasting task.

In the refreshed first-pass model run:

- Training period: 2023-04-11 to 2025-11-15.
- Test period: 2025-11-16 to 2026-07-11.
- Model frame rows: 1188.
- Training rows: 950.
- Test rows: 238.

## Models

### Rolling Historical Volatility

The rolling-volatility benchmark predicts that tomorrow's realised volatility will equal today's 30-day realised volatility. This is a simple persistence model and provides a transparent baseline.

### GARCH(1,1)

GARCH(1,1) models conditional return variance using the formula:

```text
sigma_t^2 = omega + alpha * epsilon_{t-1}^2 + beta * sigma_{t-1}^2
```

In the first-pass implementation, the GARCH parameters are fitted using grid-search maximum likelihood with variance targeting. The one-step-ahead conditional variance is then converted into a 30-day realised-volatility forecast using the most recent 29 observed returns plus the forecast next-day variance.

### Lagged Linear Regression

A lagged linear regression is included as an interpretable comparison model. It uses lagged returns, absolute returns, realised-volatility lags, volume, trade count, and rolling summary features. It helps test whether a simple feature-based model can compete with more complex models.

### Random Forest

The first-pass Random Forest is a lightweight in-repo implementation because the current Python environment does not include scikit-learn. It uses bootstrapped regression trees with random feature selection. This provides a machine-learning comparison while keeping the project reproducible in the current environment.

### LSTM

The LSTM is implemented using PyTorch in a project-local virtual environment. It uses rolling 30-day sequences of core market features, including realised volatility, returns, volume-related features, and rolling return summaries. In the current version, the network uses a single LSTM layer with 32 hidden units followed by a small regression head. Training uses a chronological validation split, Adam optimisation, and early stopping so that the model remains small and reproducible rather than being heavily tuned.

## Exported Evidence

The current pipeline exports more than the final ranking table. It also saves Random Forest feature importance, linear-regression coefficients, GARCH parameter estimates, LSTM training history, LSTM training metadata, a model-run metadata manifest, and a forecast-comparison figure. This makes the results section and appendix easier to justify with direct evidence.

## Evaluation Metrics

The models are evaluated using:

```text
MAE = mean(|y_t - yhat_t|)
MSE = mean((y_t - yhat_t)^2)
RMSE = sqrt(MSE)
```

MAE is easier to interpret because it reports average absolute forecast error. RMSE penalises larger errors more strongly, which is useful when volatility forecasts miss sudden changes.
