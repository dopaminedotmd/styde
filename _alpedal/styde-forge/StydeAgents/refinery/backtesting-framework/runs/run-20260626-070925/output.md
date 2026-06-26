blueprint: Backtesting Framework
domain: trading
version: 1
purpose:
  Builds backtesting infrastructure for systematic trading strategies.
  Vectorized backtesting on daily to tick data.
  Walk-forward optimization with expanding/rolling windows.
  Monte Carlo simulations for robustness testing.
  Performance metrics: Sharpe, Sortino, Calmar, max drawdown, CAGR.
  Data pipeline: source from yfinance/polygon/CSV, clean outliers, adjust splits.
components:
  Data:
    source: yfinance | polygon.io | local CSV
    cleaning: remove NaN, adjust for splits, filter outliers beyond 5 std
    frequency: 1d | 1h | 1m | tick
    storage: parquet with date partitioning
  Vector:
    method: pandas/numpy vectorized operations on OHLCV arrays
    signals: computed column-based (SMA crossover, RSI, MACD)
    portfolio: equal-weight | volatility-target | risk-parity
    execution: fill at next open, slippage model (bps fixed), commission fixed per trade
  WalkForward:
    window_type: expanding | rolling
    train_size: 252 days (1 year)
    test_size: 63 days (1 quarter)
    step: 63 days
    selection: best Sharpe in train, validate on test
    output: parameter stability matrix, walk-forward equity curve
  MonteCarlo:
    runs: 10000
    method: scramble trade returns with replacement
    metrics_distribution: Sharpe, CAGR, maxDD, Calmar
    confidence: 95% VaR, 99% VaR
    output: histogram of outcomes, probability of negative return
  Metrics:
    Sharpe: mean(returns) / std(returns) * sqrt(252)
    Sortino: mean(returns) / downside_std * sqrt(252)
    Calmar: CAGR / abs(maxDD)
    MaxDD: max(trough_from_peak)
    CAGR: (final/initial)^(252/n) - 1
    WinRate: count(returns>0) / count(total)
    ProfitFactor: sum(gains) / abs(sum(losses))
  Architecture:
    pipeline: Data -> Vector -> Metrics
    optional: Data -> WalkForward -> Vector -> Metrics -> MonteCarlo
    output: equity_curve.csv, metrics.json, trades.csv, parameters.json
  edge_cases:
    - zero trades in window: skip, mark as inactive
    - insufficient history: pad with NaN, exclude from metric calc
    - single asset delisted: drop, rebalance remaining
    - survivorship bias: flag if using current index constituents