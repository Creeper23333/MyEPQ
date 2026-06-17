# Literature Notes

Use this file to summarise sources in your own words.

## Note Template

```text
Source:
Main idea:
Useful evidence or concept:
How it supports my EPQ:
Limitations or possible bias:
```

## Notes

### Source 1: Katsiampa (2017)

Source: Katsiampa, P. (2017). Volatility estimation for Bitcoin: A comparison of GARCH models. Economics Letters.

Main idea: The paper compares GARCH-type models for Bitcoin volatility and shows that Bitcoin volatility can be analysed using established econometric volatility models.

Useful evidence or concept: GARCH models are suitable because they model volatility clustering, which is a common feature of financial returns.

How it supports my EPQ: This is a core source for selecting GARCH(1,1) as the traditional statistical benchmark.

Limitations or possible bias: The paper focuses on GARCH-family models rather than direct comparison with machine learning, so it cannot answer the full research question alone.

### Source 2: Hansen and Lunde (2005)

Source: Hansen, P. R., & Lunde, A. (2005). A forecast comparison of volatility models: Does anything beat a GARCH(1,1)? Journal of Applied Econometrics.

Main idea: The paper compares many ARCH-type models and asks whether more complex models reliably outperform GARCH(1,1).

Useful evidence or concept: It provides a strong justification for using GARCH(1,1) as a serious benchmark rather than treating it as a weak straw-man model.

How it supports my EPQ: It helps frame the project as a fair comparison. If machine learning only slightly beats GARCH, the advantage may not be practically meaningful.

Limitations or possible bias: It does not focus on cryptocurrency, so its findings need to be applied cautiously to Bitcoin.

### Source 3: Catania, Grassi and Ravazzolo (2019)

Source: Catania, L., Grassi, S., & Ravazzolo, F. (2019). Forecasting cryptocurrencies under model and parameter instability. International Journal of Forecasting.

Main idea: Cryptocurrency forecasting is affected by model and parameter instability, meaning that a model that works in one market period may not remain best later.

Useful evidence or concept: Forecasting performance should be tested out-of-sample and discussed in terms of stability, not only in-sample fit.

How it supports my EPQ: This supports using chronological validation and discussing robustness as part of the evaluation.

Limitations or possible bias: The paper studies a broader set of forecasting models and cryptocurrencies, so the exact method is more advanced than this EPQ can reproduce.

### Source 4: Dudek et al. (2024)

Source: Dudek, G., Fiszeder, P., Kobus, P., & Orzeszko, W. (2024). Forecasting cryptocurrencies volatility using statistical and machine learning methods: A comparative study. Applied Soft Computing.

Main idea: The paper compares many statistical and machine learning models, including GARCH, Random Forest, and LSTM, for daily and weekly cryptocurrency volatility.

Useful evidence or concept: It finds that there is no single best method for every cryptocurrency, metric, or forecast horizon; simpler models can sometimes perform as well as complex ML models.

How it supports my EPQ: This is one of the strongest sources for the project's critical angle: the final answer may need to balance accuracy with interpretability and context.

Limitations or possible bias: The paper uses realised variance from intraday returns, while this EPQ starts with daily Hyperliquid candles, so the target variable is less precise.

### Source 5: Huang, Sangiorgi and Urquhart (2024)

Source: Huang, Z.-C., Sangiorgi, I., & Urquhart, A. (2024). Forecasting Bitcoin volatility using machine learning techniques. Journal of International Financial Markets, Institutions and Money.

Main idea: The paper directly compares neural-network methods such as LSTM and CNN-LSTM against traditional volatility models for Bitcoin volatility forecasting.

Useful evidence or concept: It reports that neural networks outperform GARCH models across forecast horizons in that study.

How it supports my EPQ: This source provides recent evidence in favour of machine learning and gives a benchmark for what my project is testing on a smaller scale.

Limitations or possible bias: The methods are more advanced than an EPQ implementation, so I should not overclaim that my simpler LSTM will reproduce the same performance.

### Source 6: Shen, Wan and Leatham (2021)

