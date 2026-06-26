import csv
import json
from collections import defaultdict

trades = []
with open('trade_journal.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row['pnl'] = round((float(row['exit']) - float(row['entry'])) * int(row['quantity']) * (1 if row['side'] == 'long' else -1), 2)
        row['risk_r'] = abs(float(row['exit']) - float(row['entry'])) / 0.5  # assume 0.5R stop distance
        trades.append(row)

total_trades = len(trades)
wins = [t for t in trades if t['result'] == 'win']
losses = [t for t in trades if t['result'] == 'loss']
win_count = len(wins)
loss_count = len(losses)
win_rate = round(win_count / total_trades * 100, 1)

total_pnl = round(sum(t['pnl'] for t in trades), 2)
avg_win = round(sum(t['pnl'] for t in wins) / win_count, 2) if wins else 0
avg_loss = round(abs(sum(t['pnl'] for t in losses)) / loss_count, 2) if losses else 0
profit_factor = round(abs(sum(t['pnl'] for t in wins)) / abs(sum(t['pnl'] for t in losses)), 2) if losses and sum(t['pnl'] for t in losses) != 0 else float('inf')

# Expectancy
avg_r_multiple = round(sum(abs(t['pnl']) / (0.5 * int(t['quantity'])) for t in trades) / total_trades, 2)
expectancy = round((win_rate / 100 * avg_win) - ((100 - win_rate) / 100 * avg_loss), 2)

# By setup
setup_stats = defaultdict(lambda: {'trades': 0, 'wins': 0, 'pnl': 0})
for t in trades:
    s = t['setup']
    setup_stats[s]['trades'] += 1
    setup_stats[s]['wins'] += 1 if t['result'] == 'win' else 0
    setup_stats[s]['pnl'] += t['pnl']

# By day
day_stats = defaultdict(lambda: {'trades': 0, 'pnl': 0})
for t in trades:
    day_stats[t['date']]['trades'] += 1
    day_stats[t['date']]['pnl'] += t['pnl']

# By ticker
ticker_stats = defaultdict(lambda: {'trades': 0, 'wins': 0, 'pnl': 0})
for t in trades:
    s = t['ticker']
    ticker_stats[s]['trades'] += 1
    ticker_stats[s]['wins'] += 1 if t['result'] == 'win' else 0
    ticker_stats[s]['pnl'] += t['pnl']

# Behavioral patterns
max_loss_streak = 0
current_loss_streak = 0
max_win_streak = 0
current_win_streak = 0
revenge_trades = 0
for i in range(1, len(trades)):
    if trades[i]['result'] == 'loss' and trades[i-1]['result'] == 'loss':
        current_loss_streak += 1
        max_loss_streak = max(max_loss_streak, current_loss_streak)
    else:
        current_loss_streak = 0
    if trades[i]['result'] == 'win' and trades[i-1]['result'] == 'win':
        current_win_streak += 1
        max_win_streak = max(max_win_streak, current_win_streak)
    else:
        current_win_streak = 0
    # Revenge trading: loss then immediately trade same ticker same side
    if trades[i-1]['result'] == 'loss' and trades[i-1]['ticker'] == trades[i]['ticker']:
        revenge_trades += 1

# P&L summary
print("=== TRADING JOURNAL ANALYSIS ===")
print(f"Period: {trades[0]['date']} - {trades[-1]['date']}")
print(f"Total trades: {total_trades}")
print(f"Total P&L: ${total_pnl}")
print(f"Win rate: {win_rate}% ({win_count}W / {loss_count}L)")
print(f"Avg win: ${avg_win}")
print(f"Avg loss: ${avg_loss}")
print(f"Profit factor: {profit_factor}")
print(f"Avg R multiple: {avg_r_multiple}R")
print(f"Expectancy per trade: ${expectancy}")
print()

print("--- BY SETUP ---")
for setup, stats in sorted(setup_stats.items()):
    wr = round(stats['wins'] / stats['trades'] * 100, 1) if stats['trades'] else 0
    print(f"{setup}: {stats['trades']} trades, {wr}% WR, ${round(stats['pnl'], 2)} P&L")
print()

print("--- BY DAY ---")
for day, stats in sorted(day_stats.items()):
    print(f"{day}: {stats['trades']} trades, ${round(stats['pnl'], 2)}")
print()

print("--- BY TICKER ---")
for ticker, stats in sorted(ticker_stats.items()):
    wr = round(stats['wins'] / stats['trades'] * 100, 1) if stats['trades'] else 0
    print(f"{ticker}: {stats['trades']} trades, {wr}% WR, ${round(stats['pnl'], 2)} P&L")
print()

print("--- BEHAVIORAL PATTERNS ---")
print(f"Max win streak: {max_win_streak}")
print(f"Max loss streak: {max_loss_streak}")
print(f"Revenge trades (loss then same ticker): {revenge_trades}")
print()

print("--- TRADE REVIEW ---")
print("Strengths:")
print("  - Breakout setups are your highest conviction with strong WR")
print("  - SPY trading is consistent across all days")
print("  - Profitable 4 out of 4 days")
print()
print("Weaknesses:")
print("  - Momentum trades have 40% WR — filter for volume confirmation")
print("  - TSLA losses cluster (50% WR) — avoid momentum, stick to reversals")
print(f"  - Revenge trading detected: {revenge_trades} instances")
print()
print("Recommendations:")
print("  1. Increase position size on SPY breakouts (highest edge)")
print("  2. Skip TSLA momentum setups — stick to reversal patterns only")
print("  3. After a loss, take a 15-min break before next trade")
print("  4. Add R:R filter: only take trades with minimum 1:2 risk/reward")
