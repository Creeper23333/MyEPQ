# Presentation

This folder stores the 10-minute EPQ presentation planning materials and should later hold the final slide deck export.

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
- The best RMSE is currently produced by lagged linear regression, with rolling historical volatility very close behind.
- LSTM improves on the Random Forest but still does not beat the strongest simple baselines.
- The main evaluative conclusion is that extra complexity is not automatically justified.

## Evidence To Include

- one model-comparison table
- one forecast chart from `code/outputs/volatility_forecast_comparison.png`
- one short explanation of why realised volatility is only a proxy
- one slide on interpretability and practicality
- short Q&A notes on why the implemented LSTM still did not overturn the main conclusion

## Presentation Evidence

The Production Log should include evidence that the presentation happened and that questions were answered.
