# How Strategies Get Bar Data in VeighNa

Complete guide to bar data generation, subscription, and consumption in VeighNa.

---

## Bar Data Sources

Strategies can receive bar data from **3 sources**:

| Source | Live Trading | Backtesting | Use Case |
|--------|--------------|-------------|----------|
| **BarGenerator** (from ticks) | ✅ | ✅ | Real-time 1min bars |
| **BarGenerator** (from 1min bars) | ✅ | ✅ | Multi-timeframe (5min, 15min, 1hr, etc.) |
| **Direct bar subscription** | ✅ | ✅ | When exchange provides bars |
| **Historical loading** | ✅ (init) | ✅ (setup) | Strategy initialization |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Bar Data Flow                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Tick Data (from Gateway)                                        │
│       ↓                                                          │
│  ┌──────────────────┐                                           │
│  │  BarGenerator    │  ← Converts ticks → 1min bars             │
│  │  (on_tick)       │                                           │
│  └────────┬─────────┘                                           │
│           ↓ (on_bar callback)                                    │
│  1min Bar Data                                                   │
│       ↓                                                          │
│  ┌──────────────────┐                                           │
│  │  BarGenerator    │  ← Converts 1min → Xmin/Hour/Daily bars   │
│  │  (on_bar)        │                                           │
│  └────────┬─────────┘                                           │
│           ↓ (on_window_bar callback)                             │
│  Xmin/Hour/Daily Bar Data                                        │
│       ↓                                                          │
│  Strategy.on_bar(bar)                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. BarGenerator Class

**Location:** `vnpy/trader/utility.py`

### Constructor

```python
class BarGenerator:
    """
    For:
    1. generating 1 minute bar data from tick data
    2. generating x minute bar/x hour bar data from 1 minute data
    
    Notice:
    1. for x minute bar, x must be able to divide 60: 2, 3, 5, 6, 10, 15, 20, 30
    2. for x hour bar, x can be any number
    """
    
    def __init__(
        self,
        on_bar: Callable,           # Callback for 1min bars
        window: int = 0,            # Window size for Xmin bars (0 = disabled)
        on_window_bar: Callable | None = None,  # Callback for Xmin bars
        interval: Interval = Interval.MINUTE,   # MINUTE, HOUR, or DAILY
        daily_end: time | None = None           # For daily bars (e.g., 15:00)
    )
```

### Usage Pattern 1: Tick → 1min Bar

```python
from vnpy.trader.utility import BarGenerator
from vnpy.trader.object import TickData, BarData

class MyStrategy:
    def __init__(self):
        # Create BarGenerator for 1min bars
        self.bg = BarGenerator(self.on_bar)
        
    def on_tick(self, tick: TickData):
        """Feed tick data to generator"""
        self.bg.update_tick(tick)
        
    def on_bar(self, bar: BarData):
        """Called when 1min bar completes"""
        # Process 1min bar
        print(f"Bar: {bar.datetime} O:{bar.open} H:{bar.high} L:{bar.low} C:{bar.close}")
```

**How it works:**
```
Tick 1 → bg.update_tick(tick1) → Bar opens
Tick 2 → bg.update_tick(tick2) → Bar updates (high/low/close)
Tick 3 → bg.update_tick(tick3) → Bar updates
...
Tick N → bg.update_tick(tickN) → Bar updates
Minute N+1 → bg.update_tick(tick) → Bar closes, on_bar() called, new bar opens
```

### Usage Pattern 2: 1min Bar → Xmin Bar

```python
class MyStrategy:
    def __init__(self):
        # 15-minute bars from 1min bars
        self.bg = BarGenerator(
            on_bar=self.on_bar,           # 1min callback
            window=15,                    # 15-minute window
            on_window_bar=self.on_15min_bar  # 15min callback
        )
        
    def on_bar(self, bar: BarData):
        """Feed 1min bar to generator"""
        self.bg.update_bar(bar)
        
    def on_15min_bar(self, bar: BarData):
        """Called when 15min bar completes"""
        # Process 15min bar
        print(f"15min Bar: {bar.datetime}")
```

**Supported windows:**
- **Minute bars:** 2, 3, 5, 6, 10, 15, 20, 30 (must divide 60)
- **Hour bars:** Any number (1, 2, 3, 4, 6, 12, etc.)
- **Daily bars:** Use `interval=Interval.DAILY` with `daily_end` time

