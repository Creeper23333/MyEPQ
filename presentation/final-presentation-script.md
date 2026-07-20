# Final 10-Minute Presentation Script

Use this as a speaking guide, not a paragraph-by-paragraph reading script. The timings total approximately ten minutes.

## Slide 1 — Research question (45 seconds)

My project asks how Random Forest and LSTM compare with rolling historical volatility and GARCH(1,1) when forecasting Bitcoin volatility. I evaluate four things: accuracy, interpretability, computational practicality and robustness. I chose this wording because I did not want to assume that machine learning would win. The real question is whether additional complexity produces a clear and stable benefit.

## Slide 2 — Why volatility? (45 seconds)

Volatility forecasting is different from predicting whether Bitcoin will rise or fall. It estimates the scale of uncertainty in future returns. That can inform position sizing, risk limits or awareness of stressful market conditions. My project is an academic model comparison, not trading advice, and it does not test profitability.

## Slide 3 — Data and target (60 seconds)

I used daily candles from Hyperliquid's BTC perpetual-futures market. The final API request returned 1,241 rows. One candle had not yet reached its end timestamp, so the pipeline excluded it and retained 1,240 completed days through 19 July 2026. I calculated log returns and used the rolling sample standard deviation as a realised-volatility proxy. The main target is tomorrow's updated 30-day value. It is a proxy because true conditional volatility cannot be directly observed.

## Slide 4 — Comparison design (55 seconds)

After lag and rolling features were created, 1,195 modelling rows remained. I froze the forecast-origin test start at 16 November 2025, leaving 950 training rows and 245 test rows. Later refreshes extend only the test set, so old test observations never become training data. I preserved chronology and did not shuffle. Scaling statistics came only from training data. The LSTM also used the final part of its training sequences for validation and early stopping. As a separate check, I divided the later period into four ordered blocks and refitted on an expanding history at each later boundary.

## Slide 5 — Models (50 seconds)

Rolling volatility is the persistence benchmark: tomorrow equals today. GARCH models conditional variance through a baseline, recent shocks and persistent past variance. Linear regression is an auxiliary check of whether lagged features need a nonlinear model. Random Forest captures nonlinear thresholds using many trees. LSTM processes 30-day sequences through a recurrent network. These models also form a spectrum from a one-rule explanation to thousands of distributed parameters.

## Slide 6 — Main result (70 seconds)

Lower RMSE is better. GARCH ranks first with RMSE 0.00098502. Linear regression and rolling volatility are close, then LSTM, then Random Forest. GARCH improves RMSE by 31.0% compared with rolling. Linear improves RMSE by only 1.9%, and its MAE is actually worse than rolling, so I do not call that small difference decisive. Neither machine-learning model improves on the benchmark overall.

The Random Forest's permutation importance helps explain why. After I removed a mathematically duplicate 30-day standard-deviation input, current 30-day volatility, its first lag and 30-day mean absolute return remained the leading signals. The forest uses a large tree structure mainly to recover persistence that simpler models expose directly.

## Slide 7 — Robustness (65 seconds)

I tested whether one table was giving a fragile answer. The full ranking is unchanged for 14-day and 30-day targets. GARCH ranks first in both test halves, every expanding-window block, and all three volatility regimes. Lower ranks do vary: LSTM beats rolling in two individual folds, but not overall. High volatility is hardest and GARCH slightly underpredicts that group. I also resampled paired 30-day blocks 2,000 times. GARCH's RMSE difference from rolling has a 95% interval from -0.00099670 to -0.00017158, while linear regression's interval crosses zero. Finally, I reran the same upgraded method on data ending one week earlier: all five ranks stayed fixed and RMSE changed by only 0.8 to 1.4 percent.

## Slide 8 — Method audit (60 seconds)

The audit became one of the most valuable parts of the project. An early GARCH result used reset row numbers after feature engineering removed rows, so I replaced that with strict date mapping. I corrected the likelihood so each return is scored before its shock updates the next variance. Because the target is a standard deviation, I now estimate its conditional expectation with 80-point Gauss-Hermite integration and export the previous square-root-of-expected-variance conversion as a sensitivity. I also removed a duplicate predictor, froze the test cutoff, and added incomplete-candle, model-input and data-quality gates. Thirty-nine tests protect these checks. I learned that reproducibility needs conceptual tests, not just code that executes.

## Slide 9 — Wider evaluation and limits (75 seconds)

GARCH reports three fitted parameters and took about 1.00 second in the recorded local run. LSTM has 5,921 trainable parameters and Random Forest contains 17,984 fitted nodes; both took about 5.4 seconds. Those times are implementation-specific, but neither machine-learning model gives an overall accuracy return for its extra structure.

There are important limits. The study uses one perpetual-futures market, daily rather than intraday data, one historical period and limited machine-learning tuning. Four refitted blocks improve the time check but are not independent external validation. I also do not test Value at Risk or portfolio performance. Published work using high-frequency data and more advanced networks sometimes finds that machine learning wins, so my result should not be generalised beyond this experiment.

## Slide 10 — Conclusion (75 seconds)

My answer is that Random Forest and LSTM do not justify their extra complexity under this design. GARCH is the most defensible overall model because it has the lowest errors, ranks first across every robustness check, has a compact explanation and has moderate computational cost. Rolling volatility remains the easiest fallback to communicate.

This does not mean machine learning can never improve Bitcoin volatility forecasting. A stronger extension would reserve a genuinely untouched future period, use intraday realised variance, run finer rolling-origin tests, try heavier-tailed or asymmetric GARCH models, and add richer inputs or a hybrid model. The main conclusion is that complexity should only be preferred when it earns its place through a clear, stable and context-relevant gain. I am now happy to take questions.

## Rehearsal checklist

- Aim for 9:30–10:00 before questions.
- Explain the volatility proxy without reading the formula.
- Say “perpetual futures”, not “Bitcoin spot”.
- Say “the frozen 2025-11-16 cutoff is primary; four-fold expanding-window is supplementary”.
- State that negative bootstrap differences favour the compared model.
- Do not claim financial advice, profitability or universal GARCH superiority.
