# Full Report Draft

## Title

Accuracy, Interpretability and Practicality in Bitcoin Volatility Forecasting: Machine Learning versus Statistical Models

## Introduction

Bitcoin prices can change sharply over short periods, making volatility important for traders, investors, and risk managers. Forecasting volatility is different from forecasting price direction: it estimates the scale of uncertainty in future returns. A useful forecast may support position sizing, risk limits, or recognition of changing market conditions.

This project asks:

> How do Random Forest and Long Short-Term Memory networks compare with rolling historical volatility and GARCH(1,1) when forecasting Bitcoin volatility, in terms of accuracy, interpretability, computational practicality, and robustness?

The wording avoids assuming that machine learning must improve the result. Random Forest can model nonlinear feature interactions, while LSTM is designed for ordered sequences. However, rolling historical volatility and GARCH are transparent methods designed around persistence and volatility clustering. The project therefore tests whether additional model complexity is justified rather than selecting a winner from RMSE alone.

The aim is to evaluate predictive error, explanation evidence, local computational cost, structural complexity, reproducibility, robustness across target definitions, and suitability for risk interpretation. The practical question is whether an accuracy gain is large and stable enough to compensate for a model becoming harder to explain and reproduce.

## Literature Review

Bollerslev (1986) provides the basis for GARCH, where current conditional variance depends on previous shocks and variance. Hansen and Lunde (2005) show why GARCH(1,1) remains a serious volatility benchmark. Katsiampa (2017) applies GARCH-family methods to Bitcoin, while Catania, Grassi and Ravazzolo (2019) stress instability in cryptocurrency forecasting and the need for out-of-sample evaluation.

Machine-learning evidence is mixed. Dudek et al. (2024) compare statistical and machine-learning methods across cryptocurrencies and find that no method dominates every asset, metric, and horizon. Huang, Sangiorgi and Urquhart (2024) report stronger neural-network results for Bitcoin in their setting, and Shen, Wan and Leatham (2021) support recurrent networks as relevant comparators to GARCH. Differences in input data, target construction, tuning, and forecast horizon make direct replication difficult at EPQ scale.

Breiman (2001) supports Random Forest as a nonlinear ensemble method, while Hochreiter and Schmidhuber (1997) establish LSTM for long-term sequential dependencies. Lundberg and Lee (2017) and Molnar (2025) show why predictive accuracy and interpretability should be separated. A complex model can be accurate without giving a direct explanation, so lower error is not automatically equivalent to greater practical usefulness.

## Mathematical Formulation

Daily logarithmic return is:

```text
r_t = ln(P_t / P_(t-1))
```

The primary realised-volatility proxy is the sample standard deviation of 30 daily returns:

```text
RV_t(30) = stdev(r_(t-29), ..., r_t)
```

The forecasting target at information date `t` is `RV_(t+1)`. GARCH(1,1) uses:

```text
sigma_t^2 = omega + alpha * epsilon_(t-1)^2 + beta * sigma_(t-1)^2
```

Forecast accuracy is measured by MAE, MSE, and RMSE. MAE measures typical absolute deviation, while RMSE penalises larger errors more strongly.

## Methodology

The dataset contains 1,233 Hyperliquid BTC perpetual-futures daily candles from 2023-02-26 to 2026-07-12. Hyperliquid was selected instead of Yahoo Finance because it provides exchange-level data for the specific market studied. Close prices are converted into log returns, then into 30-day realised volatility. A 14-day target is calculated from the same returns for robustness testing.

Features include current and lagged returns, absolute returns, current and lagged realised volatility, log volume, log trade count, and rolling return summaries. Scaling statistics are fitted on training data only. The primary modelling frame has 1,188 rows. A fixed chronological 80/20 holdout produces 950 training rows from 2023-04-11 to 2025-11-15 and 238 test rows from 2025-11-16 to 2026-07-11. This is not a walk-forward refit. LSTM separately uses a chronological validation segment within the training period for early stopping.

Five models are compared: a rolling persistence benchmark; GARCH(1,1) fitted by deterministic grid-search likelihood; ridge-stabilised lagged linear regression; a 160-tree project-local Random Forest; and a PyTorch LSTM with 32 hidden units and a 30-observation input sequence.

Accuracy is evaluated using MAE, MSE, RMSE, and RMSE relative to the rolling benchmark. Interpretability evidence is model-specific: formula, parameters, coefficients, feature importance, or documented architecture limitations. Computational evidence records fit time, prediction time, and structural size during the same local run. Robustness reruns the complete model set for 14-day and 30-day targets.

