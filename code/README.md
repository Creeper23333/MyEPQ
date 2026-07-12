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
    reporting/   Markdown summaries, metadata exports, and chart rendering
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
- `epq_pipeline/data/volatility_dataset.py`: transforms raw candles into the processed realised-volatility dataset and request metadata.
- `epq_pipeline/features/engineering.py`: converts the processed dataset into lagged features, rolling features, standardised model matrices, and LSTM sequences.
- `epq_pipeline/models/garch.py`: grid-search GARCH(1,1) fitting and conversion from conditional variance to a 30-day realised-volatility-style forecast.
- `epq_pipeline/models/linear.py`: closed-form lagged linear regression with coefficient export.
- `epq_pipeline/models/random_forest.py`: lightweight in-repo regression forest used to avoid adding scikit-learn as a hard dependency.
- `epq_pipeline/models/lstm.py`: PyTorch LSTM definition, training loop, early stopping, and prediction logic.
- `epq_pipeline/models/metrics.py`: MAE, MSE, RMSE calculation and ranking helpers.
- `epq_pipeline/reporting/exports.py`: writes model summary markdown and a structured run metadata JSON file.
- `epq_pipeline/reporting/charting.py`: renders the out-of-sample forecast comparison chart with Pillow.
- `epq_pipeline/pipeline/fetch_data.py`: CLI for data refresh.
- `epq_pipeline/pipeline/model_runner.py`: CLI for the full modelling run, split into data preparation, model fitting, prediction assembly, evaluation, and export steps.

## Runtime Flow

1. Fetch Hyperliquid BTC daily candles from the public info endpoint.
2. Write a raw OHLCV archive and request metadata.
3. Build log returns and 30-day realised volatility.
4. Create lagged return, lagged volatility, rolling summary, and volume-based features.
5. Shift the forecast target forward by one day.
6. Apply a chronological 80/20 split.
7. Standardise feature matrices for the linear model, Random Forest, and LSTM inputs.
8. Fit and score rolling historical volatility, GARCH(1,1), lagged linear regression, Random Forest, and LSTM.
9. Export prediction tables, ranking tables, feature importance, linear coefficients, LSTM training history, run metadata, and the comparison chart.

## Entry Points

Refresh data only:

```bash
.venv/bin/python code/fetch_hyperliquid_data.py --end-date 2026-07-13
```

Run models only:

```bash
.venv/bin/python code/run_volatility_models.py
```

Run the full refresh pipeline:

```bash
./code/run_epq_pipeline.sh 2026-07-13
```

Run the test suite:

```bash
.venv/bin/python code/run_tests.py
```

## Current Generated Outputs

- `code/outputs/model_performance.csv`
- `code/outputs/model_predictions.csv`
- `code/outputs/random_forest_feature_importance.csv`
- `code/outputs/linear_regression_coefficients.csv`
- `code/outputs/garch_parameters.json`
- `code/outputs/lstm_training_summary.json`
- `code/outputs/lstm_training_history.csv`
- `code/outputs/model_run_metadata.json`
- `code/outputs/volatility_forecast_comparison.png`
- `code/outputs/model_summary.md`

## Current Status

As refreshed on 2026-07-13, the pipeline pulls 1233 BTC daily candles from 2023-02-26 to the latest available candle on 2026-07-12. The processed modelling frame contains 1188 rows, split into 950 training rows and 238 test rows.

Current RMSE ranking:

1. Lagged linear regression: `0.00141843`
2. Rolling historical volatility: `0.00144481`
3. LSTM: `0.00184029`
4. Random Forest: `0.00212715`
5. GARCH(1,1): `0.01292761`
