# Final 10-Minute Presentation Script

Use this as a speaking guide, not a paragraph-by-paragraph reading script. The timings total approximately ten minutes.

## Slide 1 — Research question (45 seconds)

My question is simple: did Random Forest or LSTM improve the forecast enough to justify the extra complexity? I chose four comparison points: error, stability, how easy the model was to explain and its practical cost. The recorded comparison uses rolling volatility and GARCH as benchmarks.

## Slide 2 — Why volatility? (45 seconds)

Volatility forecasting is different from predicting whether Bitcoin will rise or fall. It estimates the scale of uncertainty in future returns. That can inform position sizing, risk limits or awareness of stressful market conditions. My project is an academic model comparison, not trading advice, and it does not test profitability.

## Slide 3 — Data and target (60 seconds)

The saved dataset comes from Hyperliquid's BTC perpetual-futures market. The API returned 1,241 daily rows; the still-open final row was excluded, leaving 1,240 completed days through 19 July 2026. The target is tomorrow's updated 30-day volatility estimate. Because 29 days stay in the window, this is an update forecast, not a forecast of a completely new 30-day period or of unobserved true volatility.

## Slide 4 — Comparison design (55 seconds)

After preparation, the saved modelling table has 1,195 rows in time order. The fixed test start is 16 November 2025, leaving 950 training rows and 245 test rows. Random Forest and LSTM settings were chosen from training data only. Four expanding time blocks provide a separate check.

## Slide 5 — Models (50 seconds)

Rolling is the simplest benchmark. GARCH models changing variance. Linear regression checks whether simple lagged features are already enough. Random Forest handles nonlinear relationships in prepared features, while LSTM uses sequences. The models do not use exactly the same inputs. The result compares the tested pipelines, not model types in every possible design.

## Slide 6 — Main result (70 seconds)

Lower error is better. GARCH comes first, followed by linear regression, rolling, LSTM and Random Forest. QLIKE gives the same order as RMSE. GARCH's RMSE is 31% lower than rolling. Linear is only 1.9% lower by RMSE and has worse MAE, so that small difference is not decisive. Neither machine-learning model beats rolling overall.

The feature checks also show that both machine-learning models depend heavily on the current volatility estimate. That helps explain why the simple persistence-based methods are difficult to beat.

## Slide 7 — Robustness (65 seconds)

The comparison was repeated in several ways. GARCH stayed first for both target lengths, both halves of the test period, every expanding time block and every volatility group. LSTM beat rolling in two individual blocks, but not overall. The block bootstrap also gave a clear GARCH advantage over rolling, while linear regression's small advantage was uncertain. The saved run using data ending one week earlier kept all five ranks unchanged.

## Slide 8 — Method audit (60 seconds)

Several checks changed the method. Forecasts are now matched by date, the GARCH update happens in the correct order, and open candles and a duplicate input are excluded. The local forest was replaced with scikit-learn's version, model selection stays inside the training period and QLIKE was added. The full suite now has 43 passing tests. Code running without an error is not enough; the dates and formulas also have to be right.

## Slide 9 — Wider evaluation and limits (75 seconds)

GARCH has three reported parameters and took 0.53 seconds to fit on this computer. Random Forest adds scikit-learn, six settings and almost 58,000 tree nodes. LSTM adds PyTorch, four settings, early stopping, seed checks and about 5,900 weights. The timings are local and form only one part of the practical comparison.

The main limits are one exchange, one market history, a daily proxy and relatively small model searches. The models also use different inputs. This result applies to this comparison, not every Bitcoin forecast. Published studies using richer high-frequency data sometimes favour neural networks.

## Slide 10 — Conclusion (75 seconds)

In this project, Random Forest and LSTM added complexity without improving the forecast enough. GARCH had the lowest errors, stayed first in the extra checks and was easier to explain. Rolling remains the simplest fallback.

The finding is limited to these data and pipelines. Different data, richer features or another testing design could change the result. A stronger next study would keep a completely untouched future period and use higher-frequency data. Thank you - I am happy to take questions.

## Rehearsal checklist

- Aim for 9:30–10:00 before questions.
- Explain the volatility proxy without reading the formula.
- Say “perpetual futures”, not “Bitcoin spot”.
- Say “the frozen 2025-11-16 cutoff is primary; four-fold expanding-window is supplementary”.
- State that negative bootstrap differences favour the compared model.
- Say “current GARCH-based pipeline”, not “GARCH always beats LSTM”.
- Do not claim financial advice, profitability or universal GARCH superiority.
