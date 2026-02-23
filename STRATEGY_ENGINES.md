# VeighNa Strategy Engines Overview

VeighNa provides **5 different strategy engines**, each designed for specific trading scenarios and use cases.

---

## 1. CTA Strategy Engine (`vnpy_ctastrategy`)

**Purpose:** Single-contract trend-following and mean-reversion strategies

**Version:** 1.4.1

**Key Features:**
- Single asset trading (futures, crypto perpetuals)
- Bar-based (K-line) strategy execution
- Built-in backtesting engine
- Stop order support (for reducing slippage)
- Real-time strategy monitoring and control

**Core Components:**
```
vnpy_ctastrategy/
├── template.py         # CtaTemplate, CtaSignal, TargetPosTemplate
├── engine.py           # CtaEngine (strategy management)
├── backtesting.py      # BacktestingEngine
├── base.py             # APP_NAME, StopOrder
└── strategies/         # Built-in strategy examples
```

**Built-in Strategies (9):**
| Strategy | Description |
|----------|-------------|
| `AtrRsiStrategy` | ATR + RSI combined signal strategy |
| `BollChannelStrategy` | Bollinger Bands channel breakout |
| `DoubleMaStrategy` | Dual moving average crossover |
| `DualThrustStrategy` | Dual Thrust range breakout |
| `KingKeltnerStrategy` | Keltner Channel trend following |
| `MultiSignalStrategy` | Multiple signal combination |
| `MultiTimeframeStrategy` | Multi-timeframe analysis |
| `TurtleSignalStrategy` | Turtle Trading rules |
| `TestStrategy` | Template for testing |

**Strategy Template API:**
```python
class CtaTemplate:
    # Callbacks
    def on_init(self): pass         # Strategy initialization
    def on_start(self): pass        # Strategy start
    def on_stop(self): pass         # Strategy stop
    def on_tick(self, tick: TickData): pass    # Tick update
    def on_bar(self, bar: BarData): pass       # Bar update (main entry point)
    def on_trade(self, trade: TradeData): pass # Trade fill
    def on_order(self, order: OrderData): pass # Order update
    def on_stop_order(self, stop_order: StopOrder): pass
    
    # Action methods
    def buy(self, price, volume, stop=False): pass    # Open long
    def sell(self, price, volume, stop=False): pass   # Close long
    def short(self, price, volume, stop=False): pass  # Open short
    def cover(self, price, volume, stop=False): pass  # Close short
    def cancel_order(self, orderid): pass
    def cancel_all(self): pass
```

**Use Cases:**
- Trend following on single futures contract
- Mean reversion on crypto perpetuals
- Any single-asset directional strategy

---

## 2. Spread Trading Engine (`vnpy_spreadtrading`)

**Purpose:** Multi-leg spread arbitrage and pairs trading

**Version:** 1.3.1

**Key Features:**
- Custom spread definition (multiple legs)
- Real-time spread pricing calculation
- Spread chart visualization
- Algorithmic spread trading
- Statistical arbitrage support

**Core Components:**
```
vnpy_spreadtrading/
├── template.py         # SpreadStrategyTemplate, SpreadAlgoTemplate
├── engine.py           # SpreadEngine
├── backtesting.py      # Spread backtesting
├── algo.py             # Spread execution algorithms
├── base.py             # SpreadData, LegData
└── strategies/         # Built-in spread strategies
```

**Built-in Strategies (2):**
| Strategy | Description |
|----------|-------------|
| `BasicSpreadStrategy` | Manual spread trading with limits |
| `StatisticalArbitrageStrategy` | Stat arb based on spread mean reversion |

**Key Concepts:**
- **Leg:** Individual contract (e.g., RB2401, RB2405)
- **Spread:** Combination of legs (e.g., Long RB2401 - Short RB2405)
- **Spread Price:** Calculated from leg prices using formula
- **Net Position:** Spread position = leg positions combined

**Strategy Template API:**
```python
class SpreadStrategyTemplate:
    # Callbacks
    def on_init(self): pass
    def on_start(self): pass
    def on_stop(self): pass
    def on_tick(self, tick: TickData): pass    # Leg tick update
    def on_bar(self, bar: BarData): pass       # Spread bar update
    def on_trade(self, trade: TradeData): pass
    
    # Action methods
    def buy_spread(self, price, volume): pass   # Long spread
    def sell_spread(self, price, volume): pass  # Short spread
    def set_spread_price(self, price): pass     # Update reference price
```

**Use Cases:**
- Calendar spread arbitrage (same commodity, different months)
- Cross-commodity spread (e.g., Rebar vs Hot Rolled Coil)
- Pairs trading (statistically correlated assets)

---

