# EPQ Project Revision Checklist (Working Notes)

**Revision points dated:** July 25, 2026

**Current bilingual clean copy prepared:** August 9, 2026

**Status:** These notes preserve the candidate's July 25 revision points. OpenAI Codex assisted with organising, editing and translating the current bilingual clean copy on August 9. This file is not authenticated supervisor feedback or tutor comments.

## 1. Title, Research Question, Aim, and Objectives

The phrase “Bitcoin volatility” is too broad for the work actually completed. The project uses daily Hyperliquid BTC perpetual-futures data and forecasts an updated rolling volatility proxy. The title and Research Question should reflect that narrower scope.

Recommended Research Question:

> **To what extent do Random Forest and LSTM justify their additional complexity over rolling historical volatility and GARCH(1,1) when forecasting the next-day update of a volatility proxy constructed from Hyperliquid BTC perpetual-futures returns?**

Recommended Aim:

> **To determine whether the additional complexity of Random Forest and LSTM is justified when forecasting the next-day update of a daily volatility proxy constructed from Hyperliquid BTC perpetual-futures returns.**

The Objectives need to be more explicit so that the Examiner can see how the project answers the Research Question:

1. Construct a reproducible daily volatility proxy from completed Hyperliquid BTC perpetual-futures candles, using a 30-day rolling sample standard deviation as the primary target and a 14-day window as a robustness check.
2. Implement rolling historical volatility, GARCH(1,1), lagged linear regression, Random Forest, and LSTM, and document the inputs, training sample, prediction target, and output transformation used by each model.
3. Compare forecast accuracy using RMSE, MAE, and supplementary QLIKE.
4. Test robustness across target windows, time periods, expanding-window folds, volatility regimes, data refreshes, relevant random seeds, and a block bootstrap.
5. Compare interpretability and practical complexity using parameters, coefficients, feature importance, architecture, tuning burden, dependencies, structural size, and local fit/predict time.
6. Determine whether any improvement from Random Forest or LSTM is sufficiently clear, stable, and practically meaningful to justify its additional complexity.

The final judgment should use four core dimensions:

| Dimension | Main evidence |
| --- | --- |
| Accuracy | RMSE, MAE, and QLIKE |
| Robustness | Windows, periods, folds, regimes, refresh, seeds, and bootstrap |
| Interpretability | Equations, parameters, coefficients, feature importance, architecture, and explanations actually produced |
| Practicality | Tuning and implementation burden, dependencies, structural size, training stability, and local fit/predict time |

Reproducibility should support all four dimensions through fixed dates, seeds, configurations, metadata, tests, and the Production Log.

## 2. Forecast Target

The report must state precisely what is being predicted. The primary target is not an independently observed value of “true Bitcoin volatility.” It is the next day's updated 30-day rolling standard deviation of daily returns, `RV(t+1, 30)`.

The current and next rolling windows share 29 returns. One known return leaves the window and the only new unknown return is `r(t+1)`. The task is therefore to predict how the entering return changes a highly overlapping and persistent rolling proxy, rather than to predict an entirely new volatility value formed only by the future market.

Suggested wording:

> At time t, the model forecasts the 30-day rolling standard deviation after the return for day t+1 becomes available. The updated window shares 29 returns with the current window, so the target is a next-day update of an overlapping volatility proxy rather than a direct observation of latent market volatility.

This definition should be consistent in the title, Research Question, Abstract, Methodology, Results, and Conclusion. Repeated explanations can be combined. Periods of larger disagreement in the forecast chart should also be interpreted in light of the target: the 29 shared observations provide less protection when the entering return is unusually large.

## 3. Methodology and Fairness of the Comparison

### 3.1 Role of each model

- Rolling historical volatility is the simplest persistence benchmark and directly exploits the overlap between adjacent targets.
- GARCH(1,1) is a conditional-variance benchmark whose forecast must be transformed into the rolling-standard-deviation proxy.
- Lagged linear regression is a low-complexity supervised comparator for approximately linear relationships in the engineered inputs and should be reported separately.
- Random Forest and LSTM are higher-complexity models capable of representing nonlinear relationships.

Performance cannot be attributed automatically to “nonlinear architecture.” The Random Forest and LSTM pipelines also differ in features, sequences, effective sample size, hyperparameters, optimization, and implementation. Without a matched experiment or ablation, the report can only conclude whether the implemented pipeline added value.

### 3.2 GARCH and the supervised models do not use identical pipelines

GARCH first forecasts next-period conditional variance and then converts it into a forecast of the rolling proxy. In the current report, Linear Regression, Random Forest, and LSTM use engineered features to predict the next-day rolling target directly. The oral discussion also used `r(t+1)^2` as shorthand for the unknown contribution of the entering return. The final Methodology must be checked against the code and state clearly whether each supervised model predicts `RV(t+1)`, `r(t+1)^2`, or another intermediate quantity.

The Conclusion should not state:

> GARCH is better than LSTM.

It should state:

> The current GARCH-based forecasting pipeline outperformed the current direct-target LSTM pipeline under this experimental design.

If time permits, a matched-pipeline comparison would be a useful extension. For example, every model could predict the same intermediate quantity, such as the conditional second moment of the entering return, before the same rolling-window transformation is applied. This would be a bonus rather than an EPQ requirement.

### 3.3 Feature sets differ across models

Different inputs weaken a strict controlled-experiment interpretation, but the existing experiments and Results do not need to be discarded solely for this reason. The report should:

- list the features and sequence length used by each model;
- explain why the input representations differ;
- report effective training-sample sizes;
- state that the study compares complete, project-specific pipelines;
- avoid attributing every performance difference to the model class alone.

