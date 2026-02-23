# Indian Market Backtesting Guide (Bar Data Only)

For Indian markets where **historical tick data is NOT available** (only 1-minute bars), VeighNa **fully supports bar-based backtesting**.

---

## Good News: VeighNa Supports Bar Backtesting Natively!

```python
# vnpy_ctastrategy/backtesting.py

def new_bar(self, bar: BarData) -> None:
    """Process bar data directly - NO tick conversion needed!"""
    self.bar = bar
    self.datetime = bar.datetime
    
    self.cross_limit_order()
    self.cross_stop_order()
    self.strategy.on_bar(bar)  # ← Direct bar callback
    
    self.update_daily_close(bar.close_price)
```

**Backtesting Mode:**
```python
engine.set_parameters(
    mode=BacktestingMode.BAR,  # ← Bar-based backtesting
    ...
)
```

---

## Complete Workflow for Indian Markets

### Step 1: Data Collection (Live)

```python
# Record 1-minute bars during live market hours (9:15 AM - 3:30 PM IST)

from vnpy.trader.object import BarData
from vnpy.trader.constant import Interval, Exchange
from vnpy.trader.database import get_database

# During live trading, save bars to database
def save_bars_to_database(bars: list[BarData]):
    database = get_database()
    database.save_bar_data(bars)

# Example: NIFTY500 stock bar
bar = BarData(
    symbol="RELIANCE",
    exchange=Exchange.NSE,
    datetime=datetime(2024, 1, 15, 9, 15),  # 9:15 AM
    interval=Interval.MINUTE,
    open_price=2450.00,
    high_price=2455.50,
    low_price=2448.00,
    close_price=2453.25,
    volume=125000,
    turnover=306875000.00,
    open_interest=0,  # For stocks
    gateway_name="NSE"
)

save_bars_to_database([bar])
```

### Step 2: Backtesting Setup

```python
from vnpy_ctastrategy import BacktestingEngine
from datetime import datetime
from vnpy.trader.constant import Interval, Exchange

engine = BacktestingEngine()

# Set parameters for Indian market
engine.set_parameters(
    vt_symbol="RELIANCE.NSE",
    interval=Interval.MINUTE,      # 1-minute bars
    start=datetime(2024, 1, 1),
    end=datetime(2024, 12, 31),
    rate=0.0003,                   # 0.03% brokerage + STT + charges
    slippage=0.05,                 # 5 paise slippage
    size=1,                        # 1 lot (or 1 for stocks)
    pricetick=0.05,                # NSE tick size
    capital=10_000_000,            # 1 crore INR
    mode=BacktestingMode.BAR,      # ← Bar-based mode
)

# Add your strategy
from strategies.dual_ma_strategy import DualMaStrategy

engine.add_strategy(DualMaStrategy, {
    "fast_window": 10,
    "slow_window": 30
})

# Run backtest
engine.run_backtesting()

# Calculate results
df = engine.calculate_result()
stats = engine.calculate_statistics()

# Show chart
engine.show_chart()
```

---

## Bar-Based Backtesting Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              Bar-Based Backtesting Flow                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Load bars from database                                      │
│     ┌──────────────────────────────────────────────────────┐    │
│     │ database.load_bar_data(symbol, exchange,             │    │
│     │                    interval, start, end)             │    │
│     │ → Returns: list[BarData]                             │    │
│     └──────────────────────────────────────────────────────┘    │
│                          ↓                                       │
│  2. Store in history_data                                        │
│     ┌──────────────────────────────────────────────────────┐    │
│     │ self.history_data = [bar1, bar2, bar3, ...]          │    │
│     └──────────────────────────────────────────────────────┘    │
│                          ↓                                       │
│  3. Replay bars sequentially                                     │
│     ┌──────────────────────────────────────────────────────┐    │
│     │ for bar in self.history_data:                        │    │
│     │     self.new_bar(bar)                                │    │
│     │         → strategy.on_bar(bar)                       │    │
│     └──────────────────────────────────────────────────────┘    │
│                          ↓                                       │
│  4. Strategy processes bar                                       │
│     ┌──────────────────────────────────────────────────────┐    │
│     │ def on_bar(self, bar: BarData):                      │    │
│     │     self.am.update_bar(bar)  # Update indicators     │    │
│     │     if self.am.inited:                               │    │
│     │         fast_ma = self.am.sma(10)                    │    │
│     │         slow_ma = self.am.sma(30)                    │    │
│     │         if fast_ma > slow_ma:                        │    │
│     │             self.buy(bar.close_price, 1)             │    │
│     └──────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## No BarGenerator Needed in Backtesting!

**Important:** In bar-based backtesting:

| Component | Live Trading | Backtesting |
|-----------|--------------|-------------|
| **BarGenerator** | ✅ Required (tick → bar) | ❌ NOT needed |
| **on_bar()** | ✅ Called by BarGenerator | ✅ Called by BacktestingEngine |
| **ArrayManager** | ✅ For indicators | ✅ For indicators |

**Your strategy stays the same:**

