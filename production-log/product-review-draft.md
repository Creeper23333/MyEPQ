# Project Product Review Draft

## Project Product

The project product is a written EPQ report supported by reproducible code, model output files, research notes, and presentation materials. The central product is not only the numerical comparison table, but the overall critical evaluation of whether machine learning complexity is justified in Bitcoin volatility forecasting.

## What The Product Achieved

- A clear research question was maintained throughout the project.
- The project used exchange-level Hyperliquid BTC perpetual futures data rather than a generic finance website.
- The code pipeline became reproducible from data fetch to output generation.
- The final comparison includes rolling historical volatility, GARCH(1,1), lagged linear regression, Random Forest, and LSTM.
- The results support a balanced conclusion rather than a forced machine-learning victory.

## Strongest Features Of The Product

1. The project uses a clearly defined forecast target and chronological validation.
2. The final evaluation goes beyond error metrics and includes interpretability and practicality.
3. The modelling results are supported by saved outputs, not only by descriptive claims.
4. The project now compares both a tree-based and a sequence-based machine-learning model.

## Limitations Of The Product

1. Realised volatility is estimated from daily data and is only a proxy for true latent volatility.
2. The Random Forest implementation is lightweight rather than using scikit-learn.
3. The LSTM is intentionally small and not heavily tuned.
4. The project focuses on one market rather than a wider multi-asset comparison.

## Overall Evaluation

The product is strongest as an evaluative EPQ rather than as a search for the most advanced forecasting architecture. Its main value is that it produces a defensible answer: in this dataset and target setting, simple and interpretable models remain highly competitive, and greater complexity must justify itself with a clear improvement.
