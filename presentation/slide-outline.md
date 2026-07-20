# Final Presentation Specification

Ten slides for a 10-minute presentation. Keep visible text concise; the detailed wording belongs in `presentation/final-presentation-script.md`.

## Slide 1 — Research question (0:00–0:45)

**Title:** When is a more complex volatility model worth it?

**Visible content:**

- Bitcoin volatility forecasting
- Random Forest and LSTM versus rolling volatility and GARCH(1,1)
- Accuracy · interpretability · practicality · robustness

**Visual:** dark BTC price/volatility motif with the research question as the main editable text.

## Slide 2 — Why volatility, not price direction? (0:45–1:30)

**Visible content:**

- Direction: will price rise or fall?
- Volatility: how uncertain are returns?
- Use: position size, risk limits, stress awareness

**Visual:** two-column contrast between a direction arrow and an uncertainty band. Do not imply financial advice.

## Slide 3 — Data and target (1:30–2:30)

**Visible content:**

- Hyperliquid BTC perpetual-futures daily candles
- 1,241 API rows → 1 still open excluded → 1,240 completed rows
- 2023-02-26 to 2026-07-19
- Target: next-day updated 30-day standard deviation of log returns

**Visual:** timeline showing raw archive, log return, rolling volatility and one-day-ahead target. Add a small warning label: “proxy, not latent volatility”.

## Slide 4 — Fair comparison design (2:30–3:25)

**Visible content:**

- 1,195 modelling rows
- 950 frozen train | 245 expanding test
- Test origins fixed from 2025-11-16; no random shuffling
- Supplementary four-fold expanding-window refitting
- Same target and dates for every model

**Visual:** horizontal train/test timeline, with the final 15% of LSTM training sequences marked as internal validation. Distinguish the primary fixed holdout from the supplementary four-block expanding-window check.

## Slide 5 — Five models, five roles (3:25–4:15)

| Model | Role | Main explanation evidence |
| --- | --- | --- |
| Rolling | persistence benchmark | one rule |
| GARCH(1,1) | conditional-variance model | omega, alpha, beta |
| Linear | auxiliary lag-feature check | signed coefficients |
| Random Forest | nonlinear ML | global feature importance |
| LSTM | sequential ML | architecture and training history |

**Visual:** five compact cards ordered from transparent to structurally complex.

## Slide 6 — Main 30-day result (4:15–5:25)

Use a native horizontal bar chart of RMSE; lower is better.

| Model | RMSE |
| --- | ---: |
| GARCH(1,1) | 0.00098502 |
| Lagged linear regression | 0.00140087 |
| Rolling historical volatility | 0.00142744 |
| LSTM | 0.00174351 |
| Random Forest | 0.00232370 |

**Callout:** GARCH RMSE is 31.0% below rolling. Linear improves RMSE by only 1.9% and has worse MAE than rolling.

## Slide 7 — Is the result robust? (5:25–6:30)

**Visible content:**

- GARCH ranks first for 14-day and 30-day targets
- GARCH ranks first in both halves of the test period
- GARCH ranks first in all four expanding-window blocks and all three target-volatility regimes
- RMSE difference vs rolling, 30-day block bootstrap:
  `-0.00044242`, 95% interval `[-0.00099670, -0.00017158]`
- Linear interval crosses zero
- Same-code 2026-07-12 cut preserves all five ranks; seven new targets change RMSE by only 0.8–1.4%

**Visual:** two small ranking columns for 14/30 days and one confidence-interval plot. Negative values favour the model.

## Slide 8 — What the audit changed (6:30–7:30)

**Visible content:**

1. Map forecasts by date, not reset row number
2. Score return before its shock updates the next GARCH variance
3. Estimate the standard-deviation target as `E[s]`; retain `sqrt(E[s²])` as a sensitivity
4. Remove the duplicate target-window predictor and freeze the test cutoff
5. Exclude candles that have not ended

**Callout:** Reproducibility requires tests and conceptual checks, not only saved code.

**Visual:** four-step audit flow from invalid assumption to test to corrected output.

## Slide 9 — Accuracy is not the only cost (7:30–8:45)

| Model | Fit time | Structure | Interpretability |
| --- | ---: | --- | --- |
| GARCH | 1.00 s | 3 parameters | High |
| LSTM | 5.42 s | 5,921 parameters | Low |
| Random Forest | 5.41 s | 17,984 nodes | Medium |

**Visible limitations:** one exchange, daily proxy, one market history, limited ML tuning, no portfolio/VaR test.

**Visual:** trade-off triangle: accuracy, transparency and implementation cost.

## Slide 10 — Answer and Q&A (8:45–10:00)

**Visible conclusion:**

> Under this Hyperliquid daily-data design, Random Forest and LSTM do not justify their extra complexity. GARCH is the most defensible overall model.

**Boundary:** This is not proof that machine learning can never work. An untouched future period, high-frequency data, richer features, finer rolling-origin tests or hybrid models could change the ranking.

**Q&A prompts:** Why is the target persistent? Why did the audit matter? What would I improve next?

## Evidence sources for the deck

- `report/final-report.md`
- `code/outputs/model_performance.csv`
- `code/outputs/model_robustness_by_window.csv`
- `code/outputs/model_robustness_by_test_segment.csv`
- `code/outputs/model_rmse_block_bootstrap.csv`
- `code/outputs/model_walk_forward_performance.csv`
- `code/outputs/model_performance_by_volatility_regime.csv`
- `code/outputs/model_computational_profile.csv`
- `code/outputs/garch_target_conversion_sensitivity.csv`
- `code/outputs/model_refresh_stability.csv`
- `code/outputs/volatility_forecast_comparison.png`
