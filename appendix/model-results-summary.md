# Current Model Results Summary

## Dataset and Validation

- Data source: Hyperliquid BTC daily perpetual-futures candles.
- Latest refresh: 2026-08-20 (Beijing date); 1,272 rows were returned and the still-open 20 August candle was excluded, leaving 1,271 complete candles through 2026-08-19.
- Primary target: next-day update of a 30-day rolling standard-deviation proxy, not annualised; adjacent targets share 29 returns.
- Primary frame: 1,226 rows through 2026-08-18; 950 training origins through 2025-11-15 and 276 test origins from 2025-11-16 to 2026-08-18, with targets through 2026-08-19.
- Primary validation: frozen forecast-origin cutoff at 2025-11-16, with no random shuffling or refitting inside the holdout. New completed candles extend the test set without changing the training boundary.
- Supplementary validation: four expanding-window rolling-origin folds, with all models refitted at each later boundary.
- Exported `date` is the forecast-origin date and `target_date` is the next completed candle whose updated rolling volatility is predicted.
- Robustness target: next-day 14-day realised volatility.

## Corrected Primary Performance

| Rank | Model | Category | MAE | RMSE | QLIKE |
| --- | --- | --- | ---: | ---: | ---: |
| 1 | GARCH(1,1) | Traditional statistical | 0.00048109 | 0.00098301 | 0.00445845 |
| 2 | Lagged linear regression | Auxiliary linear comparator | 0.00072090 | 0.00137492 | 0.00724584 |
| 3 | Rolling historical volatility | Persistence benchmark | 0.00061444 | 0.00139570 | 0.00754794 |
| 4 | LSTM | Nonlinear sequence pipeline | 0.00099818 | 0.00168735 | 0.00897661 |
| 5 | Random Forest | Nonlinear tabular pipeline | 0.00123057 | 0.00211129 | 0.01182354 |

RMSE and QLIKE give the same ordering. GARCH improves RMSE by 29.6% relative to rolling; LSTM and Random Forest are 20.9% and 51.3% worse.

## Method Corrections

The modelling audit corrected the following material issues:

1. Earlier GARCH predictions were extracted by reset dataframe row number after feature engineering removed incomplete early rows. The pipeline now maps forecasts to test observations by date and rejects missing or duplicate mappings.
2. The GARCH likelihood recursion updated conditional variance with the current return before scoring that same return, which introduced one-step look-ahead. The likelihood now scores each return using information available beforehand and only then updates the next variance.
3. The conversion from one-step conditional variance to expected rolling sample variance initially substituted the expected return into the sample mean and therefore over-counted conditional variance by `variance / window`. The corrected expectation includes the random next return in both its squared term and the sample-mean term.
4. Because the scored target is a standard deviation, the squared-error point forecast is `E[s]`, not `sqrt(E[s^2])`. The primary GARCH forecast now integrates `E[s]` with 80-point Gauss-Hermite quadrature. The analytic alternative remains exported: its RMSE is `0.00098255`, versus `0.00098301` for the theoretically aligned primary conversion. The roughly 0.05% difference does not change any model rank.
5. `realised_volatility_30d` and `rolling_return_std_30d` were mathematically the same predictor. The matching rolling-standard-deviation column is now removed dynamically for the active target window, leaving 25 tabular features and eight LSTM features in the primary run.
6. A moving 80/20 row split allowed later refreshes to move old test rows into training. The primary forecast-origin cutoff is now frozen at 2025-11-16, so the original 950-row training set stays unchanged while newly completed candles extend the test evidence.
7. The project-local forest was replaced by the standard `sklearn.ensemble.RandomForestRegressor`; six predeclared candidates are selected on chronological training validation and the final holdout remains untouched.
8. LSTM now compares four predeclared hidden-size/learning-rate pairs under the same training-only chronological-validation principle, with early stopping and seed stability recorded.
9. Variance-scale QLIKE is reported with epsilon `1e-12`, following Patton's imperfect-proxy concern. It supplements rather than replaces RMSE/MAE and does not remove the rolling proxy's limitations.
10. Feature sets and target transformations differ across pipelines, so conclusions are explicitly about the tested GARCH-based and direct-target ML pipelines rather than an isolated architecture effect.

The current figures above are post-correction. The data fetch also now drops any daily candle whose end timestamp has not passed at fetch time.

## Robustness

| Window | Winner | Winner RMSE | Rolling RMSE | Improvement over rolling |
| --- | --- | --- | --- | --- |
| 14 days | GARCH(1,1) | 0.00181314 | 0.00272309 | 33.4% |
| 30 days | GARCH(1,1) | 0.00098301 | 0.00139570 | 29.6% |