### Usage Pattern 3: Multi-Timeframe

```python
class MultiTimeframeStrategy:
    def __init__(self):
        # 1min bars from ticks
        self.bg_1min = BarGenerator(self.on_bar)
        
        # 15min bars from 1min
        self.bg_15min = BarGenerator(
            on_bar=self.on_bar,
            window=15,
            on_window_bar=self.on_15min_bar
        )
        
        # 1hr bars from 1min
        self.bg_1hr = BarGenerator(
            on_bar=self.on_bar,
            window=60,
            on_window_bar=self.on_1hr_bar,
            interval=Interval.HOUR
        )
        
    def on_tick(self, tick: TickData):
        self.bg_1min.update_tick(tick)
        
    def on_bar(self, bar: BarData):
        """1min bar"""
        self.bg_15min.update_bar(bar)
        self.bg_1hr.update_bar(bar)
        
    def on_15min_bar(self, bar: BarData):
        """15min bar - medium-term signal"""
        pass
        
    def on_1hr_bar(self, bar: BarData):
        """1hr bar - long-term signal"""
        pass
```

---

## 2. CTA Strategy Template Integration

**Location:** `vnpy_ctastrategy/template.py`

### Built-in BarGenerator

CTA strategies use BarGenerator internally:

```python
class CtaTemplate(ABC):
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        self.cta_engine = cta_engine
        self.bg = BarGenerator(self.on_bar)  # Built-in
        
    def on_tick(self, tick: TickData):
        """Default: feed tick to BarGenerator"""
        self.bg.update_tick(tick)
        
    def on_bar(self, bar: BarData):
        """Override this for your strategy logic"""
        pass
```

### Your Strategy Implementation

```python
from vnpy_ctastrategy import CtaTemplate, BarGenerator, ArrayManager

class DualMaStrategy(CtaTemplate):
    """Dual Moving Average CTA Strategy"""
    
    author = "Your Name"
    
    # Parameters
    fast_window = 10
    slow_window = 30
    
    # Variables
    fast_ma0 = 0.0
    fast_ma1 = 0.0
    slow_ma0 = 0.0
    slow_ma1 = 0.0
    
    parameters = ["fast_window", "slow_window"]
    variables = ["fast_ma0", "fast_ma1", "slow_ma0", "slow_ma1"]
    
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        
        # Additional BarGenerator for multi-timeframe (optional)
        self.bg_15min = BarGenerator(
            on_bar=self.on_bar,
            window=15,
            on_window_bar=self.on_15min_bar
        )
        
        # ArrayManager for indicator calculation
        self.am = ArrayManager(size=100)
        
    def on_init(self):
        """Initialize strategy"""
        self.write_log("Strategy initialized")
        
        # Load historical bars for initialization
        self.load_bar(10)  # Load 10 days of 1min bars
        
    def on_start(self):
        self.write_log("Strategy started")
        
    def on_stop(self):
        self.write_log("Strategy stopped")
        
    def on_tick(self, tick: TickData):
        """Tick data callback"""
        # Default behavior: generate 1min bar
        self.bg.update_tick(tick)
        
    def on_bar(self, bar: BarData):
        """1min bar callback - main strategy logic"""
        # Cancel pending orders
        self.cancel_all()
        
        # Update ArrayManager
        self.am.update_bar(bar)
        
        # Wait until ArrayManager is initialized
        if not self.am.inited:
            return
        
        # Calculate indicators
        fast_ma = self.am.sma(self.fast_window)
        slow_ma = self.am.sma(self.slow_window)
        
        # Generate signals
        if fast_ma > slow_ma and self.pos == 0:
            self.buy(bar.close_price, 1)
        elif fast_ma < slow_ma and self.pos > 0:
            self.sell(bar.close_price, 1)
        
        # Update variables
        self.fast_ma0 = fast_ma
        self.slow_ma0 = slow_ma
        
        # Push event to UI
        self.put_event()
        
    def on_15min_bar(self, bar: BarData):
        """15min bar callback (if using multi-timeframe)"""
        self.write_log(f"15min bar: {bar.datetime}")
        
    def on_trade(self, trade):
        """Trade fill callback"""
        self.write_log(f"Trade: {trade.direction} {trade.volume} @ {trade.price}")
        self.put_event()
        
    def on_order(self, order):
        """Order update callback"""
        self.put_event()
```

