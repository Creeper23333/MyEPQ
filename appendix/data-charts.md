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
| 1 | GARCH(1,1) | 0.00048109 | 0.00098301 | 0.00445845 |
| 2 | Lagged linear regression | 0.00072090 | 0.00137492 | 0.00724584 |
| 3 | Rolling historical volatility | 0.00061444 | 0.00139570 | 0.00754794 |
| 4 | LSTM | 0.00099818 | 0.00168735 | 0.00897661 |
| 5 | Random Forest | 0.00123057 | 0.00211129 | 0.01182354 |

Full data tables, predictions, target-window checks, test halves, regimes,
bootstrap intervals and expanding-window folds remain in `code/outputs/` and
are indexed in `appendix/model-results-summary.md`.