All five models retain the same rank at both windows: GARCH, linear regression, rolling historical volatility, LSTM, and Random Forest. This supports ranking stability across the two tested target definitions, but it does not prove stability across different assets.

The 276-observation primary test period was also divided into two chronological halves of 138 observations. GARCH ranked first from 2025-11-16 to 2026-04-02 with RMSE `0.00121469`, and again from 2026-04-03 to 2026-08-18 with RMSE `0.00067613`. Linear regression ranked second in the first half, while rolling ranked second in the later half, so only GARCH's first place was unchanged between halves.

A 2,000-sample paired circular 30-day moving-block bootstrap compared each model's RMSE with rolling historical volatility while retaining local time dependence. GARCH's observed RMSE difference was `-0.00041269` and its 95% interval was `[-0.00089954, -0.00016861]`, with 100% of replicates favouring GARCH. The linear interval `[-0.00008328, 0.00004204]` crossed zero, so its small point advantage is not decisive. The LSTM and Random Forest intervals were fully positive, supporting worse RMSE than rolling under this resampling design. These intervals quantify sampling uncertainty in one market history; they are not a universal guarantee.

The four expanding-window test blocks contain 69 observations each. GARCH ranks first in every block, with fold RMSE values `0.00059084`, `0.00161607`, `0.00064841` and `0.00070307`. Concatenating the four blocks gives GARCH RMSE `0.00098432`; the overall order remains GARCH, linear regression, rolling, LSTM and Random Forest. LSTM beats rolling in the first block only, but not overall, so one local result does not establish a general machine-learning improvement.

The primary test target was also divided into three groups of 92 observations. GARCH ranks first in low-, medium- and high-volatility regimes, with RMSE `0.00069948`, `0.00068656` and `0.00139222`. Its high-regime mean bias is `-0.00013275`, so the winning model still slightly underpredicts the most volatile group on average.

An apples-to-apples refresh check reran the current code on the archive truncated at 2026-07-19. Adding 31 completed candles through 2026-08-19 preserves every overall rank. RMSE changes are small and downward: GARCH from `0.00098502` to `0.00098301`, linear from `0.00140087` to `0.00137492`, rolling from `0.00142744` to `0.00139570`, LSTM from `0.00174351` to `0.00168735`, and Random Forest from `0.00220594` to `0.00211129`. QLIKE rises for all five models, so the refresh does not support an unqualified claim that every aspect improved.

The final completed target is also a useful shock-day diagnostic. On 19 August the close rose from `64,696` to `69,323`, a log return of about `0.06908`, and the 30-day proxy rose from `0.01212489` to `0.01746941`. Random Forest's saved forecast (`0.01303376`) was the closest of the five on that one date, ahead of GARCH (`0.01253680`), but every model underpredicted the jump. This is one already observed holdout target, not evidence that Random Forest improved overall and not a valid basis for post-hoc tuning or model selection.

## Multi-Dimensional Interpretation

GARCH has the lowest errors, stays first in the extra checks and can be explained with three reported parameters. Rolling historical volatility is easiest to explain but less accurate. Linear regression is fast and coefficient-based, but it only narrowly improves RMSE over rolling and has worse MAE.

Random Forest supplies impurity importance, repeated holdout permutation importance and OOB evidence. OOB RMSE is `0.00128268`, versus chronological-test RMSE `0.00211129`. The current proxy, its first lag and 30-day mean absolute return lead permutation importance. LSTM seeds 7, 42 and 101 produce RMSE `0.00178061`, `0.00168735` and `0.00172688`. Ablating the current proxy increases LSTM RMSE by `0.00476927`, showing prediction sensitivity without establishing causality.

The current local run measured fit times of `0.529684` seconds for GARCH, `1.384384` for Random Forest and `9.739972` for LSTM. Practicality also includes dependency, tuning, stability and maintenance burden; local timings are not universal deployment benchmarks.

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
- `code/outputs/random_forest_tuning.csv`
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
- `code/outputs/lstm_tuning.csv`
- `code/outputs/lstm_feature_sensitivity.csv`
- `code/outputs/model_run_metadata.json`
- `code/outputs/volatility_forecast_comparison.png`
- `code/outputs/model_summary.md`
- `code/outputs/model_refresh_stability.csv`
- `data/raw/hyperliquid_BTC_1d_quality_report.json`

## Close-Out Position

The final report and presentation materials use the upgraded result and make the implementation audit explicit. Supervisor comments, signatures, real presentation evidence and the candidate's own centre-controlled form fields still require human completion. No third-party form is tracked in the repository.
