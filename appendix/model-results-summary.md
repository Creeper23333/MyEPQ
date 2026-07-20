# Current Model Results Summary

## Dataset and Validation

- Data source: Hyperliquid BTC daily perpetual-futures candles.
- Latest refresh: 2026-07-20 (Beijing time); 1,241 rows were returned and the still-open final candle was excluded, leaving 1,240 complete candles through 2026-07-19.
- Primary target: next-day 30-day realised volatility, not annualised.
- Primary frame: 1,195 rows; 950 train and 245 test observations.
- Primary validation: frozen forecast-origin cutoff at 2025-11-16, with no random shuffling or refitting inside the holdout. New completed candles extend the test set without changing the training boundary.
- Supplementary validation: four expanding-window rolling-origin folds, with all models refitted at each later boundary.
- Exported `date` is the forecast-origin date and `target_date` is the next completed candle whose updated rolling volatility is predicted.
- Robustness target: next-day 14-day realised volatility.

## Corrected Primary Performance

| Rank | Model | Category | MAE | MSE | RMSE |
| --- | --- | --- | --- | --- | --- |
| 1 | GARCH(1,1) | Traditional statistical | 0.00047642 | 0.00000097 | 0.00098502 |
| 2 | Lagged linear regression | Interpretable lag-feature model | 0.00073861 | 0.00000196 | 0.00140087 |
| 3 | Rolling historical volatility | Benchmark | 0.00062843 | 0.00000204 | 0.00142744 |
| 4 | LSTM | Machine learning | 0.00104907 | 0.00000304 | 0.00174351 |
| 5 | Random Forest | Machine learning | 0.00135845 | 0.00000540 | 0.00232370 |

GARCH improves RMSE by 31.0% relative to rolling historical volatility. Machine learning does not produce an overall accuracy advantage: LSTM and Random Forest are 22.1% and 62.8% worse than rolling by RMSE.

## Method Corrections

The modelling audit found six material comparability or implementation issues and corrected each:

1. Earlier GARCH predictions were extracted by reset dataframe row number after feature engineering removed incomplete early rows. The pipeline now maps forecasts to test observations by date and rejects missing or duplicate mappings.
2. The GARCH likelihood recursion updated conditional variance with the current return before scoring that same return, which introduced one-step look-ahead. The likelihood now scores each return using information available beforehand and only then updates the next variance.
3. The conversion from one-step conditional variance to expected rolling sample variance initially substituted the expected return into the sample mean and therefore over-counted conditional variance by `variance / window`. The corrected expectation includes the random next return in both its squared term and the sample-mean term.
4. Because the scored target is a standard deviation, the squared-error point forecast is `E[s]`, not `sqrt(E[s^2])`. The primary GARCH forecast now integrates `E[s]` with 80-point Gauss-Hermite quadrature. The analytic alternative remains exported: its RMSE is `0.00098447`, versus `0.00098502` for the theoretically aligned primary conversion. The 0.06% difference does not change any model rank.
5. `realised_volatility_30d` and `rolling_return_std_30d` were mathematically the same predictor. The matching rolling-standard-deviation column is now removed dynamically for the active target window, leaving 25 tabular features and eight LSTM features in the primary run.
6. A moving 80/20 row split allowed later refreshes to move old test rows into training. The primary forecast-origin cutoff is now frozen at 2025-11-16, so the original 950-row training set stays unchanged while newly completed candles extend the test evidence.

The current figures above are post-correction. The data fetch also now drops any daily candle whose end timestamp has not passed at fetch time.

## Robustness

| Window | Winner | Winner RMSE | Rolling RMSE | Improvement over rolling |
| --- | --- | --- | --- | --- |
| 14 days | GARCH(1,1) | 0.00178208 | 0.00276213 | 35.5% |
| 30 days | GARCH(1,1) | 0.00098502 | 0.00142744 | 31.0% |

All five models retain the same rank at both windows: GARCH, linear regression, rolling historical volatility, LSTM, and Random Forest. This supports ranking stability across the two tested target definitions, but it does not prove stability across different assets.

The primary test period was also divided into two chronological halves. GARCH ranked first in both, with RMSE `0.00128466` over the first 122 observations and `0.00054380` over the final 123; all five models retained the same ordering.

