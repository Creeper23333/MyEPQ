# Results Draft

## Primary 30-Day Target

| Rank | Model | Category | MAE | MSE | RMSE |
| --- | --- | --- | --- | --- | --- |
| 1 | GARCH(1,1) | Traditional statistical | 0.00047808 | 0.00000099 | 0.00099637 |
| 2 | Lagged linear regression | Interpretable lag-feature model | 0.00074798 | 0.00000201 | 0.00141843 |
| 3 | Rolling historical volatility | Benchmark | 0.00063564 | 0.00000209 | 0.00144481 |
| 4 | LSTM | Machine learning | 0.00106690 | 0.00000339 | 0.00184029 |
| 5 | Random Forest | Machine learning | 0.00122445 | 0.00000452 | 0.00212715 |

The corrected primary result does not support the claim that machine learning improves forecasting accuracy in this implementation. GARCH(1,1) has the lowest MAE and RMSE. Its RMSE is approximately 31.0% below the rolling benchmark. Lagged linear regression improves RMSE over the rolling benchmark by approximately 1.8%, although its MAE is higher. LSTM and Random Forest have RMSE values approximately 27.4% and 47.2% above the rolling benchmark respectively.

## Method Audit and Correction

An audit found that the earlier GARCH output was selected by reset dataframe row number after feature engineering had removed incomplete early rows. This could pair a GARCH forecast with the wrong test date. The pipeline now stores the forecast series against its source dates and explicitly maps it to the test dates. It also rejects duplicate source dates or missing forecasts. The corrected result is therefore the valid result used in this report; the earlier GARCH ranking has been retired rather than averaged or selectively retained.

This correction did not change the linear regression, rolling benchmark, Random Forest, or LSTM predictions. It changed the interpretation substantially: the strongest model is now a traditional statistical model, while the wider conclusion that machine learning has not won remains unchanged.

## Robustness Across Volatility Windows

| Window | GARCH RMSE | Linear RMSE | Rolling RMSE | LSTM RMSE | RF RMSE | Winner |
| --- | --- | --- | --- | --- | --- | --- |
| 14 days | 0.00179214 | 0.00262221 | 0.00278701 | 0.00360202 | 0.00391877 | GARCH(1,1) |
| 30 days | 0.00099637 | 0.00141843 | 0.00144481 | 0.00184029 | 0.00212715 | GARCH(1,1) |

The complete model set was rerun with next-day 14-day realised volatility as an alternative target. The shorter window is more variable and therefore produces larger errors for every model. However, the model ordering is unchanged: GARCH ranks first, followed by linear regression, rolling historical volatility, LSTM, and Random Forest. GARCH improves on the rolling benchmark by approximately 35.7% for the 14-day target and 31.0% for the 30-day target. This ranking stability strengthens the result, although two windows from one market are not enough to establish universal superiority.

## Computational Practicality

The pipeline records fit time, prediction time, and a model-specific structural measure during the primary run. In the current local CPU run, rolling historical volatility required no fitting; linear regression fitted in less than one millisecond; GARCH took about 0.6 seconds; LSTM took about 4.1 seconds; and the in-repo Random Forest took about 5.2 seconds. Prediction time was small for every model relative to fitting time.

The structural evidence also shows the difference in complexity. GARCH has three fitted parameters, linear regression has 27 coefficients including its intercept, LSTM has 6,049 trainable parameters, and the fitted Random Forest contains 18,036 tree nodes across 160 trees. These measures are not directly equivalent, but they make the scale of each implementation visible. Timing values are from one machine and one run, so they are evidence about this project's implementations rather than universal speed benchmarks.

## Interpretability

Rolling historical volatility is the easiest model to explain because it directly carries today's realised volatility forward. GARCH is also relatively interpretable: `omega`, `alpha`, and `beta` represent baseline variance, response to shocks, and volatility persistence. Linear regression exports a signed coefficient for each standardised input, although correlated lag features limit causal interpretation. Random Forest exports global feature importance, but this does not show the direction of an effect or explain an individual forecast. LSTM records its architecture, inputs, parameter count, and training history, but its recurrent hidden states do not provide a direct explanation of each prediction.

## Result Against the Research Question

GARCH provides the best balance in the current evidence: it has the strongest accuracy at both target windows, high interpretability, a small parameter set, deterministic fitting, and moderate local runtime. Machine learning remains useful as a comparison because it tests nonlinear and sequential alternatives, but neither LSTM nor Random Forest provides an accuracy gain that compensates for lower transparency and greater structural complexity.
