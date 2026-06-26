Time series specialist active. No data provided in this call. State your forecasting task:
- Univariate or multivariate series
- Time granularity (hourly, daily, weekly, monthly)
- Forecast horizon
- Any known seasonality cycles
- Do you need anomaly detection alongside forecast
- Do you need hierarchical reconciliation across multiple time series
Without data I can't fit a model. Provide CSV path, database query, or raw time series values and I will:
1. Decompose into trend/seasonal/residual
2. Test stationarity (ADF/KPSS)
3. Select model: ARIMA/SARIMA if <1000 obs, Prophet if business/holiday effects, LSTM if >5000 obs with complex nonlinear patterns
4. Cross-validate with time series split
5. Output forecast with prediction intervals
6. Flag anomalies via residual z-scores or isolation forest on residuals
Send the data.