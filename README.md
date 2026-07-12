# A-level EPQ Project

## Working Direction

**Refined research question:**
How do Random Forest and Long Short-Term Memory networks compare with rolling historical volatility and GARCH(1,1) when forecasting Bitcoin volatility, in terms of accuracy, interpretability, computational practicality, and robustness?

## Project Aim

This project critically evaluates whether the additional complexity of machine-learning volatility forecasts is justified. It compares predictive error, explanation evidence, measured local runtime, model complexity, reproducibility, robustness across 14-day and 30-day targets, and suitability for risk-management interpretation.

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
- Wider comparison dimensions: accuracy, interpretability, computational practicality, robustness, reproducibility, and usefulness for risk-management decisions
- Validation: fixed chronological 80/20 holdout, with no random shuffling; LSTM early stopping uses a chronological validation segment inside the training period
- Robustness check: the full model set is rerun for 14-day and 30-day realised-volatility targets

## Current Project Position

As of 2026-07-13, the project has moved from a broad "machine learning versus statistics" idea into a controlled Bitcoin volatility-forecasting comparison with reproducible data and model outputs. The main adjustment is that the final discussion will avoid a simplistic "best model wins" structure. Instead, it asks whether any accuracy gain from machine learning is large enough to justify weaker interpretability and higher implementation cost.

The current data-and-model pipeline has been refreshed and expanded into a packaged code architecture under `code/epq_pipeline/`. The latest run uses 1233 raw daily candles through 2026-07-12, produces a modelling frame of 1188 rows, and evaluates a chronological 80/20 split from 2023-04-11 to 2026-07-11.

The latest method audit corrected GARCH forecast extraction so predictions are aligned to test observations by date after feature rows are removed. This materially changed the GARCH result and is recorded transparently because the earlier row-index alignment was not reliable. Machine learning still has not produced a decisive advantage. The corrected 30-day RMSE ranking is:

- GARCH(1,1): `0.00099637`
- Lagged linear regression: `0.00141843`
- Rolling historical volatility: `0.00144481`
- LSTM: `0.00184029`
- Random Forest: `0.00212715`

GARCH also ranks first for the 14-day target, where its RMSE is `0.00179214`. The robustness check therefore supports the statistical model rather than treating its 30-day result as a one-window accident. The critical conclusion remains that machine learning needs a clear benefit to justify reduced transparency and higher structural complexity, but the strongest comparator is now GARCH rather than lagged linear regression.

The planned report structure is:

1. Introduction
2. Literature Review
3. Mathematical Formulation
4. Methodology and Data Source
5. Results
6. Comparative Analysis and Discussion
7. Conclusion

Draft material now exists for each main report section, and a stitched full-report draft is now available in `report/full-report-draft.md`, with research notes and appendix evidence supporting the final write-up.

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

### Code Architecture

The analysis code is now split into package layers rather than large single scripts:

```text
code/
  epq_pipeline/
    common/     Shared IO and dataclasses
    data/       Hyperliquid API access and dataset construction
    features/   Feature engineering and sequence preparation
    models/     GARCH, linear regression, Random Forest, LSTM, metrics
    pipeline/   Command-level orchestration
    reporting/  Summary markdown, metadata JSON, and chart exports
  tests/        Unit tests
  outputs/      Generated tables, JSON files, and figures
```

## Submission Components

- Written report: 4500-5500 words
- Production log
- Presentation: 10 minutes delivery plus 5 minutes Q&A
- Appendix: timetable, risk assessment, data/code evidence, extra results

## Immediate Close-Out Tasks

1. Complete the final report using the corrected GARCH result and the new multi-dimensional evidence tables.
2. Transfer the latest daily log and milestone notes into the official `production-log/Form.docx`.
3. Build the final presentation slides and keep evidence of the presentation and Q&A.
