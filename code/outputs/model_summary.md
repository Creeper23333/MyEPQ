# Current Volatility Model Results

Generated: 2026-08-20T05:07:17+00:00

## Dataset

- Source file: `data/processed/hyperliquid_BTC_1d_volatility.csv`
- Model frame rows: 1226
- Train rows: 950 (2023-04-11 to 2025-11-15)
- Test rows: 276 (2025-11-16 to 2026-08-18)
- Forecast target: next-day 30-day realised volatility, not annualised
- Primary validation: frozen forecast-origin cutoff at 2025-11-16; later data extends the test set without moving earlier test rows into training
- Supplementary validation: 4-fold expanding-window rolling-origin evaluation with refitting at each later boundary
- Exported `date` is the forecast-origin date; `target_date` is the next completed candle whose updated rolling volatility is predicted

## Result

Best current model by RMSE: **GARCH(1,1)** with RMSE `0.00098301`.

- QLIKE is evaluated on squared forecasts with epsilon `1e-12`.

| Rank | Model | Category | MAE | MSE | RMSE | QLIKE |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | GARCH(1,1) | Traditional statistical | 0.00048109 | 0.00000097 | 0.00098301 | 0.00445845 |
| 2 | Lagged linear regression | Interpretable lag-feature model | 0.00072090 | 0.00000189 | 0.00137492 | 0.00724584 |
| 3 | Rolling historical volatility | Benchmark | 0.00061444 | 0.00000195 | 0.00139570 | 0.00754794 |
| 4 | LSTM | Machine learning | 0.00099818 | 0.00000285 | 0.00168735 | 0.00897661 |
| 5 | Random Forest | Machine learning | 0.00123057 | 0.00000446 | 0.00211129 | 0.01182354 |

## Notes

- Rolling historical volatility is the transparent benchmark.
- GARCH(1,1) is fitted by grid-search maximum likelihood with variance targeting. The primary 30-day standard-deviation forecast is E[s], evaluated by 80-point Gauss-Hermite quadrature; sqrt(E[s^2]) is retained as a target-conversion sensitivity.
- Random Forest uses the standard scikit-learn implementation. A compact, predeclared candidate set is compared on chronological training validation and the selected configuration is refitted on all pre-test rows.
- LSTM is fitted using PyTorch on rolling 30-day sequences of core market features. A compact predeclared candidate set and early stopping use only chronological training validation; the selected run used hidden size 32 and learning rate 0.003.

## Computational Practicality

Timings are from one local CPU run and are implementation-specific, so they indicate relative project cost rather than universal benchmark speed.

| Model | Fit seconds | Predict seconds | Complexity | Selection/tuning |
| --- | --- | --- | --- | --- |
| Rolling historical volatility | 0.000000 | 0.000011 | 0 fitted parameters | None |
| GARCH(1,1) | 0.529684 | 0.010776 | 3 fitted parameters | Deterministic coarse-to-fine likelihood grid |
| Lagged linear regression | 0.004307 | 0.000019 | 26 coefficients including intercept | No search; ridge 1e-8 fixed for numerical stability |
| Random Forest | 1.384384 | 0.007390 | 57970 tree nodes across forest | 6 predeclared candidates on chronological training validation; selected model refitted on all pre-test rows |
| LSTM | 9.739972 | 0.004044 | 5921 trainable parameters | 4 predeclared candidates on chronological training validation plus early stopping |

## Robustness Across Target Windows

| Window | Rank | Model | RMSE | QLIKE | Difference from rolling benchmark |
| --- | --- | --- | --- | --- | --- |
| 14 days | 1 | GARCH(1,1) | 0.00181314 | 0.01741379 | -33.416% |
| 14 days | 2 | Lagged linear regression | 0.00258160 | 0.03009120 | -5.196% |
| 14 days | 3 | Rolling historical volatility | 0.00272309 | 0.03175436 | 0.000% |
| 14 days | 4 | LSTM | 0.00352137 | 0.03527526 | 29.315% |
| 14 days | 5 | Random Forest | 0.00383276 | 0.03940360 | 40.750% |
| 30 days | 1 | GARCH(1,1) | 0.00098301 | 0.00445845 | -29.569% |
| 30 days | 2 | Lagged linear regression | 0.00137492 | 0.00724584 | -1.489% |
| 30 days | 3 | Rolling historical volatility | 0.00139570 | 0.00754794 | 0.000% |
| 30 days | 4 | LSTM | 0.00168735 | 0.00897661 | 20.896% |
| 30 days | 5 | Random Forest | 0.00211129 | 0.01182354 | 51.271% |

## Robustness Across Test-Period Halves

