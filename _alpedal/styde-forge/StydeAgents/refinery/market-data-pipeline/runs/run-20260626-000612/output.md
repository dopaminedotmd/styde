Market Data Pipeline - blueprints/market_data_pipeline
Blueprint created with 3 files:
BLUEPRINT.md
- Purpose: Builds real-time market data pipelines. WebSocket feeds, order book, tick aggregation.
- Domain: trading, Version: 1
- Skills: WebSocket, OrderBook, Aggregate, Latency, Store
persona.md
- Market data engineer persona. Rules: WebSocket connect, OrderBook reconstruct, OHLCV aggregate, minimize latency, time-series store.
config.yaml
- Blueprint config. domain: trading, name: market-data-pipeline. Toolsets: terminal, file, web. Model: deepseek-v4-flash. Judge: deepseek-v4-pro.
Skills directory with 5 skill files:
skills/websocket.md
- Connect to exchange WebSocket feeds. Handle reconnection. Manage subscriptions. Parse binary frames (SBE, Simple Binary Encoding). Handle connection pool.
skills/orderbook.md
- Reconstruct order book from L2/L3 deltas. Maintain price-time priority queue. Handle snapshots and sequencing. Detect straddles and iceburg orders.
skills/aggregate.md
- Aggregate ticks into OHLCV bars. Support 1s, 1m, 5m, 15m, 1h, 1d resolutions. Handle tick-rule sign generation. Real-time bar emission with timestamp alignment.
skills/latency.md
- Minimize end-to-end latency. Use async I/O. Batch writes. Zero-copy deserialization. Monitor p50/p99/p999 latency histograms.
skills/store.md
- Use time-series databases for tick data. InfluxDB for ticks, Parquet for cold storage. Compression strategy. Retention policies. Write-ahead log for crash recovery.
Blueprint validated. 0 errors. 0 warnings.
Agent ready for spawn. Task: connect Binance WebSocket stream for BTC-USDT, reconstruct order book, emit 1s OHLCV bars, store ticks in InfluxDB. Target end-to-end latency under 50ms p99.