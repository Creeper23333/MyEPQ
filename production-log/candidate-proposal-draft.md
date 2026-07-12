# Candidate Proposal Draft

## Proposed Title

Accuracy, Interpretability and Practicality in Bitcoin Volatility Forecasting: Machine Learning versus Statistical Models

## Research Question

How do Random Forest and Long Short-Term Memory networks compare with rolling historical volatility and GARCH(1,1) when forecasting Bitcoin volatility, in terms of accuracy, interpretability, computational practicality, and robustness?

## Reason for Choosing This Topic

I chose this topic because cryptocurrency markets are known for large and sudden price movements, making volatility forecasting important for risk management. Bitcoin is a suitable focus because it is the most established cryptocurrency, and Hyperliquid provides exchange-level public OHLCV candle data for BTC perpetual futures. The project also allows me to combine mathematics, statistics, computing, and financial decision-making.

## Aim

To critically evaluate whether the additional complexity of Random Forest and LSTM is justified when compared with transparent statistical approaches for Bitcoin volatility forecasting.

## Objectives

1. Research the mathematical foundations of logarithmic returns, realised volatility, and GARCH-type volatility models.
2. Collect daily BTC candle data from Hyperliquid and convert it into log returns and a realised volatility target.
3. Implement rolling historical volatility and GARCH(1,1) as traditional statistical benchmarks.
4. Implement Random Forest regression and LSTM as machine learning models.
5. Compare model forecasts using MAE, MSE, and RMSE.
6. Evaluate whether any improvement in accuracy is meaningful once interpretability, computational complexity, and project scale are considered.
7. Test whether conclusions remain stable across 14-day and 30-day realised-volatility targets.
8. Use model-specific explanation evidence and measured local runtime rather than unsupported general claims about interpretability or efficiency.

## Planned Methodology

The project will use daily Bitcoin perpetual futures candle data from Hyperliquid. Prices will be cleaned and converted into logarithmic returns. Realised volatility will be estimated using a rolling window, most likely 30 days. The data will be split chronologically so that models are trained on earlier observations and tested on later observations.

The first model will be rolling historical volatility, which gives a transparent baseline. The second model will be GARCH(1,1), a standard statistical volatility model. The machine learning comparison will begin with Random Forest regression because it can model non-linear relationships while remaining more interpretable than a neural network. If time allows, an LSTM model will be implemented as the main deep learning model because it is designed for sequential data.

Forecasts will be evaluated using MAE, MSE, and RMSE. The final analysis will also compare interpretability and practicality, because a model with slightly lower error may not be better if it is difficult to explain or reproduce.

## Resources Needed

- Hyperliquid BTC perpetual futures OHLCV candle data.
- Academic sources on GARCH, Bitcoin volatility, Random Forests, LSTM, and model interpretability.
- Python or notebook environment for data cleaning and modelling.
- Spreadsheet source evaluation table for recording source reliability.
- Report drafts, production log notes, and appendix evidence.

## Ethical and Practical Considerations

The project uses public market data and does not involve human participants. The main practical risks are weak referencing, excessive scope, and overclaiming the results. The report must make clear that the project is educational and does not provide financial advice.

## Expected Product

The final product will be a written EPQ report supported by a modelling notebook or script, source evaluation table, charts, result tables, and a presentation. The report will answer whether machine learning improves Bitcoin volatility forecasting and whether the improvement is practically worthwhile.

## Retrospective Status Note (2026-07-13)

The project followed this proposal closely in topic and overall comparison logic. Since the proposal stage, LSTM has been implemented, Hyperliquid replaced the proposed generic Yahoo Finance source, and the evaluation expanded to measured computational evidence and a 14-day/30-day robustness check. A method audit also corrected GARCH date alignment. The final analysis can now compare tree-based, recurrent, benchmark, feature-based, and statistical models using reproducible outputs.
