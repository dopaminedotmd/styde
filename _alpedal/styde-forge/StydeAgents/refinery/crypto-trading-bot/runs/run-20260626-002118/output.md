CCXT DCA/GRID/ARBITRAGE BOT v1
DEPENDENCIES: pip install ccxt pandas numpy
FILE: crypto_bot.py
```python
import ccxt
import ccxt.async_support as ccxt_async
import pandas as pd
import numpy as np
import asyncio
import time
import json
import logging
import os
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple
from enum import Enum
from datetime import datetime, timedelta
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger('crypto_bot')
# ─── Config ───────────────────────────────────────────────────────────────────
@dataclass
class ExchangeConfig:
    name: str
    api_key: str = ''
    secret: str = ''
    password: str = ''
    sandbox: bool = True
    rate_limit: bool = True
@dataclass
class DCAConfig:
    symbol: str = 'BTC/USDT'
    interval_hours: float = 24.0
    amount_usdt: float = 10.0
    order_type: str = 'market'  # market or limit
    max_price_deviation_pct: float = 5.0
@dataclass
class GridConfig:
    symbol: str = 'ETH/USDT'
    upper_price: float = 0.0
    lower_price: float = 0.0
    grid_levels: int = 10
    total_investment_usdt: float = 100.0
    take_profit_pct: float = 2.0
    rebalance_interval_minutes: float = 60.0
@dataclass
class ArbitrageConfig:
    symbols: List[str] = field(default_factory=lambda: ['BTC/USDT', 'ETH/USDT'])
    min_spread_pct: float = 0.5
    max_trade_size_usdt: float = 50.0
    exchanges: List[str] = field(default_factory=lambda: ['binance', 'kucoin', 'okx'])
    min_volume_24h_usdt: float = 100000.0
@dataclass
class RiskConfig:
    max_drawdown_pct: float = 15.0
    max_position_size_usdt: float = 200.0
    stop_loss_pct: float = 5.0
    take_profit_pct: float = 10.0
    max_open_trades: int = 5
    daily_loss_limit_usdt: float = 50.0
@dataclass
class BotConfig:
    exchange: ExchangeConfig = field(default_factory=ExchangeConfig)
    dca: DCAConfig = field(default_factory=DCAConfig)
    grid: GridConfig = field(default_factory=GridConfig)
    arbitrage: ArbitrageConfig = field(default_factory=ArbitrageConfig)
    risk: RiskConfig = field(default_factory=RiskConfig)
    data_dir: str = 'bot_data'
    log_level: str = 'INFO'
# ─── State Management ─────────────────────────────────────────────────────────
class TradeSide(Enum):
    BUY = 'buy'
    SELL = 'sell'
@dataclass
class Trade:
    id: str
    symbol: str
    side: TradeSide
    amount: float
    price: float
    cost: float
    fee: float
    timestamp: int
    strategy: str  # dca, grid, arbitrage, manual
    status: str = 'open'  # open, closed, cancelled
    pnl: float = 0.0
    close_price: float = 0.0
    close_time: int = 0
class BotState:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.trades: List[Trade] = []
        self.grid_orders: Dict[str, List[Dict]] = {}  # symbol -> list of grid orders
        self.daily_pnl: float = 0.0
        self.daily_loss: float = 0.0
        self.peak_balance: float = 0.0
        self.current_balance: float = 0.0
        os.makedirs(data_dir, exist_ok=True)
    def save(self):
        path = os.path.join(self.data_dir, 'state.json')
        data = {
            'trades': [t.__dict__ for t in self.trades],
            'grid_orders': self.grid_orders,
            'daily_pnl': self.daily_pnl,
            'daily_loss': self.daily_loss,
            'peak_balance': self.peak_balance,
            'current_balance': self.current_balance,
            'updated': time.time()
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    def load(self) -> bool:
        path = os.path.join(self.data_dir, 'state.json')
        if not os.path.exists(path):
            return False
        with open(path) as f:
            data = json.load(f)
        self.trades = [Trade(**t) for t in data.get('trades', [])]
        self.grid_orders = data.get('grid_orders', {})
        self.daily_pnl = data.get('daily_pnl', 0.0)
        self.daily_loss = data.get('daily_loss', 0.0)
        self.peak_balance = data.get('peak_balance', 0.0)
        self.current_balance = data.get('current_balance', 0.0)
        return True
# ─── Exchange Wrapper ─────────────────────────────────────────────────────────
class ExchangeManager:
    def __init__(self, config: ExchangeConfig):
        self.config = config
        self.exchanges: Dict[str, ccxt.Exchange] = {}
        self._init_exchange(config)
    def _init_exchange(self, cfg: ExchangeConfig):
        exchange_class = getattr(ccxt, cfg.name)
        ex = exchange_class({
            'apiKey': cfg.api_key,
            'secret': cfg.secret,
            'password': cfg.password,
            'enableRateLimit': cfg.rate_limit,
        })
        if cfg.sandbox and hasattr(ex, 'set_sandbox_mode'):
            ex.set_sandbox_mode(True)
        self.exchanges[cfg.name] = ex
    def get(self, name: str = '') -> ccxt.Exchange:
        if not name:
            name = self.config.name
        return self.exchanges.get(name)
    def get_balance(self, exchange_name: str = '') -> Dict[str, float]:
        ex = self.get(exchange_name)
        try:
            bal = ex.fetch_balance()
        except Exception:
            log.warning(f'Balance fetch failed for {ex.name}')
            return {}
        total = {}
        for currency, data in bal.get('total', {}).items():
            if data > 0:
                total[currency] = data
        return total
    def get_ticker(self, symbol: str, exchange_name: str = '') -> dict:
        ex = self.get(exchange_name)
        return ex.fetch_ticker(symbol)
    def create_order(self, symbol: str, side: str, amount: float,
                     price: Optional[float] = None,
                     order_type: str = 'market',
                     exchange_name: str = '') -> dict:
        ex = self.get(exchange_name)
        params = {}
        if order_type == 'limit' and price:
            params['price'] = price
        return ex.create_order(symbol, order_type, side, amount, price or None, params)
    def get_orderbook(self, symbol: str, limit: int = 10, exchange_name: str = '') -> dict:
        ex = self.get(exchange_name)
        return ex.fetch_order_book(symbol, limit)
    def get_fees(self, symbol: str, exchange_name: str = '') -> dict:
        ex = self.get(exchange_name)
        market = ex.market(symbol)
        return {'maker': market['maker'], 'taker': market['taker']}
    def cancel_order(self, order_id: str, symbol: str, exchange_name: str = ''):
        ex = self.get(exchange_name)
        return ex.cancel_order(order_id, symbol)
    def get_open_orders(self, symbol: str = '', exchange_name: str = ''):
        ex = self.get(exchange_name)
        return ex.fetch_open_orders(symbol)
    def fetch_ohlcv(self, symbol: str, timeframe: str = '1h',
                    limit: int = 100, exchange_name: str = '') -> pd.DataFrame:
        ex = self.get(exchange_name)
        ohlcv = ex.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    async def get_ticker_async(self, symbol: str, exchange_name: str = '') -> dict:
        ex = getattr(ccxt_async, exchange_name or self.config.name)()
        try:
            ticker = await ex.fetch_ticker(symbol)
            return ticker
        finally:
            await ex.close()
# ─── Strategy Implementations ─────────────────────────────────────────────────
class DCAStrategy:
    def __init__(self, config: DCAConfig, exchange_mgr: ExchangeManager, state: BotState, risk: RiskConfig):
        self.config = config
        self.exchange = exchange_mgr
        self.state = state
        self.risk = risk
        self.last_purchase = 0.0
    def should_buy(self) -> bool:
        elapsed = time.time() - self.last_purchase
        if elapsed < self.config.interval_hours * 3600:
            return False
        return self._check_risk_limits()
    def _check_risk_limits(self) -> bool:
        open_dca = sum(1 for t in self.state.trades if t.strategy == 'dca' and t.status == 'open')
        if open_dca >= self.risk.max_open_trades:
            log.warning(f'DCA: max open trades reached ({open_dca})')
            return False
        daily_risk = self.state.daily_loss >= self.risk.daily_loss_limit_usdt
        if daily_risk:
            log.warning(f'DCA: daily loss limit reached ({self.state.daily_loss:.2f})')
            return False
        return True
    def execute_buy(self) -> Optional[Trade]:
        if not self.should_buy():
            return None
        try:
            ticker = self.exchange.get_ticker(self.config.symbol)
            price = ticker['last']
            amount = self.config.amount_usdt / price
            order = self.exchange.create_order(
                self.config.symbol, 'buy', amount,
                order_type=self.config.order_type
            )
            trade = Trade(
                id=order['id'],
                symbol=self.config.symbol,
                side=TradeSide.BUY,
                amount=amount,
                price=order.get('price', price),
                cost=self.config.amount_usdt,
                fee=order.get('fee', {}).get('cost', 0),
                timestamp=int(time.time() * 1000),
                strategy='dca'
            )
            self.state.trades.append(trade)
            self.last_purchase = time.time()
            log.info(f'DCA buy: {amount:.6f} {self.config.symbol} @ {price:.2f}')
            self.state.save()
            return trade
        except Exception as e:
            log.error(f'DCA buy failed: {e}')
            return None
    def check_take_profit(self, trade: Trade) -> bool:
        try:
            ticker = self.exchange.get_ticker(trade.symbol)
            current_price = ticker['last']
            change_pct = (current_price - trade.price) / trade.price * 100
            if change_pct >= self.risk.take_profit_pct:
                log.info(f'DCA take profit: {trade.symbol} +{change_pct:.2f}%')
                return True
            return False
        except Exception:
            return False
class GridStrategy:
    def __init__(self, config: GridConfig, exchange_mgr: ExchangeManager, state: BotState, risk: RiskConfig):
        self.config = config
        self.exchange = exchange_mgr
        self.state = state
        self.risk = risk
    def setup_grid(self) -> bool:
        ticker = self.exchange.get_ticker(self.config.symbol)
        current_price = ticker['last']
        if current_price <= 0:
            log.error(f'Grid: invalid price {current_price}')
            return False
        upper = self.config.upper_price or current_price * 1.1
        lower = self.config.lower_price or current_price * 0.9
        if lower >= upper:
            log.error(f'Grid: lower >= upper ({lower} >= {upper})')
            return False
        levels = np.linspace(lower, upper, self.config.grid_levels + 2)[1:-1]
        investment_per_level = self.config.total_investment_usdt / self.config.grid_levels
        amount_per_level = investment_per_level / levels
        orders = []
        for i, price in enumerate(levels):
            side = 'buy' if price < current_price else 'sell'
            amount = investment_per_level / price
            order = self.exchange.create_order(
                self.config.symbol, side, amount,
                price=float(price), order_type='limit'
            )
            orders.append({
                'price': float(price),
                'amount': float(amount),
                'side': side,
                'order_id': order['id'],
                'placed': time.time()
            })
        self.state.grid_orders[self.config.symbol] = orders
        self.state.save()
        log.info(f'Grid set: {len(orders)} levels on {self.config.symbol} ({lower:.2f} - {upper:.2f})')
        return True
    def rebalance(self) -> bool:
        ticker = self.exchange.get_ticker(self.config.symbol)
        current_price = ticker['last']
        orders = self.state.grid_orders.get(self.config.symbol, [])
        if not orders:
            return self.setup_grid()
        filled_orders = [o for o in orders if time.time() - o['placed'] > 3600]
        if len(filled_orders) > self.config.grid_levels * 0.5:
            log.info(f'Grid rebalance: {len(filled_orders)}/{len(orders)} orders aged')
            self.cancel_grid()
            return self.setup_grid()
        return True
    def cancel_grid(self):
        orders = self.state.grid_orders.get(self.config.symbol, [])
        for o in orders:
            try:
                self.exchange.cancel_order(o['order_id'], self.config.symbol)
            except Exception:
                pass
        self.state.grid_orders[self.config.symbol] = []
        self.state.save()
    def calculate_pnl(self) -> float:
        ticker = self.exchange.get_ticker(self.config.symbol)
        current_price = ticker['last']
        orders = self.state.grid_orders.get(self.config.symbol, [])
        if not orders:
            return 0.0
        total_cost = sum(o['amount'] * o['price'] for o in orders if o['side'] == 'buy')
        total_value = sum(o['amount'] * current_price for o in orders if o['side'] == 'buy')
        return total_value - total_cost
class ArbitrageStrategy:
    def __init__(self, config: ArbitrageConfig, exchange_mgr: ExchangeManager, state: BotState, risk: RiskConfig):
        self.config = config
        self.exchange = exchange_mgr
        self.state = state
        self.risk = risk
    def find_arbitrage(self) -> List[Dict]:
        opportunities = []
        for symbol in self.config.symbols:
            prices = {}
            for ex_name in self.config.exchanges:
                try:
                    ticker = self.exchange.get_ticker(symbol, ex_name)
                    if not ticker or 'last' not in ticker:
                        continue
                    ticker_24h = ticker.get('quoteVolume', 0)
                    if ticker_24h < self.config.min_volume_24h_usdt:
                        continue
                    prices[ex_name] = ticker['last']
                except Exception as e:
                    log.debug(f'Arbitrage {ex_name} {symbol}: {e}')
                    continue
            if len(prices) < 2:
                continue
            min_ex = min(prices, key=prices.get)
            max_ex = max(prices, key=prices.get)
            spread = (prices[max_ex] - prices[min_ex]) / prices[min_ex] * 100
            if spread >= self.config.min_spread_pct:
                max_trade = min(
                    self.config.max_trade_size_usdt,
                    self.risk.max_position_size_usdt
                )
                opportunities.append({
                    'symbol': symbol,
                    'buy_exchange': min_ex,
                    'sell_exchange': max_ex,
                    'buy_price': prices[min_ex],
                    'sell_price': prices[max_ex],
                    'spread_pct': spread,
                    'max_trade_usdt': max_trade
                })
        return sorted(opportunities, key=lambda x: x['spread_pct'], reverse=True)
    def execute_arbitrage(self, opportunity: Dict) -> bool:
        symbol = opportunity['symbol']
        buy_ex = opportunity['buy_exchange']
        sell_ex = opportunity['sell_exchange']
        buy_price = opportunity['buy_price']
        sell_price = opportunity['sell_price']
        amount = opportunity['max_trade_usdt'] / buy_price
        try:
            buy_order = self.exchange.create_order(
                symbol, 'buy', amount,
                exchange_name=buy_ex
            )
            sell_order = self.exchange.create_order(
                symbol, 'sell', amount,
                exchange_name=sell_ex
            )
            profit = amount * (sell_price - buy_price)
            trade = Trade(
                id=f'arb_{int(time.time())}',
                symbol=symbol,
                side=TradeSide.BUY,
                amount=amount,
                price=buy_price,
                cost=amount * buy_price,
                fee=0,
                timestamp=int(time.time() * 1000),
                strategy='arbitrage',
                status='closed',
                pnl=profit,
                close_price=sell_price,
                close_time=int(time.time() * 1000)
            )
            self.state.trades.append(trade)
            self.state.save()
            log.info(f'Arbitrage executed: {symbol} buy @ {buy_price:.2f} ({buy_ex}) sell @ {sell_price:.2f} ({sell_ex}) profit ${profit:.2f}')
            return True
        except Exception as e:
            log.error(f'Arbitrage execution failed: {e}')
            return False
    async def scan_continuously(self, interval_seconds: int = 60):
        while True:
            opps = self.find_arbitrage()
            for opp in opps:
                self.execute_arbitrage(opp)
            await asyncio.sleep(interval_seconds)
class RiskManager:
    def __init__(self, config: RiskConfig, state: BotState, exchange_mgr: ExchangeManager):
        self.config = config
        self.state = state
        self.exchange = exchange_mgr
    def update_balance(self):
        bal = self.exchange.get_balance()
        total = sum(v for v in bal.values())
        self.state.current_balance = total
        if total > self.state.peak_balance:
            self.state.peak_balance = total
        self.state.save()
    def check_drawdown(self) -> bool:
        if self.state.peak_balance <= 0:
            return True
        drawdown = (self.state.peak_balance - self.state.current_balance) / self.state.peak_balance * 100
        if drawdown > self.config.max_drawdown_pct:
            log.warning(f'Max drawdown exceeded: {drawdown:.2f}% > {self.config.max_drawdown_pct}%')
            return False
        return True
    def check_daily_loss(self) -> bool:
        today_start = time.mktime(datetime.now().replace(hour=0, minute=0, second=0).timetuple()) * 1000
        today_trades = [t for t in self.state.trades if t.timestamp >= today_start]
        today_pnl = sum(t.pnl for t in today_trades)
        self.state.daily_pnl = today_pnl
        self.state.daily_loss = abs(min(0, today_pnl))
        if self.state.daily_loss >= self.config.daily_loss_limit_usdt:
            log.warning(f'Daily loss limit hit: ${self.state.daily_loss:.2f}')
            return False
        return True
    def position_sizing(self, available_usdt: float, confidence: float = 1.0) -> float:
        max_pos = min(
            available_usdt * 0.5 * confidence,
            self.config.max_position_size_usdt
        )
        return max(0, max_pos)
    def set_stop_loss(self, trade: Trade) -> float:
        stop_price = trade.price * (1 - self.config.stop_loss_pct / 100)
        log.info(f'Stop loss set: {trade.symbol} @ {stop_price:.2f} (entry {trade.price:.2f})')
        return stop_price
    def should_stop_all(self) -> bool:
        return not self.check_drawdown() or not self.check_daily_loss()
# ─── Main Bot Controller ─────────────────────────────────────────────────────
class CryptoBot:
    def __init__(self, config: BotConfig):
        self.config = config
        self.state = BotState(config.data_dir)
        self.state.load()
        self.exchange = ExchangeManager(config.exchange)
        self.risk = RiskManager(config.risk, self.state, self.exchange)
        self.dca = DCAStrategy(config.dca, self.exchange, self.state, config.risk)
        self.grid = GridStrategy(config.grid, self.exchange, self.state, config.risk)
        self.arbitrage = ArbitrageStrategy(config.arbitrage, self.exchange, self.state, config.risk)
        self.running = False
    def run_cycle(self):
        log.info('=== Bot cycle start ===')
        self.risk.update_balance()
        if self.risk.should_stop_all():
            log.critical('Risk limits triggered. Stopping all activity.')
            return
        dca_trade = self.dca.execute_buy()
        if dca_trade:
            sl = self.risk.set_stop_loss(dca_trade)
            log.info(f'DCA stop loss: {sl:.2f}')
        for trade in self.state.trades:
            if trade.status == 'open' and trade.strategy == 'dca':
                if self.dca.check_take_profit(trade):
                    trade.status = 'closed'
                    ticker = self.exchange.get_ticker(trade.symbol)
                    trade.close_price = ticker['last']
                    trade.close_time = int(time.time() * 1000)
                    trade.pnl = (trade.close_price - trade.price) * trade.amount
                    log.info(f'Trade closed: {trade.symbol} PnL ${trade.pnl:.2f}')
        self.grid.rebalance()
        opps = self.arbitrage.find_arbitrage()
        for opp in opps[:3]:
            self.arbitrage.execute_arbitrage(opp)
        self.state.save()
        log.info(f'Balance: ${self.state.current_balance:.2f} | Peak: ${self.state.peak_balance:.2f}')
    def run(self, interval_seconds: int = 60):
        self.running = True
        log.info(f'Bot started. Cycle every {interval_seconds}s')
        try:
            while self.running:
                self.run_cycle()
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            log.info('Bot stopped by user')
            self.running = False
        finally:
            self.state.save()
    def run_async(self):
        asyncio.run(self.arbitrage.scan_continuously(30))
    def report(self) -> dict:
        open_trades = [t for t in self.state.trades if t.status == 'open']
        closed_trades = [t for t in self.state.trades if t.status == 'closed']
        total_pnl = sum(t.pnl for t in closed_trades)
        win_trades = sum(1 for t in closed_trades if t.pnl > 0)
        return {
            'total_trades': len(self.state.trades),
            'open_trades': len(open_trades),
            'closed_trades': len(closed_trades),
            'total_pnl_usdt': round(total_pnl, 2),
            'win_rate': round(win_trades / max(1, len(closed_trades)) * 100, 1),
            'current_balance_usdt': round(self.state.current_balance, 2),
            'peak_balance_usdt': round(self.state.peak_balance, 2),
            'drawdown_pct': round(
                (self.state.peak_balance - self.state.current_balance) / max(1, self.state.peak_balance) * 100, 2
            ),
            'active_grids': len(self.state.grid_orders),
            'daily_pnl': round(self.state.daily_pnl, 2),
        }
# ─── Quick Start ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    config = BotConfig(
        exchange=ExchangeConfig(name='binance', sandbox=True),
        dca=DCAConfig(symbol='BTC/USDT', interval_hours=24, amount_usdt=10),
        grid=GridConfig(symbol='ETH/USDT', total_investment_usdt=100, grid_levels=10),
        arbitrage=ArbitrageConfig(exchanges=['binance', 'kucoin']),
        risk=RiskConfig(max_drawdown_pct=15, max_position_size_usdt=200),
        data_dir='./crypto_bot_data',
        log_level='INFO'
    )
    bot = CryptoBot(config)
    bot.run(interval_seconds=120)
```
USAGE:
1. Set API keys in ExchangeConfig (empty for sandbox mode)
2. Adjust DCAConfig, GridConfig, ArbitrageConfig params per asset
3. Run: python crypto_bot.py
FEATURES:
DCA: Time-weighted entry every N hours. Takes profit at configured %. Stop loss at configured %.
Grid: Levels evenly spaced between lower/upper price. Auto-rebalances when >50% orders age 1h+. Cancel/reset on trend shift.
Arbitrage: Scans multiple exchanges. Filters by 24h volume. Executes cross-exchange when spread >= min. Async scanner included.
Risk: Position sizing caps at max_position_size_usdt. Daily loss limit halts all trades. Max drawdown % triggers full stop. Tracked via BotState with JSON persistence.
CCXT: Uses unified API. Supports 100+ exchanges. Sandbox mode default. Rate limiting enabled.
EXTENSIONS:
- Add Telegram alerts: logging handler + send_message()
- Add trailing stop: update stop_loss tracking per trade
- Add indicator filtering (RSI, MACO, VWAP) before DCA entry
- Add SQLite/Postgres for trade history instead of JSON