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
- Current data request window: 2023-02-26 to 2026-07-13
- Latest daily candle returned by the API in the 2026-07-13 refresh: 2026-07-12
- Optional extension: Ethereum, only if the Bitcoin workflow is completed early
- Baseline model: rolling historical volatility
- Traditional statistical model: GARCH(1,1)
- Current implemented comparison models: lagged linear regression, Random Forest regression, LSTM, rolling historical volatility, and GARCH(1,1)
- Primary accuracy metrics: MAE, RMSE, and MSE on realised volatility forecasts
- Wider comparison dimensions: accuracy, interpretability, computational practicality, and usefulness for risk-management decisions

## Current Project Position

As of 2026-07-13, the project has moved from a broad "machine learning versus statistics" idea into a controlled Bitcoin volatility-forecasting comparison with reproducible data and model outputs. The main adjustment is that the final discussion will avoid a simplistic "best model wins" structure. Instead, it asks whether any accuracy gain from machine learning is large enough to justify weaker interpretability and higher implementation cost.

The current data-and-model pipeline has been refreshed and expanded with an implemented LSTM. The latest run uses 1233 raw daily candles through 2026-07-12, produces a modelling frame of 1188 rows, and evaluates a chronological 80/20 split from 2023-04-11 to 2026-07-11.

The main current result is that machine learning still has not produced a decisive advantage over the best simple models, although the implemented LSTM improves on the Random Forest. The current RMSE ranking is:

- Lagged linear regression: `0.00141843`
- Rolling historical volatility: `0.00144481`
- LSTM: `0.00184029`
- Random Forest: `0.00210549`
- GARCH(1,1): `0.01292761`

This strengthens the critical direction of the EPQ: simple persistence-based or interpretable lag-feature models remain highly competitive for this target, while more complex machine-learning models need a clear and stable benefit to justify their extra implementation cost.

The planned report structure is:

1. Introduction
2. Literature Review
3. Mathematical Formulation
4. Methodology and Data Source
5. Results
6. Comparative Analysis and Discussion
7. Conclusion

Draft material now exists for each main report section, with research notes and appendix evidence supporting the final write-up.

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

## Immediate Close-Out Tasks

1. Fold the refreshed model results, including the LSTM comparison, into the formal written report.
2. Transfer the latest daily log and milestone notes into the official `production-log/Form.docx`.
3. Build the final presentation slides and keep evidence of the presentation and Q&A.
