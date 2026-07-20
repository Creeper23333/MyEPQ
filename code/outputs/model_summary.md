# Current Volatility Model Results

Generated: 2026-07-20T06:14:33+00:00

## Dataset

- Source file: `data/processed/hyperliquid_BTC_1d_volatility.csv`
- Model frame rows: 1195
- Train rows: 950 (2023-04-11 to 2025-11-15)
- Test rows: 245 (2025-11-16 to 2026-07-18)
- Forecast target: next-day 30-day realised volatility, not annualised
- Primary validation: frozen forecast-origin cutoff at 2025-11-16; later data extends the test set without moving earlier test rows into training
- Supplementary validation: 4-fold expanding-window rolling-origin evaluation with refitting at each later boundary
- Exported `date` is the forecast-origin date; `target_date` is the next completed candle whose updated rolling volatility is predicted

## Result

Best current model by RMSE: **GARCH(1,1)** with RMSE `0.00098502`.

| Rank | Model | Category | MAE | MSE | RMSE |
| --- | --- | --- | --- | --- | --- |
| 1 | GARCH(1,1) | Traditional statistical | 0.00047642 | 0.00000097 | 0.00098502 |
| 2 | Lagged linear regression | Interpretable lag-feature model | 0.00073861 | 0.00000196 | 0.00140087 |
| 3 | Rolling historical volatility | Benchmark | 0.00062843 | 0.00000204 | 0.00142744 |
| 4 | LSTM | Machine learning | 0.00104907 | 0.00000304 | 0.00174351 |
| 5 | Random Forest | Machine learning | 0.00135845 | 0.00000540 | 0.00232370 |

## Notes

- Rolling historical volatility is the transparent benchmark.
- GARCH(1,1) is fitted by grid-search maximum likelihood with variance targeting. The primary 30-day standard-deviation forecast is E[s], evaluated by 80-point Gauss-Hermite quadrature; sqrt(E[s^2]) is retained as a target-conversion sensitivity.
- Random Forest is a lightweight in-repo implementation because the current environment does not include scikit-learn.
- LSTM is fitted using PyTorch on rolling 30-day sequences of core market features. Early stopping selected epoch 20 from 50 completed epochs using a chronological validation split.

## Computational Practicality

Timings are from one local CPU run and are implementation-specific, so they indicate relative project cost rather than universal benchmark speed.

| Model | Fit seconds | Predict seconds | Complexity |
| --- | --- | --- | --- |
| Rolling historical volatility | 0.000000 | 0.000016 | 0 fitted parameters |
| GARCH(1,1) | 1.001552 | 0.020569 | 3 fitted parameters |
| Lagged linear regression | 0.000236 | 0.000037 | 26 coefficients including intercept |
| Random Forest | 5.412435 | 0.038393 | 17984 tree nodes across forest |
| LSTM | 5.422232 | 0.010940 | 5921 trainable parameters |

## Robustness Across Target Windows

| Window | Rank | Model | RMSE | Difference from rolling benchmark |
| --- | --- | --- | --- | --- |
| 14 days | 1 | GARCH(1,1) | 0.00178208 | -35.482% |
| 14 days | 2 | Lagged linear regression | 0.00260295 | -5.763% |
| 14 days | 3 | Rolling historical volatility | 0.00276213 | 0.000% |
| 14 days | 4 | LSTM | 0.00364246 | 31.871% |
| 14 days | 5 | Random Forest | 0.00405515 | 46.812% |
| 30 days | 1 | GARCH(1,1) | 0.00098502 | -30.994% |
| 30 days | 2 | Lagged linear regression | 0.00140087 | -1.861% |
| 30 days | 3 | Rolling historical volatility | 0.00142744 | 0.000% |
| 30 days | 4 | LSTM | 0.00174351 | 22.142% |
| 30 days | 5 | Random Forest | 0.00232370 | 62.787% |

## Robustness Across Test-Period Halves

