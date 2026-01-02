# Crypto-Volatility-Neural-Nets
Forecasting Short-Term Crypto Volatility Spikes Using Neural Networks

Guiding question: Can neural networks can help dentify market and macroeconomic conditions that precede short-term volatility spikes in cryptocurrency markets (e.g., Bitcoin)?



## Data Source

**Provider:** CoinDesk Data API

**Endpoint:** Historical OHLCV+ (hourly candlesticks)

**Instrument:** BTC-USD

**Market Index:** CADLI (CoinDesk Aggregate Digital Liquidity Index)

**Resolution:** 1-hour intervals

**Data Fields:** Open, High, Low, Close, Volume (OHLCV), with additional volume-related metrics

**Collection Method:** REST API requests with backward pagination

**Study Period:** January 2021 to the most recently available complete trading day at the time of data collection

**Reproducibility:** Data were fetched once and stored locally as a static dataset for all experiments

**Documentation:**
https://developers.coindesk.com/documentation/data-api/index_cc_v1_historical_hours