---

## 3. Historical Bar Loading

### Live Trading: `load_bar()`

```python
class CtaTemplate:
    def load_bar(
        self,
        days: int,
        interval: Interval = Interval.MINUTE,
        callback: Callable | None = None,
        use_database: bool = False
    ) -> None:
        """
        Load historical bar data for initializing strategy.
        
        Parameters:
            days: Number of days to load
            interval: Bar interval (MINUTE, HOUR, DAILY)
            callback: Callback function (default: self.on_bar)
            use_database: Load from database vs datafeed
        """
        if not callback:
            callback = self.on_bar
            
        bars: list[BarData] = self.cta_engine.load_bar(
            self.vt_symbol,
            days,
            interval,
            callback,
            use_database
        )
        
        # Replay bars through callback
        for bar in bars:
            callback(bar)
```

**Usage:**
```python
def on_init(self):
    # Load 10 days of 1min bars
    self.load_bar(10)
    
    # Load 30 days of daily bars
    self.load_bar(30, interval=Interval.DAILY)
    
    # Load with custom callback
    self.load_bar(10, callback=self.my_custom_bar_handler)
```

### Backtesting: `load_bar_data()`

```python
# vnpy_ctastrategy/backtesting.py

from datetime import datetime
from vnpy.trader.constant import Interval, Exchange
from vnpy.trader.database import get_database

def load_bar_data(
    symbol: str,
    exchange: Exchange,
    interval: Interval,
    start: datetime,
    end: datetime
) -> list[BarData]:
    """Load bar data from database or datafeed"""
    
    database = get_database()
    
    # Load from database
    bars: list[BarData] = database.load_bar_data(
        symbol,
        exchange,
        interval,
        start,
        end
    )
    
    # If database empty, try datafeed
    if not bars:
        from vnpy.trader.datafeed import get_datafeed
        datafeed = get_datafeed()
        bars = datafeed.query_bar_history(...)
    
    return bars
```

---

## 4. Backtesting Engine Bar Flow

**Location:** `vnpy_ctastrategy/backtesting.py`

### Backtesting Setup

```python
from vnpy_ctastrategy import BacktestingEngine
from datetime import datetime
from vnpy.trader.constant import Interval, Exchange

engine = BacktestingEngine()

# Set parameters
engine.set_parameters(
    vt_symbol="RB2401.SHFE",
    interval=Interval.MINUTE,
    start=datetime(2024, 1, 1),
    end=datetime(2024, 12, 31),
    rate=0.0003,          # Transaction fee rate
    slippage=0.2,         # Slippage in ticks
    size=10,              # Contract size
    pricetick=1,          # Price tick
    capital=1_000_000,    # Initial capital
)

# Add strategy
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

### Backtesting Bar Flow

```python
def run_backtesting(self) -> None:
    """Run backtesting"""
    
    # Load historical data
    self.load_data()  # Loads bars into self.history_data
    
    # Iterate through bars
    for bar in self.history_data:
        # Update datetime
        self.datetime = bar.datetime
        
        # Call strategy on_bar
        if self.bar:
            self.callback(self.bar)  # Calls strategy.on_bar()
        
        # Update bar in strategy
        self.bar = bar
```

---

## 5. ArrayManager for Indicator Calculation

**Location:** `vnpy/trader/utility.py`

```python
class ArrayManager:
    """
    For indicator calculation.
    Stores OHLCV arrays for talib indicators.
    """
    
    def __init__(self, size: int = 100):
        self.size = size
        self.count = 0
        self.inited = False
        
        self.open_array = np.zeros(size)
        self.high_array = np.zeros(size)
        self.low_array = np.zeros(size)
        self.close_array = np.zeros(size)
        self.volume_array = np.zeros(size)
        
    def update_bar(self, bar: BarData) -> None:
        """Update bar into array manager"""
        if not self.inited:
            self._check_init()
            
        self.open_array = np.roll(self.open_array, -1)
        self.high_array = np.roll(self.high_array, -1)
        self.low_array = np.roll(self.low_array, -1)
        self.close_array = np.roll(self.close_array, -1)
        self.volume_array = np.roll(self.volume_array, -1)
        
        self.open_array[-1] = bar.open_price
        self.high_array[-1] = bar.high_price
        self.low_array[-1] = bar.low_price
        self.close_array[-1] = bar.close_price
        self.volume_array[-1] = bar.volume
        
    def _check_init(self) -> None:
        self.count += 1
        if self.count >= self.size:
            self.inited = True
            
    # Indicator methods
    def sma(self, n: int, array: bool = False) -> float | np.ndarray:
        """Simple Moving Average"""
        return talib.SMA(self.close_array, timeperiod=n)[-1]
        
    def ema(self, n: int, array: bool = False) -> float | np.ndarray:
        """Exponential Moving Average"""
        return talib.EMA(self.close_array, timeperiod=n)[-1]
        
    def atr(self, n: int, array: bool = False) -> float | np.ndarray:
        """Average True Range"""
        return talib.ATR(self.high_array, self.low_array, self.close_array, timeperiod=n)[-1]
        
    def rsi(self, n: int, array: bool = False) -> float | np.ndarray:
        """RSI"""
        return talib.RSI(self.close_array, timeperiod=n)[-1]
        
    def macd(self, fast: int, slow: int, signal: int, array: bool = False):
        """MACD"""
        return talib.MACD(self.close_array, fastperiod=fast, slowperiod=slow, signalperiod=signal)
        
    # ... 50+ more indicators
