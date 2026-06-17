# Code

This folder will contain the data analysis and model comparison work.

## Planned Workflow

1. Load Bitcoin price data from Hyperliquid.
2. Calculate log returns.
3. Calculate realised volatility.
4. Build benchmark model: rolling historical volatility.
5. Build traditional statistical model: GARCH(1,1).
6. Build machine learning model 1: Random Forest regression using lagged returns and lagged volatility features.
7. Build machine learning model 2: LSTM using a scaled rolling sequence of previous observations.
8. Compare models using MAE, MSE, and RMSE.
9. Record interpretability and computational practicality notes beside the error metrics.
10. Export tables and charts for the report and appendix.

## Possible Files

- `volatility_models.ipynb`: main notebook
- `fetch_hyperliquid_data.py`: downloads Hyperliquid BTC candles and prepares volatility data
- `requirements.txt`: Python packages
- `outputs/`: generated tables and figures

## Implementation Logic

The first implementation should stay deliberately simple:

1. Use Hyperliquid BTC daily perpetual futures candles from the public info API.
2. Calculate log returns as `ln(price_t / price_t-1)`.
3. Calculate 30-day rolling realised volatility from log returns.
4. Shift the realised volatility target forward by one day so the models forecast future volatility, not current volatility.
5. Create lag features such as previous returns, previous realised volatility, and rolling summary statistics.
6. Fit rolling volatility and GARCH(1,1) first.
7. Fit Random Forest after the statistical models, because it is easier to interpret than LSTM.
8. Fit a small LSTM last only if the cleaned dataset and baseline results are stable.
9. Use chronological validation only.
10. Save all outputs so the report can reproduce the results table.

## Hyperliquid Data Fetch

Run:

```bash
python3 code/fetch_hyperliquid_data.py
```

Default outputs:

- `data/raw/hyperliquid_BTC_1d_candles.csv`
- `data/raw/hyperliquid_BTC_1d_metadata.json`
- `data/processed/hyperliquid_BTC_1d_volatility.csv`

The script uses `POST https://api.hyperliquid.xyz/info` with `type: "candleSnapshot"`. The supplied address is used only for an optional `userRole` metadata check; public market candles do not require a user address.