```python
from vnpy_ctastrategy import CtaTemplate, BarGenerator, ArrayManager

class DualMaStrategy(CtaTemplate):
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        
        # BarGenerator - used in LIVE trading
        self.bg = BarGenerator(self.on_bar)
        
        # ArrayManager - used in BOTH live and backtesting
        self.am = ArrayManager(size=100)
        
    def on_tick(self, tick):
        """Called in live trading - feed to BarGenerator"""
        self.bg.update_tick(tick)
        
    def on_bar(self, bar):
        """Called in BOTH live and backtesting"""
        # Update ArrayManager
        self.am.update_bar(bar)
        
        if not self.am.inited:
            return
        
        # Calculate indicators
        fast_ma = self.am.sma(10)
        slow_ma = self.am.sma(30)
        
        # Generate signals
        if fast_ma > slow_ma and self.pos == 0:
            self.buy(bar.close_price, 1)
        elif fast_ma < slow_ma and self.pos > 0:
            self.sell(bar.close_price, 1)
```

**In backtesting:**
- `on_tick()` is **never called** (no ticks)
- `on_bar()` is called **directly by BacktestingEngine**
- `BarGenerator` sits idle (not used)

---

## Multi-Timeframe Backtesting (1min → 15min, 1hr)

For your NIFTY500 multi-timeframe strategy:

```python
from vnpy_ctastrategy import CtaTemplate, BarGenerator, ArrayManager

class MultiTimeframeStrategy(CtaTemplate):
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        
        # BarGenerators for multiple timeframes
        self.bg_1min = BarGenerator(self.on_bar)
        self.bg_15min = BarGenerator(
            on_bar=self.on_bar,
            window=15,
            on_window_bar=self.on_15min_bar
        )
        self.bg_1hr = BarGenerator(
            on_bar=self.on_bar,
            window=60,
            on_window_bar=self.on_1hr_bar,
            interval=Interval.HOUR
        )
        
        # ArrayManagers for each timeframe
        self.am_1min = ArrayManager(size=100)
        self.am_15min = ArrayManager(size=100)
        self.am_1hr = ArrayManager(size=100)
        
    def on_tick(self, tick):
        """Live trading only"""
        self.bg_1min.update_tick(tick)
        
    def on_bar(self, bar):
        """1min bar - BOTH live and backtesting"""
        # Update 1min ArrayManager
        self.am_1min.update_bar(bar)
        
        # Feed to higher timeframe generators
        self.bg_15min.update_bar(bar)
        self.bg_1hr.update_bar(bar)
        
        # Process 1min signals
        if self.am_1min.inited:
            rsi_1min = self.am_1min.rsi(14)
            # ... 1min strategy logic
            
    def on_15min_bar(self, bar):
        """15min bar - BOTH live and backtesting"""
        self.am_15min.update_bar(bar)
        
        if self.am_15min.inited:
            ma_15min = self.am_15min.sma(20)
            # ... 15min strategy logic
            
    def on_1hr_bar(self, bar):
        """1hr bar - BOTH live and backtesting"""
        self.am_1hr.update_bar(bar)
        
        if self.am_1hr.inited:
            trend_1hr = self.am_1hr.macd(12, 26, 9)
            # ... 1hr strategy logic
```

**How it works in backtesting:**

```
BacktestingEngine loads 1min bars
    ↓
For each 1min bar:
    engine.new_bar(bar)
        ↓
    strategy.on_bar(bar)  ← 1min callback
        ↓
    bg_15min.update_bar(bar)  ← BarGenerator accumulates
        ↓
    (After 15 bars) → on_15min_bar() ← 15min callback
        ↓
    bg_1hr.update_bar(bar)  ← BarGenerator accumulates
        ↓
    (After 60 bars) → on_1hr_bar() ← 1hr callback
```

**BarGenerator works in backtesting too!** It synthesizes higher timeframes from 1min bars.

---

## Data Import for Indian Markets

### Option 1: Import from CSV

```python
import pandas as pd
from vnpy.trader.object import BarData
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.database import get_database
from datetime import datetime

def import_nse_bars_from_csv(csv_file: str, symbol: str):
    """Import NSE 1-minute bar data from CSV"""
    
    # Read CSV (assumes columns: datetime, open, high, low, close, volume)
    df = pd.read_csv(csv_file)
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    bars = []
    for _, row in df.iterrows():
        bar = BarData(
            symbol=symbol,
            exchange=Exchange.NSE,
            datetime=row['datetime'],
            interval=Interval.MINUTE,
            open_price=row['open'],
            high_price=row['high'],
            low_price=row['low'],
            close_price=row['close'],
            volume=row['volume'],
            gateway_name="NSE"
        )
        bars.append(bar)
    
    # Save to database
    database = get_database()
    database.save_bar_data(bars)
    
    print(f"Imported {len(bars)} bars for {symbol}")

# Usage
import_nse_bars_from_csv("RELIANCE_2024_1min.csv", "RELIANCE")
```

### Option 2: Import from Data Provider