## 3. Portfolio Strategy Engine (`vnpy_portfoliostrategy`)

**Purpose:** Multi-asset portfolio strategies (Alpha, options arbitrage)

**Version:** 1.2.2

**Key Features:**
- Trade multiple contracts simultaneously
- Portfolio-level backtesting
- Support for Alpha strategies (long-short equity)
- Options arbitrage strategies
- Daily PnL calculation

**Core Components:**
```
vnpy_portfoliostrategy/
├── template.py         # StrategyTemplate
├── engine.py           # StrategyEngine (live + backtest)
├── backtesting.py      # BacktestingEngine
├── base.py             # APP_NAME, utility functions
└── strategies/         # Built-in portfolio strategies
```

**Built-in Strategies (4):**
| Strategy | Description |
|----------|-------------|
| `PairTradingStrategy` | Pairs trading with cointegration |
| `PcpArbitrageStrategy` | Period conversion arbitrage |
| `PortfolioBollChannelStrategy` | Multi-asset Bollinger strategy |
| `TrendFollowingStrategy` | Multi-asset trend following |

**Strategy Template API:**
```python
class StrategyTemplate:
    # Callbacks
    def on_init(self): pass
    def on_start(self): pass
    def on_stop(self): pass
    def on_tick(self, tick: TickData): pass    # Any leg tick
    def on_bar(self, bar: BarData): pass       # Any leg bar
    def on_trade(self, trade: TradeData): pass
    def on_order(self, order: OrderData): pass
    
    # Action methods
    def buy(self, vt_symbol, price, volume): pass
    def sell(self, vt_symbol, price, volume): pass
    def short(self, vt_symbol, price, volume): pass
    def cover(self, vt_symbol, price, volume): pass
```

**Key Difference from CTA:**
- CTA: Single contract, one `on_bar()` per contract
- Portfolio: Multiple contracts, `on_bar()` for any contract in portfolio

**Use Cases:**
- Alpha strategies (long-short equity portfolio)
- Options arbitrage (convertible bond arbitrage)
- Multi-asset trend following
- Statistical arbitrage across multiple assets

---

## 4. Algorithmic Trading Engine (`vnpy_algotrading`)

**Purpose:** Smart order execution algorithms (reduce market impact)

**Version:** 1.1.0

**Key Features:**
- Pre-built execution algorithms
- Algorithm monitoring and control
- Real-time algorithm status tracking
- No backtesting (execution-focused)

**Core Components:**
```
vnpy_algotrading/
├── template.py         # AlgoTemplate
├── engine.py           # AlgoEngine
├── base.py             # AlgoOrder, APP_NAME
└── algos/              # Built-in algorithms
```

**Built-in Algorithms (5):**
| Algorithm | Description |
|-----------|-------------|
| `TwapAlgo` | Time-Weighted Average Price - slice order over time |
| `IcebergAlgo` | Iceberg order - hide true order size |
| `SniperAlgo` | Sniper - execute when price condition met |
| `BestLimitAlgo` | Best Limit - queue at best bid/ask |
| `StopAlgo` | Stop loss - trigger order when price breached |

**Algorithm Template API:**
```python
class AlgoTemplate:
    # Parameters
    vt_symbol: str      # Trading symbol
    direction: Direction  # LONG or SHORT
    offset: Offset      # OPEN or CLOSE
    volume: float       # Total volume to execute
    price: float        # Price limit (if applicable)
    
    # Callbacks
    def on_tick(self, tick: TickData): pass
    def on_order(self, order: OrderData): pass
    def on_trade(self, trade: TradeData): pass
    
    # Actions
    def buy(self, price, volume): pass
    def sell(self, price, volume): pass
    def cancel_all(self): pass
    def write_algo_log(self, msg): pass
```

**Use Cases:**
- Large order execution (minimize market impact)
- Automated stop-loss execution
- Passive market making (queue at best price)
- Stealth trading (iceberg orders)

---

## 5. Script Trading Engine (`vnpy_scripttrader`)

**Purpose:** Ad-hoc trading scripts, multi-asset strategies, REPL trading

**Version:** 1.1.1

**Key Features:**
- No strategy template (free-form scripting)
- Synchronous trading API (blocking calls)
- Multi-account support
- Command-line trading interface
- No backtesting

**Core Components:**
```
vnpy_scripttrader/
├── engine.py           # ScriptEngine
├── cli.py              # init_cli_trading() for REPL
└── ui/                 # GUI manager
```

