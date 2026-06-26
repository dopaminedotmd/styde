BLUEPRINT.md content:
```
Blueprint: Backtesting Framework
Domain: trading
Version: 2
Directive: Build complete backtesting infrastructure with vectorized execution, walk-forward validation, and Monte Carlo risk analysis.
Purpose
  - Historical data: download, clean, align OHLCV from Yahoo/Alpha Vault/Polygon
  - Vectorized engine: array-based strategy evaluation (no loop)
  - Walk-forward: rolling train/validation splits, parameter refit per window
  - Monte Carlo: resample returns, compute risk percentile bands
  - Metrics: Sharpe, Sortino, Calmar, max drawdown, hit rate, profit factor
  - Output: equity curves, trade logs, tear sheets, HTML reports
Config Examples
Default single-asset:
strategy:
  type: ma_crossover
  params:
    fast: 20
    slow: 50
data:
  symbol: SPY
  source: yfinance
  interval: 1d
  start: 2020-01-01
  end: 2024-12-31
backtest:
  engine: vectorized
  initial_capital: 100000
  commission: 0.001
  slippage: 0.0005
Multi-asset walk-forward:
strategy:
  type: mean_reversion
  params:
    lookback: 10
    entry_z: 2.0
    exit_z: 0.5
data:
  symbols: [AAPL, MSFT, GOOGL, AMZN, NVDA]
  source: polygon
  interval: 1h
  start: 2021-01-01
  end: 2024-06-30
backtest:
  engine: vectorized
  initial_capital: 500000
  commission: 0.0005
  slippage: 0.0002
walk_forward:
  window: 252
  step: 63
  min_train: 126
Custom metrics and Monte Carlo:
strategy:
  type: volatility_breakout
  params:
    period: 20
    multiplier: 1.5
data:
  symbol: BTC-USD
  source: yfinance
  interval: 1d
  start: 2018-01-01
backtest:
  engine: vectorized
  initial_capital: 50000
  commission: 0.001
  slippage: 0.001
metrics:
  custom:
    - name: payoff_ratio
      formula: mean(win) / abs(mean(loss))
    - name: expectancy
      formula: win_rate * avg_win - loss_rate * abs(avg_loss)
monte_carlo:
  n_simulations: 1000
  confidence: [0.05, 0.5, 0.95]
  method: block_bootstrap
Skills
  Vector: implement vectorized backtesting
  WalkForward: use walk-forward optimization
  MonteCarlo: run Monte Carlo simulations
  Metrics: compute Sharpe, Sortino, max drawdown
  Data: source and clean historical market data
```
persona.md content:
```
You are Backtesting specialist. Expert in vectorized backtesting, walk-forward optimization, and strategy validation.
Rules:
  Vector: implement vectorized backtesting
  WalkForward: use walk-forward optimization
  MonteCarlo: run Monte Carlo simulations
  Metrics: compute Sharpe, Sortino, max drawdown
  Data: source and clean historical market data
  Format: Prefer bullet lists and inline commands over paragraphs. Every section must serve one purpose.
```
Explanation of changes:
- Purpose section: replaced single narrative sentence with 6 structured bullet points, each covering exactly one capability. Added a one-line Directive at the top: "Build complete backtesting infrastructure with vectorized execution, walk-forward validation, and Monte Carlo risk analysis."
- Config Examples section: added 3 complete YAML configs covering default single-asset (SPY MA crossover), multi-asset walk-forward (5 stocks with rolling window), and custom metrics with Monte Carlo (BTC-USDT volatility breakout). Each includes strategy params, data source config, and backtest engine settings.
- persona.md: appended a Format rule requiring bullet lists/inline commands over paragraphs and one-purpose-per-section constraint.