Do not write:

> LSTM is not effective for Bitcoin volatility forecasting.

Write:

> LSTM did not provide a stable benefit under the available daily sample, selected inputs, and current training procedure.

### 3.4 Random Forest implementation

The current Random Forest is a simplified project-local regressor, not a fully representative and widely validated library implementation. It is acceptable for an EPQ if described accurately, but its poor performance should not be used as decisive evidence against Random Forest as a model family.

A more professional approach would use a standard library Random Forest and record the library version, seed, number of trees, maximum depth, minimum leaf size, feature-subsampling rule, and tuning method. If time does not allow a rerun, retain the current version but call it a “lightweight project-local Random Forest implementation” and limit the conclusion accordingly.

### 3.5 Hyperparameter tuning

The reasons for the Random Forest and LSTM hyperparameters, and the fairness of the tuning process, need to be checked. Record:

- which settings were fixed in advance and why;
- which values or ranges were considered;
- whether chronological validation, rather than the final test set, was used;
- which metric selected the settings;
- how seeds and LSTM early stopping were handled;
- whether the models were deliberately kept small because of EPQ time and scale.

If tuning was limited or unequal, state this as a limitation. Do not imply that the result is the best achievable performance of the model family.

## 4. Evaluation Metrics and Results

RMSE and MAE should remain because they are intuitive. However, volatility is latent and the current target is an imperfect proxy, so QLIKE should be added as a supplementary metric.

Patton (2011) explains that the loss function can affect forecast rankings when imperfect volatility proxies are used, and identifies QLIKE as robust under the paper's assumptions. Calculate QLIKE on the variance scale:

> `v_t = max(y_t^2, epsilon)`
> `v_hat_t = max(y_hat_t^2, epsilon)`
> `QLIKE_t = v_t / v_hat_t - ln(v_t / v_hat_t) - 1`

Lower QLIKE is better. The report should state the value of `epsilon`, explain how nonpositive forecasts are handled, and make clear that the standard-deviation forecasts are squared before evaluation.

QLIKE should not be presented as eliminating every problem with the proxy. Patton's result depends on assumptions that do not map perfectly onto a 30-day overlapping rolling variance. The careful claim is that QLIKE provides a relevant supplementary robustness check for an imperfect volatility proxy.

Recommended source:

Patton, A. J. (2011), “Volatility forecast comparison using imperfect volatility proxies,” *Journal of Econometrics*, 160(1), 246-256. [DOI](https://doi.org/10.1016/j.jeconom.2010.03.034); [author-hosted full text](https://public.econ.duke.edu/~ap172/Patton_vol_proxies_JoE_2011.pdf).

The existing Results answer Accuracy and Robustness well. After QLIKE is added, show its ranking beside RMSE and MAE and discuss any disagreement. Change the main conclusion only if the new evidence supports doing so, and update the relevant tables, discussion, conclusion, and appendices consistently.

## 5. Interpretability and Practicality

The interpretability evidence is adequate for an EPQ but weaker than the Accuracy and Robustness evidence. Recommended additions:

- Linear regression: include a compact table of standardized coefficients showing direction and magnitude.
- GARCH(1,1): interpret omega, alpha, beta, persistence, and the conversion from conditional variance to the rolling proxy.
- Random Forest: show impurity importance and, if already available, permutation importance. Explain that global importance is associational, can be divided among correlated features, and does not explain one forecast.
- LSTM: architecture, loss curves, and seed stability mainly describe structure and training stability. They do not explain individual predictions. If time permits, add a small sensitivity or ablation analysis for selected holdout cases and label it as exploratory.

Practicality should not be answered by runtime alone. Local fit/predict time can remain, but the discussion should also cover:

- the number of tuning and implementation decisions;
- library and environment dependencies;
- training stability and seed sensitivity;
- parameter count, node count, or structural size;
- difficulty of reproducing, maintaining, and explaining the pipeline.

It is reasonable to state that GARCH required fewer tuning and implementation choices in this project. One local timing table does not prove that GARCH is universally faster to deploy.

## 6. Conclusion, Academic Writing, and Source Evaluation

The Conclusion must be limited to the current data, target, features, implementations, and tuning budget. Suggested wording:

> In the tested daily sample, the current GARCH-based pipeline gave the best balance of error, stability and implementation burden. Neither tested Random Forest nor LSTM beat the rolling benchmark overall. This statement is limited to the current target, inputs, implementations and tuning budget; different data or designs may give another ranking.

The next draft needs an academic-writing edit focused on precision:

- use “forecast,” “proxy,” “pipeline,” “conditional variance,” and “rolling standard deviation” consistently;
- separate evidence, interpretation, and speculation;
- state assumptions before explaining results;
- avoid causal claims when the evidence is associational;
- use “the tested model” or “the current pipeline” instead of broad claims about a whole model family.

The project already demonstrates sufficient critical thinking and evaluation. Source Evaluation could be strengthened by comparing studies by data frequency, volatility target, market, forecast horizon, model implementation, validation method, peer-review status, relevance, and limitations. This can be placed in the Appendix and Source Evaluation.

## 7. Production Log and Next Revision

Every later change should be recorded in the Production Log, including:

- date;
- the issue or decision that led to the change;
- text, code, experiment, table, or figure changed;
- reason for the change;
- results or conclusions affected;
- reflection and remaining limitation;
- location of the relevant file or evidence.

The change record should state what was changed, why it was changed, which result or conclusion was affected, and where the evidence is stored. If genuine supervisor feedback is received later, add it separately with the real date and either the original wording or an approved paraphrase. The official Production Log should be completed from the candidate's own record and the centre-issued form.
