# Source Evaluation Summary

This is the current audited source-evaluation summary. `research/Source_Evaluation_Tianlin_He.xlsx` is retained as the original spreadsheet evidence, but its dense layout and some earlier broad summaries were not suitable as the final authority; the evaluated roles and limitations below are the reconciled version used by the final report.

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

## What This Means For The EPQ

The literature does not support a simple assumption that machine learning will always be better. Huang, Sangiorgi and Urquhart (2024) provide strong recent evidence that neural networks can outperform GARCH in Bitcoin volatility forecasting, but Dudek et al. (2024) show that model performance depends on the cryptocurrency, forecast horizon, and metric. This supports a balanced final argument: accuracy matters, but it should be evaluated alongside interpretability, computational practicality, and risk-management usefulness.

The final audited results make this point clearer. GARCH(1,1) ranks first for both target windows, both halves of the primary test set, all four expanding-window test blocks and all three target-volatility regimes. Lagged linear regression and rolling historical volatility also outperform the implemented LSTM and lightweight Random Forest. A paired moving-block bootstrap supports GARCH's improvement over rolling but does not make the linear model's 1.8% RMSE improvement decisive. RF OOB versus future-test error and LSTM multi-seed results provide additional evidence about generalisation and optimisation stability. The literature should therefore frame a bounded result, not force a predetermined machine-learning victory or a universal GARCH claim.
