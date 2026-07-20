# Code

This folder contains the reproducible analysis pipeline for the EPQ Bitcoin volatility-forecasting project. The code is now organised as a small package rather than two large standalone scripts, so data collection, feature engineering, model training, exports, and tests are separated cleanly.

## Architecture

```text
code/
  epq_pipeline/
    common/      Shared IO helpers and dataclasses
    data/        Hyperliquid API client and dataset-building logic
    features/    Feature engineering, scaling, and chronological splitting
    models/      Rolling benchmark support, GARCH, linear regression, RF, LSTM, metrics
    pipeline/    Command-level orchestration for fetch and modelling runs
    reporting/   Charts, metadata, multi-dimensional evaluation, and robustness exports
  outputs/       Generated model tables, JSON metadata, and figures
  tests/         Unit tests for feature engineering, dataset logic, metrics, and exports
  fetch_hyperliquid_data.py
  run_volatility_models.py
  run_epq_pipeline.sh
  run_tests.py
  requirements.txt
```

## Module Responsibilities

- `epq_pipeline/common/io.py`: directory creation, CSV/JSON/text writing, and safe JSON serialisation for dataclasses, NumPy values, dates, and paths.
- `epq_pipeline/common/types.py`: shared typed containers such as `PerformanceRow`, `StandardizationStats`, and `ChronologicalSplit`.
- `epq_pipeline/config.py`: one place for default file paths, feature lists, model hyperparameters, and output locations.
- `epq_pipeline/data/hyperliquid.py`: low-level POST client for the Hyperliquid info endpoint plus candle and user-role fetch helpers.
- `epq_pipeline/data/volatility_dataset.py`: filters incomplete candles, enforces schema/timestamp/cadence/OHLC/activity quality gates, and writes the processed dataset, request metadata, and a quality report.
- `epq_pipeline/features/engineering.py`: converts the processed dataset into lagged features, rolling features, explicit forecast-origin/target dates, standardised model matrices, and LSTM sequences.
- `epq_pipeline/models/garch.py`: grid-search GARCH(1,1) fitting, 80-point Gauss-Hermite evaluation of the primary expected-standard-deviation target, and an analytic `sqrt(E[s^2])` sensitivity.
- `epq_pipeline/models/linear.py`: closed-form lagged linear regression with coefficient export.
- `epq_pipeline/models/random_forest.py`: lightweight in-repo regression forest with bootstrap fitting, impurity importance, and out-of-bag predictions.
- `epq_pipeline/models/lstm.py`: PyTorch LSTM definition, training loop, early stopping, and prediction logic.
- `epq_pipeline/models/metrics.py`: MAE, MSE, RMSE calculation and ranking helpers.
- `epq_pipeline/reporting/evaluation.py`: builds timings, structural complexity, test-segment and volatility-regime scores, permutation importance, moving-block bootstrap intervals, and auditable comparison rows.
- `epq_pipeline/reporting/exports.py`: writes model summary markdown and a structured run metadata JSON file.
- `epq_pipeline/reporting/charting.py`: renders the out-of-sample forecast comparison chart with Pillow.
- `epq_pipeline/pipeline/fetch_data.py`: CLI for data refresh.
- `epq_pipeline/pipeline/model_runner.py`: CLI for the full modelling run, split into data preparation, model fitting, prediction assembly, evaluation, and export steps.

## Runtime Flow

