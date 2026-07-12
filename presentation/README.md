# Presentation

This folder stores the 10-minute EPQ presentation planning materials and should later hold the final slide deck export.

Current support files:

- `slide-outline.md`: slide-by-slide speaking structure
- `qa-notes.md`: likely Q&A answers and defence points

## Current Slide Plan

1. Research question and motivation
2. Why cryptocurrency volatility matters
3. Methodology and models compared
4. Key results
5. Evaluation and limitations
6. Conclusion
7. Q&A preparation

## Current Key Messages

- The project compares rolling historical volatility, GARCH(1,1), lagged linear regression, Random Forest, and LSTM on Hyperliquid BTC daily data.
- The refreshed dataset currently runs from 2023-02-26 to the latest available daily candle on 2026-07-12.
- Correctly date-aligned GARCH produces the best RMSE for both 14-day and 30-day targets.
- LSTM improves on Random Forest but does not beat GARCH, lagged linear regression, or rolling historical volatility.
- The main evaluative conclusion is supported by accuracy, interpretability, measured local runtime, structural complexity, and robustness evidence.

## Evidence To Include

- one model-comparison table
- one forecast chart from `code/outputs/volatility_forecast_comparison.png`
- one short explanation of why realised volatility is only a proxy
- one slide on interpretability and practicality
- one compact 14-day/30-day robustness comparison
- one transparent note explaining the GARCH date-alignment correction
- short Q&A notes on why the implemented LSTM still did not overturn the main conclusion

## Presentation Evidence

The Production Log should include evidence that the presentation happened and that questions were answered.
