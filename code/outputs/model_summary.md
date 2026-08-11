# Current Volatility Model Results

Generated: 2026-07-25T16:23:07+00:00

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

- QLIKE is evaluated on squared forecasts with epsilon `1e-12`.

| Rank | Model | Category | MAE | MSE | RMSE | QLIKE |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | GARCH(1,1) | Traditional statistical | 0.00047642 | 0.00000097 | 0.00098502 | 0.00370047 |
| 2 | Lagged linear regression | Interpretable lag-feature model | 0.00073861 | 0.00000196 | 0.00140087 | 0.00623445 |
| 3 | Rolling historical volatility | Benchmark | 0.00062843 | 0.00000204 | 0.00142744 | 0.00669043 |
| 4 | LSTM | Machine learning | 0.00104907 | 0.00000304 | 0.00174351 | 0.00816805 |
| 5 | Random Forest | Machine learning | 0.00128867 | 0.00000487 | 0.00220594 | 0.01170773 |

## Notes

- Rolling historical volatility is the transparent benchmark.
- GARCH(1,1) is fitted by grid-search maximum likelihood with variance targeting. The primary 30-day standard-deviation forecast is E[s], evaluated by 80-point Gauss-Hermite quadrature; sqrt(E[s^2]) is retained as a target-conversion sensitivity.
- Random Forest uses the standard scikit-learn implementation. A compact, predeclared candidate set is compared on chronological training validation and the selected configuration is refitted on all pre-test rows.
- LSTM is fitted using PyTorch on rolling 30-day sequences of core market features. A compact predeclared candidate set and early stopping use only chronological training validation; the selected run used hidden size 32 and learning rate 0.003.

## Computational Practicality

Timings are from one local CPU run and are implementation-specific, so they indicate relative project cost rather than universal benchmark speed.

| Model | Fit seconds | Predict seconds | Complexity | Selection/tuning |
| --- | --- | --- | --- | --- |
| Rolling historical volatility | 0.000000 | 0.000010 | 0 fitted parameters | None |
| GARCH(1,1) | 0.530158 | 0.011173 | 3 fitted parameters | Deterministic coarse-to-fine likelihood grid |
| Lagged linear regression | 0.000227 | 0.000014 | 26 coefficients including intercept | No search; ridge 1e-8 fixed for numerical stability |
| Random Forest | 1.384994 | 0.007129 | 57970 tree nodes across forest | 6 predeclared candidates on chronological training validation; selected model refitted on all pre-test rows |
| LSTM | 11.051759 | 0.003069 | 5921 trainable parameters | 4 predeclared candidates on chronological training validation plus early stopping |

## Robustness Across Target Windows

| Window | Rank | Model | RMSE | QLIKE | Difference from rolling benchmark |
| --- | --- | --- | --- | --- | --- |
| 14 days | 1 | GARCH(1,1) | 0.00178208 | 0.01151218 | -35.482% |
| 14 days | 2 | Lagged linear regression | 0.00260295 | 0.02188030 | -5.763% |
| 14 days | 3 | Rolling historical volatility | 0.00276213 | 0.02296215 | 0.000% |
| 14 days | 4 | LSTM | 0.00364246 | 0.02991099 | 31.871% |
| 14 days | 5 | Random Forest | 0.00397432 | 0.03281829 | 43.886% |
| 30 days | 1 | GARCH(1,1) | 0.00098502 | 0.00370047 | -30.994% |
| 30 days | 2 | Lagged linear regression | 0.00140087 | 0.00623445 | -1.861% |
| 30 days | 3 | Rolling historical volatility | 0.00142744 | 0.00669043 | 0.000% |
| 30 days | 4 | LSTM | 0.00174351 | 0.00816805 | 22.142% |
| 30 days | 5 | Random Forest | 0.00220594 | 0.01170773 | 54.538% |

## Robustness Across Test-Period Halves

| Segment | Dates | Rank | Model | RMSE | QLIKE |
| --- | --- | --- | --- | --- | --- |
| First half | 2025-11-16 to 2026-03-17 | 1 | GARCH(1,1) | 0.00128466 | 0.00540834 |
| First half | 2025-11-16 to 2026-03-17 | 2 | Lagged linear regression | 0.00181258 | 0.00870625 |
| First half | 2025-11-16 to 2026-03-17 | 3 | Rolling historical volatility | 0.00184741 | 0.00938494 |
| First half | 2025-11-16 to 2026-03-17 | 4 | LSTM | 0.00230143 | 0.01186128 |
| First half | 2025-11-16 to 2026-03-17 | 5 | Random Forest | 0.00296438 | 0.01786868 |
| Second half | 2026-03-18 to 2026-07-18 | 1 | GARCH(1,1) | 0.00054380 | 0.00200650 |
| Second half | 2026-03-18 to 2026-07-18 | 2 | Lagged linear regression | 0.00080636 | 0.00378273 |
| Second half | 2026-03-18 to 2026-07-18 | 3 | Rolling historical volatility | 0.00082064 | 0.00401783 |
| Second half | 2026-03-18 to 2026-07-18 | 4 | LSTM | 0.00089524 | 0.00450485 |
| Second half | 2026-03-18 to 2026-07-18 | 5 | Random Forest | 0.00098827 | 0.00559687 |