An implementation audit found that earlier GARCH forecasts had been selected by reset row index after feature engineering removed incomplete rows. The corrected pipeline maps every forecast to its test observation by date and fails if alignment is incomplete. Only corrected results are used below.

## Results

| Rank | Model | Category | MAE | MSE | RMSE |
| --- | --- | --- | --- | --- | --- |
| 1 | GARCH(1,1) | Traditional statistical | 0.00047808 | 0.00000099 | 0.00099637 |
| 2 | Lagged linear regression | Interpretable lag-feature model | 0.00074798 | 0.00000201 | 0.00141843 |
| 3 | Rolling historical volatility | Benchmark | 0.00063564 | 0.00000209 | 0.00144481 |
| 4 | LSTM | Machine learning | 0.00106690 | 0.00000339 | 0.00184029 |
| 5 | Random Forest | Machine learning | 0.00122445 | 0.00000452 | 0.00212715 |

GARCH improves RMSE by approximately 31.0% relative to rolling historical volatility on the 30-day target. Linear regression improves RMSE by only 1.8% and has a higher MAE than rolling. LSTM and Random Forest are approximately 27.4% and 47.2% worse than rolling by RMSE.

For the 14-day target, the ranking remains GARCH, linear regression, rolling, LSTM, then Random Forest. GARCH RMSE is `0.00179214`, approximately 35.7% below the 14-day rolling benchmark. Maintaining the same full ranking across both windows strengthens the result, while still leaving open whether it would survive other markets or regimes.

The current local run shows a large practicality gap. Rolling requires no fitting, linear regression fits in less than one millisecond, GARCH takes roughly 0.6 seconds, and the two machine-learning implementations take several seconds. GARCH has three fitted parameters, linear regression 27 coefficients, LSTM 6,049 trainable parameters, and Random Forest 18,036 fitted tree nodes. Timing is machine-specific and these complexity units are descriptive rather than directly equivalent.

## Comparative Analysis and Discussion

GARCH provides the strongest current combination of accuracy and interpretability. Its parameters have established meanings related to baseline variance, shock response, and persistence, and it ranks first at both target windows. The rolling-target conversion remains a methodological assumption, but robustness across 14 and 30 days reduces the likelihood that its result is a single-window accident.

Rolling historical volatility remains a valuable benchmark because next-day rolling volatility overlaps with today's window. Linear regression also benefits from explicit persistence features. Its small RMSE gain over rolling should not be overstated because its MAE is worse and correlated lag features complicate coefficient interpretation.

Random Forest feature importance shows that current realised volatility, 30-day rolling return standard deviation, and recent volatility lags dominate. The model is therefore largely recovering persistence through a much larger structure. LSTM captures sequential information and improves on Random Forest, but it remains behind all three simpler alternatives. Neither machine-learning model produces an accuracy gain to offset its reduced transparency.

Interpretability is not treated as a vague claim. Rolling has a one-rule explanation; GARCH has three named parameters; linear regression exports every coefficient; Random Forest exports global importance but not direction or local explanation; and LSTM records architecture and training history but cannot directly explain a prediction. This evidence supports the high, medium, and low interpretability assessments without pretending they are precise numerical measurements.

The main limitations are daily rather than intraday data, one perpetual-futures market, one fixed chronological holdout, a lightweight Random Forest, and a deliberately small LSTM. The 14/30-day check tests sensitivity to target definition but not repeated market regimes. Consequently, the findings apply to this dataset and implementation rather than proving universal GARCH superiority.

## Conclusion

Machine learning does not provide the best accuracy, interpretability, practicality, or robustness trade-off in this project. GARCH has the lowest MAE and RMSE for both tested windows, a compact three-parameter structure, and an established volatility interpretation. Lagged linear regression and rolling historical volatility also outperform LSTM and Random Forest.

This does not show that machine learning can never improve Bitcoin volatility forecasting. Richer intraday or sentiment data, wider tuning, other assets, and walk-forward refitting could change the result. The evidence supports a narrower conclusion: under the tested Hyperliquid daily-data design, Random Forest and LSTM do not justify their extra complexity, while GARCH is the most defensible overall model.

The corrected date-alignment issue reinforces the project's critical value. A reproducible comparison is not only a table of errors; it requires checking that each forecast is matched to the correct observation and revising the conclusion when the evidence changes.
