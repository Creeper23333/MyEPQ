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
- The refreshed dataset contains 1,271 completed candles from 2023-02-26 to 2026-08-19; the still-open 20 August row was excluded from 1,272 returned rows.
- All retained rows passed automated schema, cadence, OHLC, price and activity checks.
- The 30-day target is tomorrow's updated rolling proxy; 29 of its returns are already known at the forecast origin.
- Correctly date-aligned GARCH produces the best RMSE and QLIKE for both 14-day and 30-day targets.
- LSTM improves on Random Forest but does not beat GARCH, lagged linear regression, or rolling historical volatility.
- The main evaluative conclusion is supported by accuracy, robustness, produced explanations, dependency/tuning burden, local runtime and structural complexity.
- GARCH also ranks first in both test-period halves, and its 30-day moving-block bootstrap interval versus rolling is entirely below zero.
- GARCH also ranks first in all four expanding-window blocks and in low-, medium-, and high-volatility target regimes.
- RF is the standard scikit-learn implementation; RF and LSTM use compact chronological training-only tuning.
- The frozen cutoff, refresh comparison, RF OOB evidence, LSTM three-seed stability and LSTM input ablation explain why added complexity did not generalise into an overall advantage.
- The 31 new completed targets retain all five overall ranks. Random Forest is closest on the final 19 August shock target, but one observed holdout date is not an overall improvement and must not be used for post-hoc tuning.
- Conclusions compare the current GARCH-based and direct-target ML pipelines; they do not establish universal GARCH superiority.

## Evidence To Include

- one model-comparison table
- one QLIKE callout showing that the variance-scale ranking agrees with RMSE
- one forecast chart from `code/outputs/volatility_forecast_comparison.png`
- one short explanation of why realised volatility is only a proxy
- one slide on interpretability and practicality
- one compact 14-day/30-day robustness comparison
- one compact test-half/bootstrap uncertainty visual
- one compact expanding-window/regime callout
- one transparent audit slide covering date alignment, likelihood order, `E[s]` integration, duplicate-feature removal, the frozen cutoff, candle completion, standard RF and training-only tuning
- short Q&A notes on why the implemented LSTM still did not overturn the main conclusion

## Presentation Evidence

The Production Log should include evidence that the presentation happened and that questions were answered.
