# Slide Outline

## Slide 1: Title and Research Question

- Title: Machine Learning vs Traditional Models in Bitcoin Volatility Forecasting
- Research question:
  How do Random Forest and LSTM compare with rolling historical volatility and GARCH(1,1) in terms of forecasting accuracy, interpretability, computational practicality, and robustness?
- Why this matters:
  volatility affects risk, position sizing, and market uncertainty

## Slide 2: Why Bitcoin Volatility Matters

- Bitcoin is highly volatile compared with many traditional assets.
- Forecasting volatility matters for risk management, not only for price prediction.
- The project focuses on Hyperliquid BTC perpetual futures rather than generic spot BTC data.

## Slide 3: Data Source and Method

- Source: Hyperliquid public info API daily candles
- Current sample:
  2023-02-26 to latest available daily candle on 2026-07-12
- Processing:
  close prices -> log returns -> 30-day realised volatility proxy
- Forecast target:
  next-day 30-day realised volatility
- Validation:
  chronological split, not random split

## Slide 4: Models Compared

- Rolling historical volatility:
  simple persistence benchmark
- GARCH(1,1):
  traditional volatility model
- Lagged linear regression:
  interpretable lag-feature comparison
- Random Forest:
  tree-based machine learning model
- LSTM:
  sequence-based neural network

## Slide 5: Main Results

Use the ranking table:

| Rank | Model | RMSE |
| --- | --- | --- |
| 1 | GARCH(1,1) | 0.00099637 |
| 2 | Lagged linear regression | 0.00141843 |
| 3 | Rolling historical volatility | 0.00144481 |
| 4 | LSTM | 0.00184029 |
| 5 | Random Forest | 0.00212715 |

Key takeaway:
the best result does not come from the most complex model

## Slide 6: What The Results Mean

- GARCH performs best after predictions are correctly aligned to test dates, showing why implementation validation matters.
- Rolling historical volatility and lagged linear regression remain competitive because persistence features are strong.
- LSTM improves on Random Forest, so sequence modelling does add some value.
- However, neither machine-learning model beats GARCH, lagged linear regression, or the rolling benchmark.

## Slide 7: Evaluation Beyond Accuracy

- Interpretability:
  rolling volatility and lagged linear regression are easier to explain
- Computational practicality:
  measured fit/prediction time and model-size evidence replace unsupported assumptions
- Robustness:
  GARCH ranks first for both 14-day and 30-day targets
- Practical usefulness:
  extra complexity must justify itself with a clear improvement

## Slide 8: Limitations

- Realised volatility is a proxy, not true latent volatility.
- The dataset uses daily candles, not intraday realised variance.
- The project uses one core market rather than many assets.
- Results may depend on the target definition and feature set.

## Slide 9: Conclusion

- Machine learning does not automatically improve Bitcoin volatility forecasting.
- In this project, simple and interpretable models remain highly competitive.
- The most balanced conclusion is that complexity should only be preferred when the gain is large enough to justify it.

## Slide 10: Q&A Prompt Slide

- Why did the simple models do so well?
- Why did the corrected GARCH model perform best?
- Why did LSTM still not win?
- What would be the next improvement if the project continued?
