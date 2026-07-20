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
- Current request window: 2023-02-26 to 2026-07-20
- Latest completed daily candle retained: 2026-07-19
- Completion check: 1,241 rows were returned and one still-open daily candle was excluded by end timestamp
- Quality check: all 1,240 retained rows passed required-field, timestamp-order, daily-cadence, symbol/interval, positive-price, OHLC and non-negative-activity checks

## Current Generated Files

- `raw/hyperliquid_BTC_1d_candles.csv`: completed-candle OHLCV archive after the rule-based end-timestamp filter; metadata retains the original API row count and excluded-row count
- `raw/hyperliquid_BTC_1d_metadata.json`: API request metadata and source notes
- `raw/hyperliquid_BTC_1d_quality_report.json`: machine-readable validation counts and cadence evidence
- `processed/hyperliquid_BTC_1d_volatility.csv`: close prices, log returns, and 30-day realised volatility

Latest refresh completed on 2026-07-20 local time (`2026-07-20T06:12:26Z`).