1. Fetch Hyperliquid BTC daily candles from the public info endpoint and remove any candle whose end timestamp is still in the future.
2. Reject critical schema, ordering, cadence, symbol, interval, price, OHLC, or negative-activity defects; write a separate data-quality report.
3. Write a raw OHLCV archive and request metadata.
4. Validate the processed model input again when modelling is run independently, including columns, daily continuity, prices, activity, returns, and rolling-volatility consistency.
5. Build log returns and 30-day realised volatility, then create lagged return, lagged volatility, rolling summary, and volume-based features. The rolling-return standard deviation identical to the active target-window volatility is removed dynamically to avoid a duplicate predictor.
6. Shift the forecast target forward by one day while retaining both `date` (forecast origin) and `target_date`.
7. Freeze the primary forecast-origin test cutoff at `2025-11-16`. The cutoff was initially near 80/20; later refreshes extend the test period without moving older test rows into training. The 14-day and 30-day robustness runs use the same test dates.
8. Standardise feature matrices without using test data; the LSTM scaler also excludes its chronological internal-validation segment.
9. Fit and score rolling historical volatility, GARCH(1,1), lagged linear regression, Random Forest, and LSTM. GARCH predicts `E[s]` under its Gaussian assumption using 80-point Gauss-Hermite quadrature; `sqrt(E[s^2])` remains an exported sensitivity rather than a sixth model.
10. Measure fit time, prediction time, and model-specific structural complexity.
11. Rerun the complete comparison for 14-day and 30-day targets.
12. Run four expanding-window rolling-origin folds, refitting all models at each later boundary.
13. Check both test halves and low/medium/high target-volatility regimes.
14. Use a paired 30-day moving-block bootstrap for RMSE differences from rolling.
15. Export Random Forest OOB and repeated permutation importance, and rerun LSTM with seeds 7, 42, and 101.
16. Export prediction tables, rankings, GARCH target-conversion sensitivity, interpretation evidence, computational profiles, robustness results, uncertainty evidence, checksummed run metadata, runtime versions, effective sample counts, and the chart.

## Entry Points

Refresh data only:

```bash
.venv/bin/python code/fetch_hyperliquid_data.py --end-date 2026-07-20
```

Run models only:

```bash
.venv/bin/python code/run_volatility_models.py
```

Run the full refresh pipeline:

```bash
./code/run_epq_pipeline.sh 2026-07-20
```

Run the test suite:

```bash
.venv/bin/python code/run_tests.py
```

Re-run the current method on the earlier 2026-07-12 data cut and compare it with the current output:

```bash
.venv/bin/python code/run_refresh_stability_check.py --comparison-end-date 2026-07-12
```

After the report and bilingual log have been synchronised, audit the complete evidence bundle:

```bash
.venv/bin/python code/verify_project_bundle.py
```

## Current Generated Outputs

- `code/outputs/model_performance.csv`
- `code/outputs/model_predictions.csv`
- `code/outputs/random_forest_feature_importance.csv`
- `code/outputs/random_forest_permutation_importance.csv`
- `code/outputs/random_forest_oob_summary.json`
- `code/outputs/linear_regression_coefficients.csv`
- `code/outputs/garch_parameters.json`
- `code/outputs/garch_target_conversion_sensitivity.csv`
- `code/outputs/lstm_training_summary.json`
- `code/outputs/lstm_training_history.csv`
- `code/outputs/model_computational_profile.csv`
- `code/outputs/model_multidimensional_comparison.csv`
- `code/outputs/model_robustness_by_window.csv`
- `code/outputs/model_robustness_by_test_segment.csv`
- `code/outputs/model_rmse_block_bootstrap.csv`
- `code/outputs/model_performance_by_volatility_regime.csv`
- `code/outputs/model_walk_forward_performance.csv`
- `code/outputs/model_walk_forward_by_fold.csv`
- `code/outputs/model_walk_forward_predictions.csv`
- `code/outputs/lstm_seed_stability.csv`
- `code/outputs/model_run_metadata.json`
- `code/outputs/volatility_forecast_comparison.png`
- `code/outputs/model_summary.md`
- `code/outputs/model_refresh_stability.csv` (generated by the separate refresh-stability command)

## Current Validation Contract

- Primary test forecast origins always begin on `2025-11-16`; the training period therefore remains frozen through `2025-11-15` when new daily rows are appended.
- The primary GARCH column now estimates `E[s]`, which is the point target aligned with squared-error evaluation. The previous `sqrt(E[s^2])` conversion is preserved in both `model_predictions.csv` and `garch_target_conversion_sensitivity.csv` for an explicit Jensen-gap check.
- `model_run_metadata.json` records the processed-input SHA-256 digest, split cutoff, runtime/library versions, resolved Random Forest feature count, and model-specific effective training samples.
- Exact scores and timings must be read from a freshly generated output bundle because they change when completed daily candles are appended and when target-conversion logic changes.
