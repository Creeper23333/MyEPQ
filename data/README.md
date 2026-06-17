# Data

This folder stores Hyperliquid cryptocurrency price data and processed volatility datasets.

## Suggested Structure

```text
data/
  raw/          Original downloaded data
  processed/    Cleaned data used for modelling
```

## Likely Data Fields

- Date
- Open
- High
- Low
- Close
- Volume
- Log return
- Realised volatility

## Data Rules

- Keep a note of the source and download date.
- Do not manually edit raw data.
- Record any cleaning decisions in the report methodology or appendix.

## Current Data Source

- Exchange: Hyperliquid
- API: `POST https://api.hyperliquid.xyz/info`
- Public market request type: `candleSnapshot`
- Core market: BTC perpetual futures
- Interval: `1d`
- Current sample period: 2023-02-26 to 2026-06-17
- Optional account/reference address: `0x28e81E9fAC95AC1fae40870E4C08E6b94FcB1C23`

## Current Generated Files

- `raw/hyperliquid_BTC_1d_candles.csv`: raw OHLCV candles returned by Hyperliquid
- `raw/hyperliquid_BTC_1d_metadata.json`: API request metadata and source notes
- `processed/hyperliquid_BTC_1d_volatility.csv`: close prices, log returns, and 30-day realised volatility
