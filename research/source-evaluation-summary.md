# Source Evaluation Summary

This summary puts the sources, their uses and their main limits in one readable table. The original spreadsheet remains at `research/Source_Evaluation_Tianlin_He.xlsx`.

The credibility scores are internal project judgments used to compare relevance, peer review, recency and methodological fit; they are not objective quality ratings.

| No | Source | Role in project | Credibility | Main limitation |
| --- | --- | --- | --- | --- |
| 1 | Katsiampa (2017) | Bitcoin GARCH benchmark | 9.5/10 | Focuses on GARCH models, not machine learning |
| 2 | Hansen and Lunde (2005) | Justifies GARCH(1,1) as a serious benchmark | 9.5/10 | Not cryptocurrency-specific |
| 3 | Catania, Grassi and Ravazzolo (2019) | Supports robustness and model-instability discussion | 9/10 | Uses more advanced methods than this EPQ can reproduce |
| 4 | Dudek et al. (2024) | Direct comparison of GARCH, Random Forest, LSTM and other methods | 10/10 | Uses intraday realised variance, while this EPQ uses daily Hyperliquid candles |
| 5 | Huang, Sangiorgi and Urquhart (2024) | Recent evidence that neural networks can outperform GARCH for Bitcoin volatility | 10/10 | More advanced neural-network setup than the EPQ implementation |
| 6 | Shen, Wan and Leatham (2021) | Supports RNN/LSTM-style modelling for Bitcoin volatility | 8.5/10 | Earlier and narrower than newer ML studies |
| 7 | Zahid, Iqbal and Koutmos (2022) | Shows possible hybrid GARCH + ML extension | 8.5/10 | Hybrid models are outside core scope |
| 8 | Brauneis and Sahiner (2026) | Supports sentiment/ML future extension and nonlinear crypto-volatility discussion | 9/10 | Sentiment data is not in the first implementation |
| 9 | Bollerslev (1986) | Foundational GARCH theory | 10/10 | Methodological, not crypto-specific |
| 10 | Breiman (2001) | Foundational Random Forest theory | 10/10 | Does not directly address time-series forecasting |
| 11 | Hochreiter and Schmidhuber (1997) | Foundational LSTM theory | 10/10 | Explains architecture, not crypto application |
| 12 | Lundberg and Lee (2017) | Supports interpretability discussion through SHAP | 9/10 | General ML interpretability rather than finance-specific |
| 13 | Patton (2011) | Justifies robust loss functions when volatility proxies are imperfect | 10/10 | Its proxy-consistency result does not make this overlapping 30-day daily proxy equivalent to latent conditional variance |

## Comparison of Sources and the Present Design

| Source | What its evidence suggests | Important design difference | How it is used |
| --- | --- | --- | --- |
| Hansen and Lunde (2005) | GARCH(1,1) can be a demanding benchmark | Exchange-rate/equity evidence, not cryptocurrency and not this proxy | Justifies a serious statistical comparator, not a predicted winner |
| Dudek et al. (2024) | Rankings vary across cryptoassets, models, horizons and metrics | Uses richer intraday realised variance | Supports conditional conclusions and multiple metrics |
| Huang, Sangiorgi and Urquhart (2024) | Neural networks can outperform GARCH for Bitcoin | High-frequency inputs, more observations and more advanced architectures | Prevents the current LSTM result becoming a universal anti-ML claim |
| Shen, Wan and Leatham (2021) | Recurrent models can improve average errors but weaken in extreme-risk tasks | Different target, model and evaluation design | Motivates regime checks and caution about stress-period performance |
| Zahid, Iqbal and Koutmos (2022) | Hybrid GARCH-ML designs can add value | Hybrid rather than matched standalone pipelines | Supports a future matched-pipeline extension |
| Patton (2011) | Proxy choice and loss function can affect ranking | The current target is an overlapping rolling standard deviation from daily returns | Motivates QLIKE while preserving explicit proxy limitations |
| Breiman (2001) and Hochreiter and Schmidhuber (1997) | RF and LSTM provide nonlinear tabular and recurrent structures | Foundational architecture papers do not validate this implementation or dataset | Justifies model inclusion, not a claim that nonlinearity caused any result |

## What This Means For The EPQ

The literature does not support a simple assumption that machine learning will always be better. Huang, Sangiorgi and Urquhart (2024) provide strong recent evidence that neural networks can outperform GARCH in Bitcoin volatility forecasting, but Dudek et al. (2024) show that model performance depends on the cryptocurrency, forecast horizon, and metric. This supports a balanced final argument: accuracy matters, but it should be evaluated alongside interpretability, computational practicality, and risk-management usefulness.

The project results follow the same cautious pattern. GARCH(1,1) ranks first by RMSE and QLIKE in both target windows, both test halves, all four expanding-window blocks and all three volatility groups. Linear regression and rolling also outperform the tested LSTM and scikit-learn Random Forest. The bootstrap supports GARCH's improvement over rolling but not a decisive 1.8% linear-model gain. Because the models use different inputs and transformations, the result applies to the methods tested here rather than proving a universal model ranking.
