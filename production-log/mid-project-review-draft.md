# Mid-Project Review Draft

## Current Stage

By the mid-project point, the project should have a refined research question, evaluated sources, a clear methodology, and the first version of the modelling plan. The most important development so far is that the project is no longer a simple "machine learning versus statistics" comparison. The comparison now includes accuracy, interpretability, computational practicality, and practical usefulness.

## What Has Gone Well

- The research question has been narrowed to Bitcoin volatility forecasting.
- The traditional model choice has been clarified: rolling historical volatility will be the simple baseline, while GARCH(1,1) will be the main statistical model.
- The machine learning models have been narrowed to Random Forest and LSTM.
- Initial literature research has identified sources that both support and challenge the idea that machine learning is always better.
- The project now has a clearer critical angle: model complexity must be justified by meaningful improvement.

## Problems or Limitations Found

- Bitcoin volatility is difficult to forecast because the market is unstable and affected by shocks.
- Realised volatility calculated from daily data is only a proxy for true volatility.
- LSTM may be hard to tune and explain within the EPQ time limit.
- Some academic studies use intraday data or more advanced features, while this project starts with daily Hyperliquid candles.
- Accuracy metrics alone may not capture whether a forecast is useful in practice.

## Changes to the Plan

The project will not attempt too many cryptocurrencies or too many machine learning models. Bitcoin remains the core asset, and Ethereum is only an optional extension. Random Forest is prioritised before LSTM because it is easier to implement and explain. The literature review and discussion will explicitly include interpretability so that the project demonstrates critical thinking even if the model implementation remains small-scale.

## What I Need To Do Next

1. Complete the data collection and cleaning workflow.
2. Implement the baseline and GARCH(1,1) models.
3. Implement Random Forest and compare it with the statistical models.
4. Attempt LSTM if time allows.
5. Produce a results table and at least one forecast chart.
6. Draft the methodology and results sections.

## Reflection

The main lesson so far is that a more complex model is not automatically a better model. The project needs to judge whether the improvement in forecast accuracy is large enough to justify the extra complexity. This makes the final answer more balanced and should help the report avoid becoming just a list of error metrics.