A 2,000-sample paired circular 30-day moving-block bootstrap compared each model's RMSE with rolling historical volatility while retaining local time dependence. GARCH's observed RMSE difference was `-0.00044242` and its 95% interval was `[-0.00099670, -0.00017158]`, with 100% of replicates favouring GARCH. The linear interval `[-0.00009605, 0.00003681]` crossed zero, so its small point advantage is not decisive. The LSTM and Random Forest intervals were fully positive, supporting worse RMSE than rolling under this resampling design. These intervals quantify sampling uncertainty in one market history; they are not a universal guarantee.

The four expanding-window test blocks contain 62, 62, 62 and 59 observations. GARCH ranks first in every block, with fold RMSE values `0.00054874`, `0.00172036`, `0.00040604` and `0.00066627`. Concatenating the four rolling-origin blocks gives GARCH RMSE `0.00098681`; the complete overall order remains GARCH, linear regression, rolling, LSTM and Random Forest. Lower ranks vary locally: LSTM is third and beats rolling in folds 1 and 4, so the mature conclusion is lack of stable overall machine-learning gain rather than failure on every subperiod.

The primary test target was also divided into terciles of 82, 81 and 82 observations. GARCH ranks first in low-, medium- and high-volatility regimes, with RMSE `0.00065099`, `0.00058047` and `0.00146368`. Its high-regime mean bias is `-0.00015218`, so the winning model still slightly underpredicts the most volatile group on average.

An apples-to-apples refresh check reran the upgraded code on the same processed archive truncated at 2026-07-12. Adding the seven newly completed candles preserves every model rank. RMSE changes are small and downward: GARCH from `0.00099309` to `0.00098502`, linear from `0.00141843` to `0.00140087`, rolling from `0.00144481` to `0.00142744`, LSTM from `0.00176625` to `0.00174351`, and Random Forest from `0.00235585` to `0.00232370`. This isolates the data extension from changes in code.

## Multi-Dimensional Interpretation

GARCH has the strongest current balance: first-place accuracy across the primary and supplementary checks, three interpretable parameters, deterministic fitting, and moderate local runtime. Rolling historical volatility is the most transparent but less accurate. Linear regression is fast and coefficient-based but only narrowly improves RMSE over rolling and has worse MAE.

Random Forest supplies impurity importance, repeated holdout permutation importance and an OOB diagnostic. Its OOB predictions cover all 950 training rows with RMSE `0.00131585`, versus chronological test RMSE `0.00232370`; the gap points to weaker cross-period generalisation. After duplicate-feature removal, current 30-day realised volatility, its first lag and 30-day rolling mean absolute return lead permutation importance. LSTM records its 5,921-parameter architecture and training history; seeds 7, 42 and 101 produce RMSE values `0.00184673`, `0.00174351` and `0.00183721`, all worse than rolling.

The current local run measured roughly 1.00 seconds to fit GARCH, 5.41 seconds for Random Forest and 5.42 seconds for the primary LSTM. These timings are implementation- and hardware-specific, so exact values should be taken from `model_computational_profile.csv` rather than presented as universal algorithm benchmarks.

## Evidence Files

- `code/outputs/model_performance.csv`
- `code/outputs/model_predictions.csv`
- `code/outputs/model_multidimensional_comparison.csv`
- `code/outputs/model_computational_profile.csv`
- `code/outputs/model_robustness_by_window.csv`
- `code/outputs/model_robustness_by_test_segment.csv`
- `code/outputs/model_rmse_block_bootstrap.csv`
- `code/outputs/random_forest_feature_importance.csv`
- `code/outputs/random_forest_permutation_importance.csv`
- `code/outputs/random_forest_oob_summary.json`
- `code/outputs/model_performance_by_volatility_regime.csv`
- `code/outputs/model_walk_forward_performance.csv`
- `code/outputs/model_walk_forward_by_fold.csv`
- `code/outputs/model_walk_forward_predictions.csv`
- `code/outputs/lstm_seed_stability.csv`
- `code/outputs/linear_regression_coefficients.csv`
- `code/outputs/garch_parameters.json`
- `code/outputs/garch_target_conversion_sensitivity.csv`
- `code/outputs/lstm_training_summary.json`
- `code/outputs/lstm_training_history.csv`
- `code/outputs/model_run_metadata.json`
- `code/outputs/volatility_forecast_comparison.png`
- `code/outputs/model_summary.md`
- `code/outputs/model_refresh_stability.csv`
- `data/raw/hyperliquid_BTC_1d_quality_report.json`

## Close-Out Position

The final report and presentation materials use the upgraded result and make the implementation audit explicit. Supervisor comments, signatures, real presentation evidence and the candidate's own centre-controlled form fields still require human completion. No third-party form is tracked in the repository.