```

### Usage in Strategy

```python
class AtrRsiStrategy(CtaTemplate):
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        
        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager(size=100)  # Store 100 bars
        
    def on_bar(self, bar: BarData):
        # Update ArrayManager
        self.am.update_bar(bar)
        
        # Wait until initialized
        if not self.am.inited:
            return
        
        # Calculate indicators
        atr = self.am.atr(14)
        rsi = self.am.rsi(14)
        ma = self.am.sma(20)
        
        # Use indicators in strategy logic
        if rsi < 30 and bar.close_price > ma:
            self.buy(bar.close_price, 1)
```

---

## 6. Portfolio Strategy Bar Data

**Location:** `vnpy_portfoliostrategy/template.py`

For multi-instrument strategies:

```python
class StrategyTemplate:
    def __init__(self, cta_engine, strategy_name, vt_symbols, setting):
        self.vt_symbols = vt_symbols
        
        # BarGenerator per symbol
        self.bgs: dict[str, BarGenerator] = {}
        self.ams: dict[str, ArrayManager] = {}
        
        for vt_symbol in vt_symbols:
            self.bgs[vt_symbol] = BarGenerator(self.on_bar)
            self.ams[vt_symbol] = ArrayManager(size=100)
            
    def on_tick(self, tick: TickData):
        """Tick for ANY symbol"""
        bg = self.bgs.get(tick.vt_symbol)
        if bg:
            bg.update_tick(tick)
            
    def on_bar(self, bar: BarData):
        """Bar for ANY symbol"""
        # Update ArrayManager for this symbol
        am = self.ams.get(bar.vt_symbol)
        if am:
            am.update_bar(bar)
            
        # Strategy logic across all symbols
        # ...
```

---

## Summary

| Component | Purpose | Location |
|-----------|---------|----------|
| **BarGenerator** | Tick → Bar, 1min → Xmin | `vnpy/trader/utility.py` |
| **ArrayManager** | Indicator calculation | `vnpy/trader/utility.py` |
| **CtaTemplate** | Strategy base class | `vnpy_ctastrategy/template.py` |
| **BacktestingEngine** | Historical replay | `vnpy_ctastrategy/backtesting.py` |

**Bar Data Flow:**
```
Exchange → Gateway → Event Engine → Strategy
                              ↓
                         BarGenerator
                              ↓
                         on_bar(bar)
                              ↓
                         ArrayManager
                              ↓
                         Indicators (SMA, RSI, MACD...)
```

**For your NIFTY500 multi-timeframe strategy:**
```python
class Nifty500Strategy(StrategyTemplate):
    def __init__(self, ...):
        for vt_symbol in vt_symbols:
            # 1min from ticks
            self.bgs[vt_symbol] = BarGenerator(self.on_bar)
            
            # 15min from 1min
            self.bg_15min[vt_symbol] = BarGenerator(
                on_bar=self.on_bar,
                window=15,
                on_window_bar=self.on_15min_bar
            )
            
            # 1hr from 1min
            self.bg_1hr[vt_symbol] = BarGenerator(
                on_bar=self.on_bar,
                window=60,
                on_window_bar=self.on_1hr_bar,
                interval=Interval.HOUR
            )
```