| Segment | Dates | Rank | Model | RMSE |
| --- | --- | --- | --- | --- |
| First half | 2025-11-16 to 2026-03-17 | 1 | GARCH(1,1) | 0.00128466 |
| First half | 2025-11-16 to 2026-03-17 | 2 | Lagged linear regression | 0.00181258 |
| First half | 2025-11-16 to 2026-03-17 | 3 | Rolling historical volatility | 0.00184741 |
| First half | 2025-11-16 to 2026-03-17 | 4 | LSTM | 0.00230143 |
| First half | 2025-11-16 to 2026-03-17 | 5 | Random Forest | 0.00313415 |
| Second half | 2026-03-18 to 2026-07-18 | 1 | GARCH(1,1) | 0.00054380 |
| Second half | 2026-03-18 to 2026-07-18 | 2 | Lagged linear regression | 0.00080636 |
| Second half | 2026-03-18 to 2026-07-18 | 3 | Rolling historical volatility | 0.00082064 |
| Second half | 2026-03-18 to 2026-07-18 | 4 | LSTM | 0.00089524 |
| Second half | 2026-03-18 to 2026-07-18 | 5 | Random Forest | 0.00100607 |

## Moving-Block Bootstrap Versus Rolling

Negative differences favour the model. Intervals use 2,000 paired circular resamples of 30-day blocks.

| Model | RMSE difference | 95% interval |
| --- | --- | --- |
| Rolling historical volatility | 0.00000000 | [0.00000000, 0.00000000] |
| GARCH(1,1) | -0.00044242 | [-0.00099670, -0.00017158] |
| Lagged linear regression | -0.00002657 | [-0.00009605, 0.00003681] |
| Random Forest | 0.00089625 | [0.00008895, 0.00158205] |
| LSTM | 0.00031607 | [0.00000898, 0.00063980] |

## Accuracy by Realised-Volatility Regime

Regimes are test-target terciles. Bias is prediction minus actual; positive values indicate overprediction.

| Regime | Rank | Model | RMSE | Bias |
| --- | --- | --- | --- | --- |
| Low | 1 | GARCH(1,1) | 0.00065099 | 0.00013635 |
| Low | 2 | Lagged linear regression | 0.00087940 | 0.00022330 |
| Low | 3 | Rolling historical volatility | 0.00092027 | 0.00009568 |
| Low | 4 | LSTM | 0.00095522 | 0.00034429 |
| Low | 5 | Random Forest | 0.00105855 | 0.00046417 |
| Medium | 1 | GARCH(1,1) | 0.00058047 | 0.00009267 |
| Medium | 2 | Lagged linear regression | 0.00084830 | 0.00007231 |
| Medium | 3 | Rolling historical volatility | 0.00086073 | 0.00004503 |
| Medium | 4 | LSTM | 0.00093082 | 0.00006152 |
| Medium | 5 | Random Forest | 0.00099505 | 0.00022877 |
| High | 1 | GARCH(1,1) | 0.00146368 | -0.00015218 |
| High | 2 | Lagged linear regression | 0.00209266 | -0.00036605 |
| High | 3 | Rolling historical volatility | 0.00212349 | -0.00008331 |
| High | 4 | LSTM | 0.00270447 | -0.00091036 |
| High | 5 | Random Forest | 0.00374624 | -0.00162318 |

## Expanding-Window Rolling-Origin Evaluation (4 Folds)

Each fold refits on all information available before its test block. The first fold reuses the primary fitted models because its training boundary is identical.

| Rank | Model | MAE | RMSE |
| --- | --- | --- | --- |
| 1 | GARCH(1,1) | 0.00047666 | 0.00098681 |
| 2 | Lagged linear regression | 0.00073315 | 0.00139934 |
| 3 | Rolling historical volatility | 0.00062843 | 0.00142744 |
| 4 | LSTM | 0.00120218 | 0.00203235 |
| 5 | Random Forest | 0.00131973 | 0.00228159 |

## LSTM Seed Stability

| Seed | Best epoch | MAE | RMSE |
| --- | --- | --- | --- |
| 7 | 11 | 0.00107150 | 0.00184673 |
| 42 | 20 | 0.00104907 | 0.00174351 |
| 101 | 16 | 0.00118157 | 0.00183721 |

## Output Files

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
