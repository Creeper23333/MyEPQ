# Hyperliquid Data Source Notes

## API Choice

The project now uses Hyperliquid exchange data rather than Yahoo Finance. The core public endpoint is:

```text
POST https://api.hyperliquid.xyz/info
```

For market candles, the request type is:

```json
{
  "type": "candleSnapshot",
  "req": {
    "coin": "BTC",
    "interval": "1d",
    "startTime": 1677369600000,
    "endTime": 1784591999999
  }
}
```

The returned candle fields include:

| Field | Meaning |
| --- | --- |
| `t` | Candle start time in milliseconds |
| `T` | Candle end time in milliseconds |
| `s` | Symbol, e.g. BTC |
| `i` | Interval, e.g. 1d |
| `o` | Open price |
| `h` | High price |
| `l` | Low price |
| `c` | Close price |
| `v` | Volume |
| `n` | Number of trades |

## Account Independence

No user or wallet address is required for the public `candleSnapshot` request. The final pipeline therefore leaves account metadata unset and models exchange-wide BTC perpetual-futures candles, not one person's trading history.

## Methodological Consequence

Using Hyperliquid improves the project because the price data comes from the exchange being studied rather than from an aggregated finance website. The limitation is that Hyperliquid BTC perpetual futures prices are not exactly the same as spot BTC-USD prices, so the report should describe the asset as Bitcoin perpetual futures or Hyperliquid BTC rather than generic Bitcoin spot price.

The current dataset starts on 2023-02-26 because the API pull returned zero volume and zero trade count before that date. This makes the sample more clearly exchange-based rather than relying on earlier price-only candles.

In the refresh run completed on 2026-07-20 Beijing time, the API returned 1,241 rows. The pipeline compared each candle's end timestamp with the fetch timestamp and excluded one still-open row, leaving 1,240 completed daily candles from 2023-02-26 through 2026-07-19. This explicit completion check prevents a partial daily close, volume or trade count from entering the model.

Before any file is accepted, the pipeline validates required fields, strictly increasing and unique start timestamps, expected interval cadence, a single symbol and interval, positive prices, valid OHLC ordering, non-negative volume and non-negative trade count. The model-only entry point also recomputes returns and volatility and rejects gaps or corrupted values. The current quality report passes all 1,240 rows with zero critical issues; both the minimum and maximum daily start-time gaps are 86,400,000 milliseconds.

Current generated files:

- `data/raw/hyperliquid_BTC_1d_candles.csv`
- `data/raw/hyperliquid_BTC_1d_metadata.json`
- `data/raw/hyperliquid_BTC_1d_quality_report.json`
- `data/processed/hyperliquid_BTC_1d_volatility.csv`
