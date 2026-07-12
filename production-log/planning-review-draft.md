# Planning Review Draft

## Progress So Far

The project has moved from a broad interest in cryptocurrency prediction to a more focused investigation of Bitcoin volatility forecasting. The research question has been refined so that the comparison is between rolling historical volatility, GARCH(1,1), Random Forest, and LSTM.

Initial research has identified three important points:

1. GARCH(1,1) is a serious benchmark for volatility forecasting, not just a simple old model.
2. Machine learning models can improve Bitcoin or cryptocurrency volatility forecasts in some studies, but the evidence is not uniform across every asset, horizon, or metric.
3. Interpretability and practicality need to be included in the final comparison, because an accurate but opaque model may not be the most useful result for risk management.

## Current Plan

The project will use Hyperliquid daily BTC perpetual futures candle data. The data will be converted into logarithmic returns and a rolling realised volatility target. The first modelling stage will implement rolling historical volatility and GARCH(1,1). The second modelling stage will add Random Forest and LSTM.

The final comparison will use:

- MAE
- MSE
- RMSE
- interpretability notes
- computational practicality notes
- risk-management usefulness discussion

## Changes Made Since Initial Idea

| Original idea | Revised plan | Reason for change |
| --- | --- | --- |
| Compare machine learning and traditional models mainly by accuracy | Compare accuracy, interpretability, practicality, and usefulness | Supervisor feedback suggested the original comparison was too linear |
| Possibly include several cryptocurrencies | Focus on Bitcoin first, Ethereum optional | Keeps the project feasible |
| Use a broad machine learning category | Specify Random Forest and LSTM | Makes the research question testable |
| Treat GARCH as one baseline | Use rolling volatility as baseline and GARCH(1,1) as the main statistical model | Gives a fairer comparison |

## Next Steps

1. Download Hyperliquid BTC candle data and save the raw file.
2. Create a cleaned dataset with log returns and rolling realised volatility.
3. Implement rolling historical volatility and GARCH(1,1).
4. Build a Random Forest model with lagged return/volatility features.
5. Attempt a small LSTM only after the baseline workflow is stable.
6. Export tables and charts for the report.

## Evidence To Keep

- Source evaluation workbook
- Literature notes and search log
- Cleaned data file
- Notebook/script outputs
- Performance comparison table
- Example forecast chart
- Planning and mid-project review drafts

## Status Note After Refresh (2026-07-13)

These planned steps have largely been completed in first-pass form. The main remaining work is now close-out work rather than pipeline creation: integrate the refreshed outputs into the full report, use the implemented LSTM result in the final comparison, and complete presentation and production-log evidence.