```python
# Example: Using historical 1min data from TrueData, GlobalDataFeeder, etc.

from TrueData import TrueDataAPI  # Example provider

def fetch_and_save_nse_data(symbol: str, start_date, end_date):
    """Fetch 1min bars from data provider and save to database"""
    
    api = TrueDataAPI()
    bars = api.get_historical_data(
        symbol=symbol,
        exchange="NSE",
        interval="1min",
        start=start_date,
        end=end_date
    )
    
    # Convert to VeighNa BarData format
    vnpy_bars = []
    for bar in bars:
        vnpy_bar = BarData(
            symbol=symbol,
            exchange=Exchange.NSE,
            datetime=bar['datetime'],
            interval=Interval.MINUTE,
            open_price=bar['open'],
            high_price=bar['high'],
            low_price=bar['low'],
            close_price=bar['close'],
            volume=bar['volume'],
            gateway_name="NSE"
        )
        vnpy_bars.append(vnpy_bar)
    
    # Save to database
    database = get_database()
    database.save_bar_data(vnpy_bars)
```

### Option 3: Record Live Data

```python
# During live market hours, record bars to database

from vnpy.trader.event import EVENT_BAR
from vnpy.event import Event

class BarRecorder:
    def __init__(self, main_engine):
        self.main_engine = main_engine
        self.database = get_database()
        
        # Register bar event handler
        main_engine.event_engine.register(
            "eBar.",  # If bar events exist
            self.on_bar_event
        )
    
    def on_bar_event(self, event: Event):
        bar: BarData = event.data
        self.database.save_bar_data([bar])
```

**Note:** Since VeighNa doesn't have `EVENT_BAR`, you'd need to:
1. Create custom bar events in your gateway
2. Or record ticks and aggregate later (if you have tick data)

---

## Backtesting Example: NIFTY500 Strategy

```python
# backtest_nifty500.py

from vnpy_portfoliostrategy import BacktestingEngine
from datetime import datetime
from vnpy.trader.constant import Interval

# NIFTY500 stock list
nifty500_stocks = [
    "RELIANCE.NSE",
    "TCS.NSE",
    "INFY.NSE",
    "HDFCBANK.NSE",
    "ICICIBANK.NSE",
    # ... 495 more stocks
]

engine = BacktestingEngine()

engine.set_parameters(
    vt_symbols=nifty500_stocks,
    interval=Interval.MINUTE,
    start=datetime(2024, 1, 1),
    end=datetime(2024, 12, 31),
    rate=0.0003,          # Brokerage + charges
    slippage=0.05,        # 5 paise
    size=1,               # 1 share for stocks
    pricetick=0.05,       # NSE tick size
    capital=100_000_000,  # 10 crore INR
)

from strategies.nifty500_breakout import Nifty500BreakoutStrategy

engine.add_strategy(Nifty500BreakoutStrategy, {
    "breakout_period": 20,
    "max_positions": 50,
})

engine.run_backtesting()
df = engine.calculate_result()
stats = engine.calculate_statistics()

print(stats)
engine.show_chart()
```

---

## Performance Considerations

### Memory Usage

Loading 1min bars for 500 stocks × 252 trading days × 375 bars/day:
```
500 × 252 × 375 = 47,250,000 bars
```

**Solution:** Use batch loading and database optimization

```python
# Use SQLite for small datasets, PostgreSQL/MySQL for large
# vnpy/trader/setting.py
DATABASE = {
    "database_name": "mysql",  # or "postgresql"
    "database_host": "localhost",
    "database_port": 3306,
    "database_user": "vnpy",
    "database_password": "vnpy",
    "database_name": "vnpy_db"
}
```

### Backtesting Speed

```python
# Optimize backtesting
engine.set_parameters(
    ...
    mode=BacktestingMode.BAR,  # Faster than tick mode
)

# Use multiprocessing for parameter optimization
from vnpy.trader.optimize import OptimizationSetting

setting = OptimizationSetting()
setting.set_target("sharpe_ratio")
setting.add_parameter("fast_window", 5, 20, 5)
setting.add_parameter("slow_window", 20, 100, 10)

# Run parallel optimization
results = engine.run_ga_optimization(setting)
# or
results = engine.run_bf_optimization(setting)
```

---

## Summary

| Requirement | Solution |
|-------------|----------|
| **Historical 1min bars** | Load from database via `load_bar_data()` |
| **Bar-based backtesting** | `mode=BacktestingMode.BAR` |
| **Multi-timeframe** | BarGenerator works in backtesting too |
| **Data import** | CSV import → database |
| **Live recording** | Record bars during live trading |
| **Strategy code** | Same for live and backtesting |

**Key Points:**

1. ✅ **VeighNa fully supports bar-based backtesting**
2. ✅ **No tick data required**
3. ✅ **BarGenerator works in both live and backtesting**
4. ✅ **Same strategy code for both modes**
5. ✅ **Multi-timeframe supported via BarGenerator**

**For Indian markets:**
```python
# 1. Import 1min bars from CSV/data provider
import_nse_bars_from_csv("NIFTY500_2024.csv", "RELIANCE")

# 2. Backtest with bar mode
engine.set_parameters(mode=BacktestingMode.BAR)

# 3. Run backtest
engine.run_backtesting()

# 4. Same strategy works in live trading
# (just switch to live CtaEngine)
```
