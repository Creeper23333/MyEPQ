# Presentation

This folder stores the final content specification, timed script and Q&A preparation for the 10-minute EPQ presentation. A `.pptx` still requires a compliant PowerPoint-authoring runtime and visual verification.

Current support files:

- `slide-outline.md`: slide-by-slide speaking structure
- `final-presentation-script.md`: timed, rehearsal-ready script
- `qa-notes.md`: likely Q&A answers and defence points

## Current Slide Plan

1. Research question
2. Why volatility, not price direction
3. Data and target
4. Fair comparison design
5. Five models and their roles
6. Main 30-day result
7. Robustness and uncertainty
8. Method-audit corrections
9. Accuracy, interpretation, cost and limitations
10. Answer and Q&A

## Current Key Messages

- The project compares rolling historical volatility, GARCH(1,1), lagged linear regression, Random Forest, and LSTM on Hyperliquid BTC daily data.
- The final dataset contains 1,240 completed candles from 2023-02-26 to 2026-07-19; one of 1,241 returned rows was still open and was excluded.
- All retained rows passed automated schema, cadence, OHLC, price and activity checks.
- Correctly date-aligned GARCH produces the best RMSE for both 14-day and 30-day targets.
- LSTM improves on Random Forest but does not beat GARCH, lagged linear regression, or rolling historical volatility.
- The main evaluative conclusion is supported by accuracy, interpretability, measured local runtime, structural complexity, and robustness evidence.
- GARCH also ranks first in both test-period halves, and its 30-day moving-block bootstrap interval versus rolling is entirely below zero.
- GARCH also ranks first in all four expanding-window blocks and in low-, medium-, and high-volatility target regimes.
- The frozen test cutoff, seven-new-day refresh comparison, Random Forest OOB versus future-test error and LSTM three-seed stability explain why the added model complexity did not generalise into an overall advantage.

## Evidence To Include

- one model-comparison table
- one forecast chart from `code/outputs/volatility_forecast_comparison.png`
- one short explanation of why realised volatility is only a proxy
- one slide on interpretability and practicality
- one compact 14-day/30-day robustness comparison
- one compact test-half/bootstrap uncertainty visual
- one compact expanding-window/regime callout
- one transparent audit slide covering date alignment, likelihood order, `E[s]` integration, duplicate-feature removal, the frozen cutoff and candle completion
- short Q&A notes on why the implemented LSTM still did not overturn the main conclusion

## Presentation Evidence

The Production Log should include evidence that the presentation happened and that questions were answered.
