# yfinance Field Audit Summary

Generated: 2026-03-20T19:49:26.403691+00:00

Tickers audited: AAPL, MSFT, TSLA, SPY, BABA, PLTR

Provider/runtime errors observed: 0

## Most Reliable Fields (Top 25 by non_null_rate)
- info.volume | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.typeDisp | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.twoHundredDayAverageChangePercent | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.twoHundredDayAverageChange | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.twoHundredDayAverage | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.triggerable | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.trailingPE | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.trailingAnnualDividendYield | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.trailingAnnualDividendRate | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.tradeable | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.symbol | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.sourceInterval | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.shortName | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.sharesOutstanding | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.regularMarketVolume | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.regularMarketTime | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.regularMarketPrice | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.regularMarketPreviousClose | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.regularMarketOpen | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.regularMarketDayRange | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.regularMarketDayLow | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.regularMarketDayHigh | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.regularMarketChangePercent | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.regularMarketChange | non_null_rate=1.00 | seen_rate=1.00 | Tier 1
- info.region | non_null_rate=1.00 | seen_rate=1.00 | Tier 1

## Notes
- Tier 1 fields are safest for UI defaults.
- Tier 2 fields are useful but need null-safe rendering.
- Tier 3 fields are best kept out of primary UI paths.
