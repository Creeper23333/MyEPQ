# Q&A Notes

## Why did rolling historical volatility perform so well?

Because the target is next-day 30-day realised volatility, which is itself a rolling and persistent measure. Today's realised volatility already contains a lot of information about tomorrow's realised volatility.

## Why did lagged linear regression beat the more complex models?

It uses direct lagged volatility and return features, so it captures persistence very efficiently without the extra complexity of nonlinear or recurrent models.

## Why did GARCH perform worst?

GARCH forecasts conditional daily variance, while the project evaluates next-day 30-day realised volatility. That mismatch makes comparison harder, even though GARCH is still a meaningful theoretical benchmark.

## Why did LSTM do better than Random Forest but still not win?

The LSTM can learn sequential patterns, so it improves on the Random Forest. However, the strongest predictive signal in this dataset still appears to be simple persistence, which lagged linear regression and rolling volatility already capture very well.

## Why not use more cryptocurrencies?

The project prioritised depth over breadth. Focusing on one core asset keeps the methodology clearer and the EPQ more manageable.

## Why use Hyperliquid rather than Yahoo Finance?

Hyperliquid gives exchange-level BTC perpetual futures candle data, which is closer to the actual market being studied than an aggregated finance website.

## Is this financial advice?

No. The project is an academic comparison of forecasting models and does not provide trading advice.

## What would you improve next?

- test a different volatility window such as 14 or 60 days
- tune the LSTM more extensively
- add richer inputs such as sentiment or intraday-based realised variance
- compare another cryptocurrency only after the core BTC pipeline is stable
