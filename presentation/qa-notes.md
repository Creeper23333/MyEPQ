# Q&A Notes

## Why did rolling historical volatility perform so well?

Because the target is tomorrow's updated 30-day rolling standard-deviation proxy. It shares 29 returns with today's window, so only the entering return is unknown at the forecast origin. Persistence is partly built into the target construction.

## Why did lagged linear regression beat the machine-learning models?

It uses direct lagged volatility and return features, so it captures persistence very efficiently without the extra complexity of nonlinear or recurrent models.

## Why did GARCH perform best after the method audit?

GARCH directly models volatility clustering through recent shocks and persistent conditional variance. The corrected pipeline aligns every forecast by date and scores each return before its shock updates the next conditional variance. It ranks first for both 14-day and 30-day targets, both test-period halves, all four expanding-window blocks and all three target-volatility regimes.

## Why did the GARCH result change?

The earlier implementation selected GARCH predictions by reset dataframe row number after feature engineering removed incomplete rows. That could match a forecast to the wrong date. The corrected code maps forecasts by date and rejects incomplete alignment. Later audits corrected the likelihood update order, estimated the standard-deviation target as `E[s]`, removed a duplicate predictor, froze the test cutoff and excluded an unfinished daily candle. The report records each change openly.

## Why did LSTM do better than Random Forest but still not win?

The LSTM can represent sequential patterns and its recorded RMSE is lower than the Random Forest's. The experiment does not prove that sequence learning caused the difference. The feature evidence suggests that simple volatility persistence remains the strongest signal, which rolling, GARCH and linear regression capture more efficiently.

## Was hyperparameter tuning fair?

Random Forest compared six predeclared candidates and LSTM compared four. Both used only the chronological tail of the training period for selection; neither inspected the final holdout. The searches are compact rather than exhaustive, so they improve fairness and reproducibility without proving each architecture reached its best possible configuration.

## How comparable were the model pipelines?

The recorded comparison keeps the same information cutoff and test dates, but the models do not use identical inputs. The tabular models use prepared features, LSTM uses sequences, and GARCH first predicts conditional variance. It compares the tested pipelines; it cannot attribute the result only to model type.

## Why add QLIKE?

True volatility cannot be observed directly, and the rolling target is only an estimate. QLIKE provides another error measure. It gives the same ranking as RMSE but does not remove the limits of the overlapping target.

## What does the bootstrap add?

The daily errors are related because the target windows overlap. The saved bootstrap therefore resamples 30-day blocks rather than single dates. GARCH's advantage over rolling stayed clear, while linear regression's small advantage did not. The evidence still comes from one market history.

## Was walk-forward validation included?

It is included as a separate check. The main test starts on 16 November 2025 and stays fixed when new data are added. The saved analysis also uses four expanding time blocks and refits the models for each block. This is block-by-block testing, not daily retraining.

## What did the Random Forest OOB result show?

Every training row received predictions only from trees that did not train on it. OOB RMSE is `0.00128268`, while chronological-test RMSE is `0.00211129`. OOB does not replace time testing, but the gap suggests weaker cross-period generalisation.

## Was the LSTM result caused by one random seed?

Seeds 7, 42 and 101 give RMSE values from `0.00168735` to `0.00178061`; all remain worse than rolling. This makes the current conclusion less dependent on one initialisation, although it does not cover every architecture or tuning choice.

## Can you explain the LSTM's predictions?

Not fully. The saved sensitivity check replaces one input at a time with its training average. Replacing the current 30-day volatility estimate changed the error most. The change identifies an influential input in the fitted model; it does not explain cause and effect or every individual forecast.

## Why was the last API candle excluded?

Daily APIs can return the current candle before it closes. The 20 August pull returned 1,272 rows, but the 20 August row's end timestamp was later than the fetch time. Excluding it leaves 1,271 completed candles through 19 August and prevents a partial-day return from entering the target.

## Why is the test boundary frozen?

A moving 80/20 split would move some old test dates into training whenever new candles arrived, so refreshes would not be directly comparable. Freezing the 2025-11-16 forecast origin means the 950-row training set stays unchanged and the 31 new completed candles add genuine later test evidence.

## What did the 19 August price jump show?

The close rose from `64,696` to `69,323`, the daily log return was about `0.06908`, and the 30-day target rose to `0.01746941`. Random Forest's forecast of `0.01303376` was closest on that single target, while GARCH forecast `0.01253680`; all five forecasts were low. Random Forest still ranks fifth overall, so this one observed holdout result is a diagnostic rather than evidence of general improvement. It also cannot be used to retune the models without sacrificing the holdout's role.

## Why use Gauss-Hermite quadrature for GARCH?

GARCH first forecasts variance, but the target is a rolling standard deviation. Numerical integration converts one into the other more directly. The saved sensitivity check also uses the simpler square-root conversion; the difference is tiny and the ranking does not change.

## Why not use more cryptocurrencies?

The project prioritised depth over breadth. Focusing on one core asset keeps the methodology clearer and the EPQ more manageable.

## Why use Hyperliquid rather than Yahoo Finance?

Hyperliquid gives exchange-level BTC perpetual futures candle data, which is closer to the actual market being studied than an aggregated finance website.

## Is this financial advice?

No. The project is an academic comparison of forecasting models and does not provide trading advice.

## Is GARCH more practical just because it ran faster?

No. Running time is only one part of practicality. The comparison also records how many settings each model needed, which libraries it depended on and how stable it was. The timings describe only this computer and this implementation.

## What would you improve next?

- reserve a genuinely untouched future test period and use finer rolling-origin blocks
- tune the LSTM within a separate chronological validation design
- add richer inputs such as sentiment or intraday-based realised variance
- compare another cryptocurrency only after the core BTC pipeline is stable
