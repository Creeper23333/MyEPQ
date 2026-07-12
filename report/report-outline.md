# EPQ Report Outline

## Proposed Title

To what extent can machine learning models improve Bitcoin volatility forecasting compared with traditional statistical models?

## Research Question

To what extent can machine learning models, specifically Random Forest and Long Short-Term Memory networks, improve Bitcoin volatility forecasting compared with traditional statistical models such as rolling historical volatility and GARCH(1,1)?

## Aims and Objectives

**Aim:**
To critically evaluate the predictive power, interpretability, computational practicality, and risk-management usefulness of machine learning approaches compared with traditional statistical approaches in cryptocurrency volatility forecasting.

**Objectives:**

1. Define logarithmic returns and realised volatility in a way that can be calculated from Hyperliquid OHLCV candle data.
2. Implement baseline statistical models: rolling historical volatility and GARCH(1,1).
3. Implement two machine learning models: Random Forest regression and LSTM.
4. Compare the models using MAE, MSE, and RMSE.
5. Evaluate whether any accuracy improvement is meaningful once interpretability and project feasibility are considered.

## 1. Introduction

- Explain cryptocurrency and Bitcoin as a high-volatility financial asset.
- Define volatility and why forecasting volatility matters for risk management.
- Introduce the research question and explain why model comparison is useful but should not be reduced to a single metric.
- Briefly state the models and evaluation approach.
- Explain why Bitcoin is used as the main case study: long data history, market relevance, and high volatility.

## 2. Literature Review

- Volatility forecasting in financial markets.
- Cryptocurrency volatility and market instability.
- Traditional statistical approaches such as rolling volatility and GARCH.
- Machine learning approaches for financial time series forecasting.
- Interpretability as a limitation of machine learning models.
- Limitations of previous research, especially in cryptocurrency markets.
- Key tension to develop: complex models may improve accuracy, but this does not automatically make them more useful for a small investor or risk manager.
- Current draft file: `report/literature-review-draft.md`

## 3. Mathematical Formulation

- Logarithmic return:

```text
r_t = ln(P_t / P_{t-1})
```

- Rolling realised volatility over a window of n days:

```text
RV_t = sqrt((1 / (n - 1)) * sum((r_i - mean(r))^2))
```

- GARCH(1,1) conditional variance:

```text
sigma_t^2 = omega + alpha * epsilon_{t-1}^2 + beta * sigma_{t-1}^2
```

- Forecast-error metrics:

```text
MAE = mean(|y_t - yhat_t|)
MSE = mean((y_t - yhat_t)^2)
RMSE = sqrt(MSE)
```

- Current draft file: `report/mathematical-formulation-draft.md`

## 4. Methodology and Data Source

- Data source and selected period.
- Hyperliquid API request structure and candle fields.
- Current request window: 2023-02-26 to 2026-07-13.
- Latest available returned daily candle in the refreshed dataset: 2026-07-12.
- Data cleaning and calculation of log returns.
- Definition of realised volatility.
- Description of each model.
- Walk-forward validation rather than one random train/test split, because financial time series must preserve chronological order.
- Evaluation metrics: MAE, MSE, and RMSE.
- Secondary evaluation dimensions: interpretability, computational practicality, and suitability for risk-management use.

## 5. Results

- Present model performance table.
- Include a chart comparing actual realised volatility with selected model forecasts.
- Include a summary table ranking models by error metrics.
- Use `report/results-draft.md` as the first-pass written results section.
- Use `code/outputs/volatility_forecast_comparison.png` as the first forecast comparison chart.
- Current refreshed best RMSE: lagged linear regression (`0.00141843`).

## 6. Comparative Analysis and Discussion

- Accuracy: Does Random Forest or LSTM reduce MAE/RMSE compared with historical volatility and GARCH(1,1)?
- Current answer from the first-pass results: LSTM improves on Random Forest but not on lagged linear regression or rolling historical volatility.
- Interpretability: Can the model's forecasts be explained clearly enough for an EPQ-level report?
- Computational practicality: How hard is the model to implement, tune, and reproduce?
- Robustness: Are results stable across different forecast windows, or dependent on one period of Bitcoin market behaviour?
- Practical usefulness: Would the forecast help a risk-management decision, or is it only a numerical improvement?
- Current draft file: `report/discussion-draft.md`

## 7. Conclusion

- Directly answer the research question.
- Summarise whether machine learning improved volatility forecasting.
- State whether the improvement was worth the loss of interpretability.
- Suggest realistic improvements, such as adding sentiment data or using high-frequency data.
- Current draft file: `report/conclusion-draft.md`

## Current Assembly

- A stitched full-report working draft is available in `report/full-report-draft.md`.

## Report Evaluation Points To Remember

- Avoid claiming that a model is "better" only because it has the lowest error in one test.
- Acknowledge that realised volatility is a proxy for latent volatility, not the true unobservable volatility.
- Discuss overfitting risk, especially for LSTM.
- Explain why Ethereum is left as an optional extension rather than part of the core project.

## References

- Use one consistent referencing style.
- Keep all sources recorded in `research/sources.md`.