Source: Shen, Z., Wan, Q., & Leatham, D. J. (2021). Bitcoin return volatility forecasting: A comparative study between GARCH and RNN. Journal of Risk and Financial Management.

Main idea: The paper compares a conventional GARCH model with a recurrent neural network for forecasting Bitcoin return volatility and risk measures.

Useful evidence or concept: It is useful evidence that RNN-type models can be considered alongside GARCH for Bitcoin volatility.

How it supports my EPQ: It supports the choice of LSTM as a sequence model rather than using only tree-based machine learning.

Limitations or possible bias: It compares RNN-style models rather than the exact Random Forest + LSTM pair used in this EPQ.

### Source 7: Zahid, Iqbal and Koutmos (2022)

Source: Zahid, M., Iqbal, F., & Koutmos, D. (2022). Forecasting Bitcoin volatility using hybrid GARCH models with machine learning. Risks.

Main idea: Hybrid models combine GARCH-type volatility structure with deep learning methods to forecast Bitcoin realised volatility.

Useful evidence or concept: This suggests that statistical and machine learning methods should not be viewed as complete opposites; hybrid approaches can exploit both.

How it supports my EPQ: It helps the discussion section consider whether a future extension should combine model types instead of choosing one winner.

Limitations or possible bias: The hybrid design is beyond the minimum EPQ scope and may not be feasible to implement within the available time.

### Source 8: Brauneis and Sahiner (2026)

Source: Brauneis, A., & Sahiner, M. (2026). Crypto volatility forecasting: Mounting a HAR, sentiment, and machine learning horserace. Asia-Pacific Financial Markets.

Main idea: The paper compares a HAR benchmark with machine learning models and investigates whether sentiment data improves crypto volatility forecasts.

Useful evidence or concept: It shows that machine learning can capture non-linear sentiment effects, but that there is no single definitive best ML model.

How it supports my EPQ: It supports the optional future extension of adding sentiment data and strengthens the argument that model performance depends on inputs and context.

Limitations or possible bias: Sentiment data is outside the current core scope, so this source is mainly useful for evaluation and future improvements.

### Source 9: Bollerslev (1986)

Source: Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. Journal of Econometrics.

Main idea: This is the foundational GARCH paper, introducing a model where current conditional variance depends on past shocks and past variance.

Useful evidence or concept: The GARCH(1,1) formula is central to the mathematical formulation section.

How it supports my EPQ: It provides theoretical grounding for the traditional model rather than relying only on later application papers.

Limitations or possible bias: It is not about Bitcoin or machine learning, so it is a methodological source rather than evidence about crypto forecasting performance.

### Source 10: Breiman (2001)

Source: Breiman, L. (2001). Random forests. Machine Learning.

Main idea: Random Forests combine many decision trees using randomness and averaging to improve predictive performance.

Useful evidence or concept: Random Forests are less opaque than neural networks because feature importance can be inspected, although they are still more complex than GARCH.

How it supports my EPQ: It justifies the choice of Random Forest as the first machine learning model before attempting LSTM.

Limitations or possible bias: The paper is not designed for time-series volatility forecasting, so lagged features must be engineered carefully.

### Source 11: Hochreiter and Schmidhuber (1997)

Source: Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. Neural Computation.

Main idea: LSTM networks are designed to learn long-term dependencies in sequential data.

Useful evidence or concept: The model is relevant because Bitcoin volatility may depend on previous sequences of returns and volatility.

How it supports my EPQ: It provides the theoretical justification for including LSTM as the main deep learning model.

Limitations or possible bias: LSTM models require careful scaling, training, and validation, which creates overfitting risk in a small project.

### Source 12: Lundberg and Lee (2017) / Molnar (2025)

Source: Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions; Molnar, C. (2025). Interpretable machine learning.

Main idea: Model interpretability matters because complex models can be accurate while still difficult to trust or explain.

Useful evidence or concept: SHAP and model-agnostic interpretability methods can help explain black-box models, but they add extra complexity.

How it supports my EPQ: These sources support the supervisor's comment that comparison should include interpretability, not only numerical accuracy.

Limitations or possible bias: Interpretability sources are general machine learning sources, not specific to Bitcoin volatility.