## Moving-Block Bootstrap Versus Rolling

Negative differences favour the model. Intervals use 2,000 paired circular resamples of 30-day blocks.

| Model | RMSE difference | 95% interval |
| --- | --- | --- |
| Rolling historical volatility | 0.00000000 | [0.00000000, 0.00000000] |
| GARCH(1,1) | -0.00044242 | [-0.00099670, -0.00017158] |
| Lagged linear regression | -0.00002657 | [-0.00009605, 0.00003681] |
| Random Forest | 0.00077850 | [0.00008093, 0.00137210] |
| LSTM | 0.00031607 | [0.00000898, 0.00063980] |

## Accuracy by Realised-Volatility Regime

Regimes are test-target terciles. Bias is prediction minus actual; positive values indicate overprediction.

| Regime | Rank | Model | RMSE | QLIKE | Bias |
| --- | --- | --- | --- | --- | --- |
| Low | 1 | GARCH(1,1) | 0.00065099 | 0.00380423 | 0.00013635 |
| Low | 2 | Lagged linear regression | 0.00087940 | 0.00622193 | 0.00022330 |
| Low | 3 | Rolling historical volatility | 0.00092027 | 0.00694494 | 0.00009568 |
| Low | 4 | LSTM | 0.00095522 | 0.00707209 | 0.00034429 |
| Low | 5 | Random Forest | 0.00102008 | 0.00802017 | 0.00037220 |
| Medium | 1 | GARCH(1,1) | 0.00058047 | 0.00164440 | 0.00009267 |
| Medium | 2 | Lagged linear regression | 0.00084830 | 0.00323318 | 0.00007231 |
| Medium | 3 | Rolling historical volatility | 0.00086073 | 0.00329157 | 0.00004503 |
| Medium | 4 | LSTM | 0.00093082 | 0.00389983 | 0.00006152 |
| Medium | 5 | Random Forest | 0.00098482 | 0.00443527 | 0.00017640 |
| High | 1 | GARCH(1,1) | 0.00146368 | 0.00562772 | -0.00015218 |
| High | 2 | Lagged linear regression | 0.00209266 | 0.00921162 | -0.00036605 |
| High | 3 | Rolling historical volatility | 0.00212349 | 0.00979334 | -0.00008331 |
| High | 4 | LSTM | 0.00270446 | 0.01348019 | -0.00091036 |
| High | 5 | Random Forest | 0.00354127 | 0.02257906 | -0.00142537 |

## Expanding-Window Rolling-Origin Evaluation (4 Folds)

Each fold refits on all information available before its test block. The first fold reuses the primary fitted models because its training boundary is identical.

| Rank | Model | MAE | RMSE | QLIKE |
| --- | --- | --- | --- | --- |
| 1 | GARCH(1,1) | 0.00047666 | 0.00098681 | 0.00371082 |
| 2 | Lagged linear regression | 0.00073315 | 0.00139934 | 0.00616854 |
| 3 | Rolling historical volatility | 0.00062843 | 0.00142744 | 0.00669043 |
| 4 | LSTM | 0.00120218 | 0.00203235 | 0.00991574 |
| 5 | Random Forest | 0.00126906 | 0.00218005 | 0.01150384 |

## LSTM Seed Stability

| Seed | Best epoch | MAE | RMSE | QLIKE |
| --- | --- | --- | --- | --- |
| 7 | 11 | 0.00107150 | 0.00184673 | 0.00852143 |
| 42 | 20 | 0.00104907 | 0.00174351 | 0.00816805 |
| 101 | 33 | 0.00105696 | 0.00178917 | 0.00802103 |

## Output Files

- `code/outputs/model_performance.csv`
- `code/outputs/model_predictions.csv`
- `code/outputs/random_forest_feature_importance.csv`
- `code/outputs/random_forest_permutation_importance.csv`
- `code/outputs/random_forest_tuning.csv`
- `code/outputs/random_forest_oob_summary.json`
- `code/outputs/linear_regression_coefficients.csv`
- `code/outputs/garch_parameters.json`
- `code/outputs/garch_target_conversion_sensitivity.csv`
- `code/outputs/lstm_training_summary.json`
- `code/outputs/lstm_training_history.csv`
- `code/outputs/lstm_tuning.csv`
- `code/outputs/lstm_feature_sensitivity.csv`
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
