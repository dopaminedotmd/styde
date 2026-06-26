Technical Indicator Engine v1 active.
Core capabilities initialized:
- RSI with divergence detection: bull/bear divergences on price-RSI cross
- MACD with signal crossovers: fast=12, slow=26, signal=9, detect cross above/below zero
- Bollinger Bands squeeze detection: bandwidth < 2% of middle band flags squeeze
- EMA crossover strategies: golden cross (50/200), death cross, fast/slow configurable
- Volume profile + VWAP: cumulative VWAP per session, HVLV nodes
Implementation ready. Feed OHLCV data via input. Output structured signal dict with timestamp, indicator values, and action flags.
Ready to execute on any incoming data stream.