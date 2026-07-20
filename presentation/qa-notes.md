# Q&A Notes

## Why did rolling historical volatility perform so well?

Because the target is next-day 30-day realised volatility, which is itself a rolling and persistent measure. Today's realised volatility already contains a lot of information about tomorrow's realised volatility.

## Why did lagged linear regression beat the machine-learning models?

It uses direct lagged volatility and return features, so it captures persistence very efficiently without the extra complexity of nonlinear or recurrent models.

## Why did GARCH perform best after the method audit?

GARCH directly models volatility clustering through recent shocks and persistent conditional variance. The corrected pipeline aligns every forecast by date and scores each return before its shock updates the next conditional variance. It ranks first for both 14-day and 30-day targets, both test-period halves, all four expanding-window blocks and all three target-volatility regimes.

## Why did the GARCH result change?

The earlier implementation selected GARCH predictions by reset dataframe row number after feature engineering removed incomplete rows. That could match a forecast to the wrong date. The corrected code maps forecasts by date and rejects incomplete alignment. Later audits corrected the likelihood update order, estimated the standard-deviation target as `E[s]`, removed a duplicate predictor, froze the test cutoff and excluded an unfinished daily candle. The report records each change openly.

## Why did LSTM do better than Random Forest but still not win?

The LSTM can represent sequential patterns and its recorded RMSE is lower than the Random Forest's. The experiment does not prove that sequence learning caused the difference. The feature evidence suggests that simple volatility persistence remains the strongest signal, which rolling, GARCH and linear regression capture more efficiently.

## What does the bootstrap add?

The target uses overlapping rolling windows, so daily errors are related. I resampled paired 30-day blocks rather than isolated dates. GARCH's RMSE difference from rolling stays below zero across the 95% interval, while linear regression's small advantage crosses zero. This is stronger descriptive evidence, but not proof for every future market.

## Did you perform walk-forward validation?

The primary result uses a forecast-origin test cutoff frozen at 2025-11-16. It was initially near an 80/20 split, but later refreshes only extend its test set. Separately, I performed four expanding-window rolling-origin folds. The first fold shares the primary training boundary; every later fold adds the preceding block and refits all models. This is block-level refitting, not daily online retraining.

## What did the Random Forest OOB result show?

Every training row received predictions only from trees that did not train on it. OOB RMSE is `0.00131585`, while the later chronological-test RMSE is `0.00232370`. OOB does not replace time testing, but the gap suggests weaker cross-period generalisation.

## Was the LSTM result caused by one random seed?

Seeds 7, 42 and 101 give RMSE values from `0.00174351` to `0.00184673`; all remain worse than rolling. This makes the current conclusion less dependent on one initialisation, although it does not cover every architecture or tuning choice.

## Why was the last API candle excluded?

Daily APIs can return the current candle before it closes. The final pull returned 1,241 rows, but the last row's end timestamp was later than the fetch time. Excluding it keeps every retained daily close comparable and prevents a partial-day return from entering the target.

## Why did you freeze the test boundary?

A moving 80/20 split would move some old test dates into training whenever new candles arrived, so refreshes would not be directly comparable. Freezing the 2025-11-16 forecast origin means the 950-row training set stays unchanged and the seven new completed candles add genuine later test evidence.

## Why use Gauss-Hermite quadrature for GARCH?

The target is a rolling standard deviation. Under squared-error scoring, its conditional point forecast is `E[s]`, whereas `sqrt(E[s²])` is slightly different because of Jensen's inequality. Eighty-point Gauss-Hermite quadrature evaluates `E[s]` deterministically under the same Gaussian assumption as the GARCH likelihood. The exported sensitivity has nearly identical RMSE and the model rank is unchanged.

## Why not use more cryptocurrencies?

The project prioritised depth over breadth. Focusing on one core asset keeps the methodology clearer and the EPQ more manageable.

## Why use Hyperliquid rather than Yahoo Finance?

Hyperliquid gives exchange-level BTC perpetual futures candle data, which is closer to the actual market being studied than an aggregated finance website.

## Is this financial advice?

No. The project is an academic comparison of forecasting models and does not provide trading advice.

## What would you improve next?

- reserve a genuinely untouched future test period and use finer rolling-origin blocks
- tune the LSTM within a separate chronological validation design
- add richer inputs such as sentiment or intraday-based realised variance
- compare another cryptocurrency only after the core BTC pipeline is stable
