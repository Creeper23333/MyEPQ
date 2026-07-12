# Q&A Notes

## Why did rolling historical volatility perform so well?

Because the target is next-day 30-day realised volatility, which is itself a rolling and persistent measure. Today's realised volatility already contains a lot of information about tomorrow's realised volatility.

## Why did lagged linear regression beat the machine-learning models?

It uses direct lagged volatility and return features, so it captures persistence very efficiently without the extra complexity of nonlinear or recurrent models.

## Why did GARCH perform best after the method audit?

GARCH directly models volatility clustering through recent shocks and persistent conditional variance. The corrected pipeline also aligns every GARCH forecast to the test set by date. It ranks first for both 14-day and 30-day targets, so the result is not dependent on only one volatility window.

## Why did the GARCH result change?

The earlier implementation selected GARCH predictions by reset dataframe row number after feature engineering removed incomplete rows. That could match a forecast to the wrong date. The corrected code maps forecasts by date and rejects incomplete alignment. The correction changed the GARCH ranking, and the report records this openly.

## Why did LSTM do better than Random Forest but still not win?

The LSTM can learn sequential patterns, so it improves on the Random Forest. However, the strongest predictive signal in this dataset still appears to be simple persistence, which lagged linear regression and rolling volatility already capture very well.

## Why not use more cryptocurrencies?

The project prioritised depth over breadth. Focusing on one core asset keeps the methodology clearer and the EPQ more manageable.

## Why use Hyperliquid rather than Yahoo Finance?

Hyperliquid gives exchange-level BTC perpetual futures candle data, which is closer to the actual market being studied than an aggregated finance website.

## Is this financial advice?

No. The project is an academic comparison of forecasting models and does not provide trading advice.

## What would you improve next?

- extend the existing 14/30-day robustness check to 60 days and repeated walk-forward periods
- tune the LSTM more extensively
- add richer inputs such as sentiment or intraday-based realised variance
- compare another cryptocurrency only after the core BTC pipeline is stable
