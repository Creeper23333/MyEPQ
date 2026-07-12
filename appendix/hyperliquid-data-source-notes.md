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
    "endTime": 1783987199999
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

## Address Use

The address supplied for the project is:

```text
0x28e81E9fAC95AC1fae40870E4C08E6b94FcB1C23
```

This address is not required for public market candles. It is kept as optional metadata because Hyperliquid user/account endpoints require a 42-character hexadecimal user address. The volatility model should use public BTC candle data, not private trading decisions from one account.

## Methodological Consequence

Using Hyperliquid improves the project because the price data comes from the exchange being studied rather than from an aggregated finance website. The limitation is that Hyperliquid BTC perpetual futures prices are not exactly the same as spot BTC-USD prices, so the report should describe the asset as Bitcoin perpetual futures or Hyperliquid BTC rather than generic Bitcoin spot price.

The current dataset starts on 2023-02-26 because the API pull returned zero volume and zero trade count before that date. This makes the sample more clearly exchange-based rather than relying on earlier price-only candles.

In the refresh run completed on 2026-07-13, the request window ended on 2026-07-13, and the latest daily candle returned by the API was dated 2026-07-12. This is normal for daily data because the current day's candle may not yet be complete at the time of the pull.

Current generated files:

- `data/raw/hyperliquid_BTC_1d_candles.csv`
- `data/raw/hyperliquid_BTC_1d_metadata.json`
- `data/processed/hyperliquid_BTC_1d_volatility.csv`
