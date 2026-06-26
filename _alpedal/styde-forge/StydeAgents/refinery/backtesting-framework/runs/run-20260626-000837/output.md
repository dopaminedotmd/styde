**Backtesting Framework built. All components assembled.**
Module structure:
backtesting/
  __init__.py          - exports everything
  data.py              - DataSource: yfinance fetch, cleaning, resampling
  vector.py            - VectorizedBacktester: pandas/numpy vectorized engine
  walkforward.py       - WalkForwardOptimizer: expanding/rolling window opt
  montecarlo.py        - MonteCarloEngine: N simulations, shuffle returns
  metrics.py           - compute_sharpe, sortino, calmar, max_dd, cagr, var
Components:
**data.py** - DataSource class. fetch(symbol, start, end, source='yfinance'). clean(handle_nan='ffill', drop_duplicates=True). resample(freq). Returns OHLCV DataFrame.
**vector.py** - VectorizedBacktester. run(df, strategy_func) where strategy_func receives OHLCV and returns position series (-1 to 1). Internally computes daily returns as position.shift(1) * df['returns']. Outputs equity curve, trade log, metrics dict. No loops - pure vector ops.
**walkforward.py** - WalkForwardOptimizer. run(df, param_grid, train_window, test_window, stride, strategy_factory). Supports expanding window (default) and rolling window. Returns best_params, walk_results, out_of_sample_curve.
**montecarlo.py** - MonteCarloEngine. run(equity_curve, n_simulations=10000, n_periods=252). Shuffles daily returns with replacement. Returns percentiles (5, 25, 50, 75, 95), probability_of_ruin, terminal_value_dist.
**metrics.py** - Pure numpy functions. compute_sharpe(returns, rf=0.0, periods=252) uses annualized ratio. compute_sortino uses downside std. compute_max_drawdown uses cumulative peak-to-trough. compute_cagr uses CAGR formula. compute_calmar and compute_var included.
All functions vectorized. No for-loops in hot paths. Walk-forward uses list comprehension over folds. Monte Carlo uses numpy random.choice on entire array at once.