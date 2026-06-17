# A-level EPQ Project

## Working Direction

**Refined research question:**
To what extent can machine learning models, specifically Random Forest and Long Short-Term Memory networks, improve Bitcoin volatility forecasting compared with traditional statistical models such as rolling historical volatility and GARCH(1,1)?

## Project Aim

This project investigates whether machine learning models can produce more accurate and practically useful forecasts of cryptocurrency volatility than traditional statistical approaches. The comparison will not be based only on error metrics: it will also consider interpretability, computational practicality, and suitability for a small-scale EPQ investigation.

## Current Scope

- Main asset: Bitcoin perpetual futures (Hyperliquid BTC)
- Data source: Hyperliquid public info API daily OHLCV candles
- Reference Hyperliquid address for optional user/account metadata: `0x28e81E9fAC95AC1fae40870E4C08E6b94FcB1C23`
- Current downloaded sample: 2023-02-26 to 2026-06-17
- Optional extension: Ethereum, only if the Bitcoin workflow is completed early
- Baseline model: rolling historical volatility
- Traditional statistical model: GARCH(1,1)
- Machine learning models: Random Forest regression and LSTM
- Primary accuracy metrics: MAE, RMSE, and MSE on realised volatility forecasts
- Wider comparison dimensions: accuracy, interpretability, computational practicality, and usefulness for risk-management decisions

## Current Mid-Project Position

The project has moved from a broad "machine learning versus statistics" idea into a more controlled comparison. The main adjustment is that the final discussion will avoid a simplistic "best model wins" structure. Instead, it will ask whether any accuracy gain from machine learning is large enough to justify weaker interpretability and higher implementation cost.

The planned report structure is:

1. Introduction
2. Literature Review
3. Mathematical Formulation
4. Methodology and Data Source
5. Results
6. Comparative Analysis and Discussion
7. Conclusion

## Folder Structure

```text
EPQ/
  production-log/   Official EPQ forms and process records
  report/           5000-word written report drafts and outline
  research/         Sources, literature notes, and search log
  data/             Raw and processed cryptocurrency price data
  code/             Data analysis and model comparison scripts/notebooks
  appendix/         Timetable, risk assessment, extra charts, model outputs
  presentation/     Slides and presentation planning materials
```

## Submission Components

- Written report: 4500-5500 words
- Production log
- Presentation: 10 minutes delivery plus 5 minutes Q&A
- Appendix: timetable, risk assessment, data/code evidence, extra results