**Script API:**
```python
# No template - direct API calls
engine = ScriptEngine()

# Get market data
ticks = engine.get_ticks(vt_symbols)
bars = engine.get_bars(vt_symbols, interval, days)

# Get positions/orders
positions = engine.get_positions()
orders = engine.get_orders()

# Trading (blocking - waits for fill)
engine.buy(vt_symbol, price, volume)
engine.sell(vt_symbol, price, volume)
engine.short(vt_symbol, price, volume)
engine.cover(vt_symbol, price, volume)

# Algorithm trading (non-blocking)
engine.send_algo("twap", vt_symbol, direction, volume, price, interval)
```

**Use Cases:**
- One-time rebalancing scripts
- Multi-leg arbitrage (manual execution)
- Portfolio rebalancing
- Interactive/REPL trading
- Custom calculations and analysis

**Example Script:**
```python
from vnpy_scripttrader import init_cli_trading

def run(engine):
    # Rebalance portfolio
    target_positions = {
        "IF2401.CFFEX": 10,
        "IC2401.CFFEX": 5,
        "IM2401.CFFEX": -8
    }
    
    for vt_symbol, target in target_positions.items():
        current = engine.get_position(vt_symbol)
        diff = target - current
        
        if diff > 0:
            engine.buy(vt_symbol, 0, diff)  # Market order
        elif diff < 0:
            engine.sell(vt_symbol, 0, abs(diff))
```

---

## Comparison Matrix

| Feature | CTA | Spread | Portfolio | Algo | Script |
|---------|-----|--------|-----------|------|--------|
| **Assets** | Single | Multi-leg | Multi-asset | Single | Any |
| **Backtesting** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Strategy Template** | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Bar-based** | ✅ | ✅ | ✅ | ❌ | Optional |
| **Tick-based** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Auto Trading** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Execution Algo** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **REPL/CLI** | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## Architecture Pattern

All strategy engines follow the same pattern:

```
┌─────────────────────────────────────────────────────┐
│                  BaseApp                             │
│  (vnpy.trader.app - defines app interface)          │
└─────────────────────────────────────────────────────┘
                          ↑
        ┌─────────────────┴───────────────────────────┐
        │                                             │
┌───────────────────┐                        ┌───────────────────┐
│ CtaStrategyApp    │                        │ SpreadTradingApp  │
│ - CtaEngine       │                        │ - SpreadEngine    │
│ - CtaTemplate     │                        │ - SpreadTemplate  │
│ - Backtesting     │                        │ - Backtesting     │
└───────────────────┘                        └───────────────────┘
```

**Common Structure:**
1. **App Class** - Registers with VeighNa framework
2. **Engine Class** - Manages strategy lifecycle (start/stop/monitor)
3. **Template Class** - Base class for user strategies
4. **Backtesting Class** - Historical simulation (except Algo/Script)
5. **Strategies Folder** - Example implementations

---

## When to Use Which

| Scenario | Recommended Engine |
|----------|-------------------|
| Single futures contract trend following | **CTA** |
| Calendar spread arbitrage | **Spread** |
| Long-short equity portfolio | **Portfolio** |
| Large order execution | **Algo** |
| Custom multi-leg arbitrage | **Script** |
| Crypto perpetual trading | **CTA** |
| Options arbitrage | **Portfolio** |
| Pairs trading (stat arb) | **Spread** or **Portfolio** |
| Stop-loss automation | **Algo** |
| Interactive trading | **Script** |

---

## Files to Study

For each engine, read in this order:

### CTA Strategy
1. `vnpy_ctastrategy/template.py` - Strategy template
2. `vnpy_ctastrategy/engine.py` - Strategy engine
3. `vnpy_ctastrategy/backtesting.py` - Backtesting
4. `vnpy_ctastrategy/strategies/dual_ma_strategy.py` - Simple example

### Spread Trading
1. `vnpy_spreadtrading/template.py` - Spread template
2. `vnpy_spreadtrading/engine.py` - Spread engine
3. `vnpy_spreadtrading/base.py` - SpreadData, LegData
4. `vnpy_spreadtrading/strategies/statistical_arbitrage_strategy.py`

### Portfolio Strategy
1. `vnpy_portfoliostrategy/template.py` - Portfolio template
2. `vnpy_portfoliostrategy/engine.py` - Portfolio engine
3. `vnpy_portfoliostrategy/backtesting.py` - Portfolio backtesting
4. `vnpy_portfoliostrategy/strategies/trend_following_strategy.py`

### Algorithmic Trading
1. `vnpy_algotrading/template.py` - Algo template
2. `vnpy_algotrading/engine.py` - Algo engine
3. `vnpy_algotrading/algos/twap_algo.py` - TWAP example
4. `vnpy_algotrading/algos/sniper_algo.py` - Sniper example

### Script Trading
1. `vnpy_scripttrader/engine.py` - Script engine (main API)
2. `vnpy_scripttrader/cli.py` - CLI trading interface
