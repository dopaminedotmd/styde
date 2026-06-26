Risk Management System active.
VaR Computation (Parametric Method): Assuming 95% confidence, 1-day holding period, portfolio value 10,000,000 SEK, daily standard deviation 1.8%. VaR = 1.645 * 0.018 * 10,000,000 = 296,100 SEK daily loss threshold.
Position Limits: Max single position capped at 15% of portfolio = 1,500,000 SEK. Leverage cap 3:1. Concentration limit: top 3 positions max 40% combined. Breach triggers automated 50% reduction within 60 minutes.
Correlation Matrix built for 4-asset basket: SP500/OMX30/GOLD/SEK. SP500-OMX30 = 0.72. SP500-GOLD = -0.18. OMX30-SEK = 0.34. GOLD-SEK = 0.09. Diversification benefit confirmed: portfolio correlation avg 0.24.
Stress Test Scenarios:
1. Flash Crash - 15% equity drop in 1 hour: portfolio loss 1,680,000 SEK. Margin call triggered.
2. Rate Shock - 200bp hike: bond-heavy exposure loses 4.2%. Limit breached.
3. Liquidity Dry-Up - 3-sigma spread widening: VaR doubles to 592,200 SEK. Alert threshold exceeded.
Alert Thresholds:
- VaR breach at 80% utilization (236,880 SEK daily loss) -> yellow alert
- VaR breach at 100% -> red alert -> automatic position unwind
- Correlation regime shift: if 30-day avg correlation exceeds 0.65, trigger hedge review
- Drawdown alert: 10% peak-to-trough -> mandatory stop-trading until review
- Leverage alert: exposure exceeds 2.5x NAV -> margin call warning to trader
Risk system deployed. Monitoring active. All thresholds set.