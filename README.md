# A-level EPQ Project

## Working Direction

**Refined research question:**
How do Random Forest and Long Short-Term Memory networks compare with rolling historical volatility and GARCH(1,1) when forecasting Bitcoin volatility, in terms of accuracy, interpretability, computational practicality, and robustness?

## Project Aim

This project critically evaluates whether the additional complexity of machine-learning volatility forecasts is justified. It compares predictive error, explanation evidence, measured local runtime, model complexity, reproducibility, robustness across 14-day/30-day targets, test-period segments, four expanding-window folds and target-volatility regimes, bootstrap uncertainty, and suitability for risk-management interpretation.

## Current Scope

- Main asset: Bitcoin perpetual futures (Hyperliquid BTC)
- Data source: Hyperliquid public info API daily OHLCV candles
- Current data request window: 2023-02-26 to 2026-07-20
- Latest completed daily candle retained in the 2026-07-20 refresh: 2026-07-19
- Data-quality control: 1,241 rows were returned; one still-open daily candle was excluded by end timestamp, and all 1,240 retained rows passed schema, ordering, daily-cadence, symbol/interval, price, OHLC, volume and trade-count checks
- Optional extension: Ethereum, only if the Bitcoin workflow is completed early
- Baseline model: rolling historical volatility
- Traditional statistical model: GARCH(1,1)
- Current implemented comparison models: lagged linear regression, Random Forest regression, LSTM, rolling historical volatility, and GARCH(1,1)
- Primary accuracy metrics: MAE, RMSE, and MSE on realised volatility forecasts
- Wider comparison dimensions: accuracy, interpretability, computational practicality, robustness, reproducibility, and usefulness for risk-management decisions
- Validation: a frozen forecast-origin test cutoff at 2025-11-16 with no random shuffling, plus four expanding-window rolling-origin folds; later refreshes extend the test set without moving old test rows into training, and LSTM early stopping uses a chronological validation segment inside each training period
- Robustness and diagnostics: 14-day/30-day targets, two test-period halves, low/medium/high volatility regimes, paired 30-day moving-block bootstrap, Random Forest OOB/permutation importance, and LSTM seeds 7/42/101

## Final Project Position

As of 2026-07-20, the project has moved from a broad "machine learning versus statistics" idea into a controlled Bitcoin volatility-forecasting comparison with a submission-length report, reproducible data and auditable model outputs. The final discussion avoids a simplistic "best model wins" structure and asks whether any accuracy gain is large and stable enough to justify weaker interpretability and higher implementation cost.

The current data-and-model pipeline has been refreshed and expanded into a packaged code architecture under `code/epq_pipeline/`. The latest run uses 1,240 completed daily candles through 2026-07-19 and produces a modelling frame of 1,195 forecast origins through 2026-07-18. The frozen primary split contains 950 training rows through 2025-11-15 and 245 test rows beginning 2025-11-16; the corresponding target dates run through 2026-07-19.

The final method audit aligned GARCH forecasts by date, corrected the likelihood update, excluded incomplete candles, froze the test cutoff, removed the rolling-standard-deviation feature that was mathematically identical to the active target-window volatility, and changed the primary GARCH standard-deviation forecast to an 80-point Gauss-Hermite estimate of `E[s]`. The earlier `sqrt(E[s^2])` conversion remains an explicit sensitivity rather than a hidden approximation. Machine learning still does not produce an overall advantage. The audited 30-day RMSE ranking is:

- GARCH(1,1): `0.00098502`
- Lagged linear regression: `0.00140087`
- Rolling historical volatility: `0.00142744`
- LSTM: `0.00174351`
- Random Forest: `0.00232370`

GARCH also ranks first for the 14-day target (`0.00178208`), both chronological halves, all three target-volatility regimes and every expanding-window fold. Its concatenated rolling-origin RMSE is `0.00098681`. The paired moving-block bootstrap interval for its RMSE difference from rolling is `[-0.00099670, -0.00017158]`. Re-running the upgraded method on the archive truncated at 2026-07-12 preserves all five ranks; appending the seven newly completed candles changes each RMSE by only about 0.8–1.4%. This is a cleaner stability check than comparing outputs produced by different code versions.

The extended diagnostics clarify why added model complexity did not help overall. Random Forest OOB predictions cover every training row with RMSE `0.00131585`, but chronological-test RMSE rises to `0.00232370`, indicating weaker cross-period generalisation. LSTM seeds 7, 42 and 101 all remain worse than rolling, although it locally beats rolling in two individual expanding-window folds. The current automated suite contains 39 passing tests.

The planned report structure is:

1. Introduction
2. Literature Review
3. Mathematical Formulation
4. Methodology and Data Source
5. Results
6. Comparative Analysis and Discussion
7. Conclusion

The canonical written product is `report/final-report.md` (5,356 words before references, within the required 5,000 +/-10% range). Superseded section drafts are intentionally excluded from the current repository tree; their development remains visible through Git history.

## Folder Structure

```text
EPQ/
  production-log/   Current English production log, weekly record, and build tool
  report/           Canonical English 5,000-word report
  research/         Sources, literature notes, and search log
  data/             Raw and processed cryptocurrency price data
  code/             Data analysis and model comparison scripts/notebooks
  appendix/         Timetable, risk assessment, extra charts, model outputs
  presentation/     Slides and presentation planning materials
  zh-cn/            Canonical Chinese report, logs, and concise index
```

## Documentation Policy

The repository tracks one current file for each deliverable. Draft report sections, superseded production-log fragments, duplicated Chinese exports, and long-form guide copies are not kept in the working tree. Git history provides process traceability without making older versions look current.

- English report: `report/final-report.md`
- Chinese report: `zh-cn/final-report-zh-cn.md`
- English production log: `production-log/complete-production-log-en.md` and `.docx`
- Chinese production log: `zh-cn/complete-production-log-zh-cn.md` and `.docx`
- Weekly records: `production-log/weekly-work-log-en.md` and `zh-cn/weekly-work-log-zh-cn.md`

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

- Written report: 5,000 words +/-10%; current report body is 5,356 words before references
- Production log: complete English transfer draft plus a structurally identical Chinese reading copy in Markdown and DOCX, each stored once
- Presentation: 10 minutes delivery plus 5 minutes Q&A
- Appendix: timetable, risk assessment, data/code evidence, extra results

## Remaining Administrative Tasks

1. Obtain the candidate's own current production-log form from the centre, then review and transfer the candidate-review material in `production-log/complete-production-log-en.docx`.
2. Produce the final slide file from the completed presentation specification when a compliant PowerPoint-authoring runtime is available.
3. Deliver the presentation and record the real audience, five questions, answers and supervisor comments; these cannot be completed in advance.
