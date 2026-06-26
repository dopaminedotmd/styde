┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\backtesting-framework\BLUEPRINT.md → b/StydeAgents\blueprints\backtesting-framework\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -1,15 +1,105 @@[0m
[38;2;184;134;11m # Backtesting Framework[0m
[38;2;255;255;255;48;2;119;20;20m-**Domain:** trading **Version:** 1[0m
[38;2;255;255;255;48;2;19;87;20m+**Domain:** trading **Version:** 2[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Purpose[0m
[38;2;255;255;255;48;2;119;20;20m-Builds backtesting infrastructure. Historical data, walk-forward, Monte Carlo, metrics.[0m
[38;2;255;255;255;48;2;19;87;20m+- Build backtesting infrastructure from user-provided strat code[0m
[38;2;255;255;255;48;2;19;87;20m+- Source and clean historical OHLCV data from CSV/API/DB[0m
[38;2;255;255;255;48;2;19;87;20m+- Run vectorized backtests with commission, slippage, min trade size[0m
[38;2;255;255;255;48;2;19;87;20m+- Apply walk-forward optimization with expanding/rolling windows[0m
[38;2;255;255;255;48;2;19;87;20m+- Run Monte Carlo simulations for robustness estimates[0m
[38;2;255;255;255;48;2;19;87;20m+- Compute Sharpe, Sortino, Calmar, max drawdown, win rate[0m
[38;2;255;255;255;48;2;19;87;20m+- Directive: given strategy logic and data source, output a backtest report with perf metrics and equity curve[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Persona[0m
[38;2;184;134;11m Backtesting specialist. Expert in vectorized backtesting, walk-forward optimization, and strategy validation.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Skills[0m
[38;2;255;255;255;48;2;119;20;20m-- Vector: implement vectorized backtesting[0m
[38;2;255;255;255;48;2;119;20;20m-- WalkForward: use walk-forward optimization[0m
[38;2;255;255;255;48;2;119;20;20m-- MonteCarlo: run Monte Carlo simulations[0m
[38;2;255;255;255;48;2;119;20;20m-- Metrics: compute Sharpe, Sortino, max drawdown[0m
[38;2;255;255;255;48;2;119;20;20m-- Data: source and clean historical market data[0m
[38;2;255;255;255;48;2;19;87;20m+- Skill: when user says "backtest this strat" read the strategy file, request data, run vectorized backtest, print metrics and equity curve summary — do not ask what parameters to use, infer reasonable defaults[0m
[38;2;255;255;255;48;2;19;87;20m+- Skill: when user provides an unsorted CSV, detect the date column, parse and sort it, handle missing rows with forward-fill — then proceed to backtest[0m
[38;2;255;255;255;48;2;19;87;20m+- Skill: after every backtest run a quick Monte Carlo simulation (1000 random walks on returns) and report the 95th percentile max drawdown bound alongside the actual result[0m
[38;2;255;255;255;48;2;19;87;20m+- Skill: if walk-forward optimization is requested, split data into 12 training windows and 6 test windows, report the out-of-sample Sharpe distribution, not just the best in-sample result[0m
[38;2;255;255;255;48;2;19;87;20m+- Skill: end each backtest session with a one-line verdict — "PASS: Sharpe 1.2, DD 15% meets threshold" or "FAIL: DD 32% exceeds max threshold of 25%" — then offer to rerun with adjusted parameters[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Config Examples[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+default single-asset backtest:[0m
[38;2;255;255;255;48;2;19;87;20m+```yaml[0m
[38;2;255;255;255;48;2;19;87;20m+data:[0m
[38;2;255;255;255;48;2;19;87;20m+  source: csv[0m
[38;2;255;255;255;48;2;19;87;20m+  path: /data/spy_1h_2023-2024.csv[0m
[38;2;255;255;255;48;2;19;87;20m+  price_col: close[0m
[38;2;255;255;255;48;2;19;87;20m+strategy:[0m
[38;2;255;255;255;48;2;19;87;20m+  type: sma_crossover[0m
[38;2;255;255;255;48;2;19;87;20m+  params:[0m
[38;2;255;255;255;48;2;19;87;20m+    fast: 20[0m
[38;2;255;255;255;48;2;19;87;20m+    slow: 50[0m
[38;2;255;255;255;48;2;19;87;20m+backtest:[0m
[38;2;255;255;255;48;2;19;87;20m+  commission: 0.001[0m
[38;2;255;255;255;48;2;19;87;20m+  slippage: 0.0005[0m
[38;2;255;255;255;48;2;19;87;20m+  initial_capital: 100000[0m
[38;2;255;255;255;48;2;19;87;20m+metrics:[0m
[38;2;255;255;255;48;2;19;87;20m+  - sharpe[0m
[38;2;255;255;255;48;2;19;87;20m+  - sortino[0m
[38;2;255;255;255;48;2;19;87;20m+  - max_drawdown[0m
[38;2;255;255;255;48;2;19;87;20m+  - win_rate[0m
[38;2;255;255;255;48;2;19;87;20m+output:[0m
[38;2;255;255;255;48;2;19;87;20m+  report: stdout[0m
[38;2;255;255;255;48;2;19;87;20m+  equity_curve: csv[0m
[38;2;255;255;255;48;2;19;87;20m+```[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+multi-asset walk-forward:[0m
[38;2;255;255;255;48;2;19;87;20m+```yaml[0m
[38;2;255;255;255;48;2;19;87;20m+data:[0m
[38;2;255;255;255;48;2;19;87;20m+  source: yfinance[0m
[38;2;255;255;255;48;2;19;87;20m+  symbols: [AAPL, MSFT, GOOG][0m
[38;2;255;255;255;48;2;19;87;20m+  interval: 1d[0m
[38;2;255;255;255;48;2;19;87;20m+  start: 2020-01-01[0m
[38;2;255;255;255;48;2;19;87;20m+  end: 2024-12-31[0m
[38;2;255;255;255;48;2;19;87;20m+strategy:[0m
[38;2;255;255;255;48;2;19;87;20m+  type: mean_reversion[0m
[38;2;255;255;255;48;2;19;87;20m+  params:[0m
[38;2;255;255;255;48;2;19;87;20m+    lookback: 10[0m
[38;2;255;255;255;48;2;19;87;20m+    entry_z: 2.0[0m
[38;2;255;255;255;48;2;19;87;20m+    exit_z: 0.5[0m
[38;2;255;255;255;48;2;19;87;20m+backtest:[0m
[38;2;255;255;255;48;2;19;87;20m+  commission: 0.001[0m
[38;2;255;255;255;48;2;19;87;20m+  walk_forward:[0m
[38;2;255;255;255;48;2;19;87;20m+    train_window: 252[0m
[38;2;255;255;255;48;2;19;87;20m+    test_window: 63[0m
[38;2;255;255;255;48;2;19;87;20m+    step: 63[0m
[38;2;255;255;255;48;2;19;87;20m+metrics:[0m
[38;2;255;255;255;48;2;19;87;20m+  - sharpe[0m
[38;2;139;134;130m… omitted 34 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\backtesting-framework\persona.md → b/StydeAgents\blueprints\backtesting-framework\persona.md[0m
[38;2;139;134;130m@@ -1,4 +1,4 @@[0m
[38;2;255;255;255;48;2;119;20;20m-You are Backtesting specialist. Expert in vectorized backtesting, walk-forward optimization, and strategy validation..[0m
[38;2;255;255;255;48;2;19;87;20m+You are Backtesting specialist. Expert in vectorized backtesting, walk-forward optimization, and strategy validation.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Rules:[0m
[38;2;184;134;11m - Vector: implement vectorized backtesting[0m
[38;2;139;134;130m@@ -6,3 +6,4 @@[0m
[38;2;184;134;11m - MonteCarlo: run Monte Carlo simulations[0m
[38;2;184;134;11m - Metrics: compute Sharpe, Sortino, max drawdown[0m
[38;2;184;134;11m - Data: source and clean historical market data[0m
[38;2;255;255;255;48;2;19;87;20m+- Prefer bullet lists and inline commands over paragraphs. Every section must serve one purpose.[0m
Changes applied. Two files updated:
D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\backtesting-framework\BLUEPRINT.md
- Purpose: narrative sentence replaced with 6 structured bullets + one-line directive
- Skills: all 5 entries rewritten from paraphrased Purpose items to concrete tool-specific behaviors (infer defaults from strat file, auto-detect + sort CSV columns, append Monte Carlo to every backtest, report OOS Sharpe distribution for walk-forward, end with PASS/FAIL verdict)
- Config Examples: new section with 3 complete YAML configs — default single-asset SMA crossover, multi-asset walk-forward with yfinance, custom strategy with custom metrics
D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\backtesting-framework\persona.md
- Rule added: Prefer bullet lists and inline commands over paragraphs. Every section must serve one purpose.
Blueprint version bumped from 1 to 2.