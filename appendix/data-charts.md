# Appendix Data Charts

## Forecast Comparison

![Actual and forecast 30-day rolling volatility proxy](../code/outputs/volatility_forecast_comparison.png)

The chart shows the fixed-cutoff chronological test. Adjacent targets share 29
returns, so close tracking partly reflects the overlapping rolling-window
construction. Larger separations are interpreted with RMSE, MAE, QLIKE, regime
bias and robustness evidence rather than by visual inspection alone.

## Primary Audited Results

| Rank | Model | MAE | RMSE | QLIKE |
| ---: | --- | ---: | ---: | ---: |
| 1 | GARCH(1,1) | 0.00047642 | 0.00098502 | 0.00370047 |
| 2 | Lagged linear regression | 0.00097354 | 0.00140087 | 0.00623445 |
| 3 | Rolling historical volatility | 0.00093289 | 0.00142744 | 0.00669043 |
| 4 | LSTM | 0.00104907 | 0.00174351 | 0.00816805 |
| 5 | Random Forest | 0.00128867 | 0.00220594 | 0.01170773 |

Full data tables, predictions, target-window checks, test halves, regimes,
bootstrap intervals and expanding-window folds remain in `code/outputs/` and
are indexed in `appendix/model-results-summary.md`.