| Segment | Dates | Rank | Model | RMSE | QLIKE |
| --- | --- | --- | --- | --- | --- |
| First half | 2025-11-16 to 2026-04-02 | 1 | GARCH(1,1) | 0.00121469 | 0.00482743 |
| First half | 2025-11-16 to 2026-04-02 | 2 | Lagged linear regression | 0.00173514 | 0.00802634 |
| First half | 2025-11-16 to 2026-04-02 | 3 | Rolling historical volatility | 0.00177108 | 0.00866312 |
| First half | 2025-11-16 to 2026-04-02 | 4 | LSTM | 0.00219711 | 0.01092534 |
| First half | 2025-11-16 to 2026-04-02 | 5 | Random Forest | 0.00281285 | 0.01622664 |
| Second half | 2026-04-03 to 2026-08-18 | 1 | GARCH(1,1) | 0.00067613 | 0.00408946 |
| Second half | 2026-04-03 to 2026-08-18 | 2 | Rolling historical volatility | 0.00087134 | 0.00643276 |
| Second half | 2026-04-03 to 2026-08-18 | 3 | Lagged linear regression | 0.00087756 | 0.00646534 |
| Second half | 2026-04-03 to 2026-08-18 | 4 | LSTM | 0.00093112 | 0.00702789 |
| Second half | 2026-04-03 to 2026-08-18 | 5 | Random Forest | 0.00100148 | 0.00742044 |

## Moving-Block Bootstrap Versus Rolling

Negative differences favour the model. Intervals use 2,000 paired circular resamples of 30-day blocks.

| Model | RMSE difference | 95% interval |
| --- | --- | --- |
| Rolling historical volatility | 0.00000000 | [0.00000000, 0.00000000] |
| GARCH(1,1) | -0.00041269 | [-0.00089954, -0.00016861] |
| Lagged linear regression | -0.00002078 | [-0.00008328, 0.00004204] |
| Random Forest | 0.00071559 | [0.00005958, 0.00128485] |
| LSTM | 0.00029165 | [0.00000368, 0.00061163] |

## Accuracy by Realised-Volatility Regime

Regimes are test-target terciles. Bias is prediction minus actual; positive values indicate overprediction.

| Regime | Rank | Model | RMSE | QLIKE | Bias |
| --- | --- | --- | --- | --- | --- |
| Low | 1 | GARCH(1,1) | 0.00069948 | 0.00523307 | 0.00015421 |
| Low | 2 | Rolling historical volatility | 0.00091130 | 0.00834489 | 0.00007514 |
| Low | 3 | Lagged linear regression | 0.00092501 | 0.00858625 | 0.00022951 |
| Low | 4 | Random Forest | 0.00098052 | 0.00868975 | 0.00041879 |
| Low | 5 | LSTM | 0.00098559 | 0.00941779 | 0.00030840 |
| Medium | 1 | GARCH(1,1) | 0.00068656 | 0.00300876 | 0.00007812 |
| Medium | 2 | Lagged linear regression | 0.00092683 | 0.00473613 | 0.00008933 |
| Medium | 3 | Rolling historical volatility | 0.00096695 | 0.00533903 | 0.00005696 |
| Medium | 4 | LSTM | 0.00099784 | 0.00529451 | 0.00008482 |
| Medium | 5 | Random Forest | 0.00108780 | 0.00646568 | 0.00017145 |
| High | 1 | GARCH(1,1) | 0.00139222 | 0.00513351 | -0.00013275 |
| High | 2 | Lagged linear regression | 0.00198912 | 0.00841513 | -0.00034007 |
| High | 3 | Rolling historical volatility | 0.00201952 | 0.00895988 | -0.00008702 |
| High | 4 | LSTM | 0.00256405 | 0.01221753 | -0.00080907 |
| High | 5 | Random Forest | 0.00335081 | 0.02031518 | -0.00127757 |

## Expanding-Window Rolling-Origin Evaluation (4 Folds)

Each fold refits on all information available before its test block. The first fold reuses the primary fitted models because its training boundary is identical.

| Rank | Model | MAE | RMSE | QLIKE |
| --- | --- | --- | --- | --- |
| 1 | GARCH(1,1) | 0.00048073 | 0.00098432 | 0.00446344 |
| 2 | Lagged linear regression | 0.00071673 | 0.00137390 | 0.00721327 |
| 3 | Rolling historical volatility | 0.00061444 | 0.00139570 | 0.00754794 |
| 4 | LSTM | 0.00116624 | 0.00189862 | 0.00998982 |
| 5 | Random Forest | 0.00121148 | 0.00209190 | 0.01161326 |

## LSTM Seed Stability

| Seed | Best epoch | MAE | RMSE | QLIKE |
| --- | --- | --- | --- | --- |
| 7 | 11 | 0.00101738 | 0.00178061 | 0.00926021 |
| 42 | 20 | 0.00099818 | 0.00168735 | 0.00897661 |
| 101 | 33 | 0.00100531 | 0.00172688 | 0.00867541 |

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
