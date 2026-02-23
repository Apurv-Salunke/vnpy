# Execution Algorithms in VeighNa (VWAP, TWAP, Custom)

Complete guide to implementing and using execution algorithms like VWAP, TWAP, and custom logic.

---

## Where Execution Algorithms Fit

```
┌─────────────────────────────────────────────────────────────────┐
│              VeighNa Architecture with Execution Algos           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Strategy Layer                                           │   │
│  │  - CtaStrategy (single-asset)                            │   │
│  │  - PortfolioStrategy (multi-asset)                       │   │
│  │  - ScriptTrader (custom scripts)                         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                          ↓                                       │
│         Decision: "Buy 10,000 shares of RELIANCE"               │
│                          ↓                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Execution Layer  ← YOU ARE HERE                          │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │  AlgoEngine (vnpy_algotrading)                     │  │   │
│  │  │  - TWAP: Time-Weighted Average Price              │  │   │
│  │  │  - VWAP: Volume-Weighted Average Price (custom)   │  │   │
│  │  │  - Iceberg: Hide true order size                  │  │   │
│  │  │  - Sniper: Execute at specific price              │  │   │
│  │  │  - BestLimit: Queue at best bid/ask               │  │   │
│  │  │  - Stop: Auto stop-loss                           │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                          ↓                                       │
│         Child Orders: "Buy 100 @ 2450", "Buy 100 @ 2451"...     │
│                          ↓                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  OMS Layer                                                │   │
│  │  - Order tracking, position management                   │   │
│  │  - OffsetConverter (for futures)                         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                          ↓                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Gateway Layer                                            │   │
│  │  - CTP, IB, Binance, etc.                                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## AlgoEngine: Execution Engine

**Location:** `vnpy_algotrading/vnpy_algotrading/engine.py`

### Architecture

```python
class AlgoEngine(BaseEngine):
    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        super().__init__(main_engine, event_engine, APP_NAME)
        
        # Algorithm templates (classes)
        self.algo_templates: dict[str, type[AlgoTemplate]] = {}
        
        # Running algorithm instances
        self.algos: dict[str, AlgoTemplate] = {}
        
        # Symbol → Algorithm mapping
        self.symbol_algo_map: dict[str, set[AlgoTemplate]] = defaultdict(set)
        
        # OrderID → Algorithm mapping
        self.orderid_algo_map: dict[str, AlgoTemplate] = {}
```

### Event Registration

```python
def register_event(self) -> None:
    """Register event handlers"""
    self.event_engine.register(EVENT_TICK, self.process_tick_event)
    self.event_engine.register(EVENT_TIMER, self.process_timer_event)
    self.event_engine.register(EVENT_ORDER, self.process_order_event)
    self.event_engine.register(EVENT_TRADE, self.process_trade_event)
```

**Event Flow:**
```
Tick Event → Update all algos for that symbol
Timer Event (1Hz) → Update all running algos
Order Event → Update specific algo
Trade Event → Update specific algo
```

---

## AlgoTemplate: Base Class for All Algorithms

**Location:** `vnpy_algotrading/vnpy_algotrading/template.py`

### Structure

```python
class AlgoTemplate:
    _count: int = 0                 # Instance counter
    
    display_name: str = ""          # Display name in UI
    default_setting: dict = {}      # Default parameters
    variables: list = []            # Variables to track
    
    def __init__(
        self,
        algo_engine: "AlgoEngine",
        algo_name: str,
        vt_symbol: str,
        direction: Direction,
        offset: Offset,
        price: float,
        volume: float,
        setting: dict
    ):
        self.algo_engine = algo_engine
        self.algo_name = algo_name
        
        # Parent order parameters
        self.vt_symbol = vt_symbol
        self.direction = direction
        self.offset = offset
        self.price = price          # Limit price (or None for market)
        self.volume = volume        # Total volume to execute
        
        # Algorithm state
        self.status = AlgoStatus.PAUSED
        self.traded = 0             # Executed volume
        self.traded_price = 0       # Average executed price
        
        # Child orders
        self.active_orders: dict[str, OrderData] = {}
    
    # Callbacks (override in subclass)
    def on_tick(self, tick: TickData): pass
    def on_order(self, order: OrderData): pass
    def on_trade(self, trade: TradeData): pass
    def on_timer(self): pass
    
    # Action methods
    def buy(price, volume, offset): → vt_orderid
    def sell(price, volume, offset): → vt_orderid
    def cancel_order(vt_orderid)
    def cancel_all()
    
    # Query methods
    def get_tick() → TickData
    def get_contract() → ContractData
```

### Algorithm Lifecycle

```
Created → PAUSED → start() → RUNNING → stop() → STOPPED
                              ↓
                         finish() → FINISHED
                              ↓
                         pause() → PAUSED → resume() → RUNNING
```

---

## Built-in TWAP Algorithm

**Location:** `vnpy_algotrading/vnpy_algotrading/algos/twap_algo.py`

### TWAP Logic

```python
class TwapAlgo(AlgoTemplate):
    display_name: str = "TWAP 时间加权平均"
    
    default_setting: dict = {
        "time": 600,        # Total execution time (seconds)
        "interval": 60      # Order interval (seconds)
    }
    
    variables: list = [
        "order_volume",     # Volume per slice
        "timer_count",      # Timer counter
        "total_count"       # Total elapsed time
    ]
    
    def __init__(self, ...):
        super().__init__(...)
        
        # Calculate slice volume
        self.order_volume = self.volume / (self.time / self.interval)
        
        # Round to contract min_volume
        contract = self.get_contract()
        if contract:
            self.order_volume = round_to(self.order_volume, contract.min_volume)
        
        self.timer_count = 0
        self.total_count = 0
    
    def on_trade(self, trade: TradeData) -> None:
        """Update traded volume"""
        if self.traded >= self.volume:
            self.finish()  # Done
    
    def on_timer(self) -> None:
        """Called every second"""
        self.timer_count += 1
        self.total_count += 1
        
        # Check if time expired
        if self.total_count >= self.time:
            self.finish()
            return
        
        # Wait for interval
        if self.timer_count < self.interval:
            return
        
        self.timer_count = 0
        
        # Cancel pending orders
        self.cancel_all()
        
        # Calculate remaining volume
        left_volume = self.volume - self.traded
        order_volume = min(self.order_volume, left_volume)
        
        # Send order
        tick = self.get_tick()
        if not tick:
            return
        
        if self.direction == Direction.LONG:
            if tick.ask_price_1 <= self.price:  # Price check
                self.buy(self.price, order_volume)
        else:
            if tick.bid_price_1 >= self.price:
                self.sell(self.price, order_volume)
```

### TWAP Execution Flow

```
Start: Buy 1000 @ 2450, time=600s, interval=60s
       → order_volume = 1000 / (600/60) = 100 per slice

t=0s:    Start algorithm
t=60s:   Send Buy 100 @ 2450
t=65s:   Trade: Bought 100 @ 2449
t=120s:  Send Buy 100 @ 2450
t=125s:  Trade: Bought 80 @ 2450 (partial)
t=180s:  Send Buy 20 @ 2450 (remaining from previous) + 80 new
...
t=600s:  Time expired → Finish
```

---

## Creating Custom VWAP Algorithm

VWAP (Volume-Weighted Average Price) is **NOT included** in standard VeighNa but can be easily created:

```python
# algos/vwap_algo.py
from vnpy.trader.object import TradeData, TickData, BarData
from vnpy.trader.constant import Direction
from vnpy.trader.utility import round_to

from ..template import AlgoTemplate


class VwapAlgo(AlgoTemplate):
    """VWAP Algorithm - Execute based on historical volume profile"""
    
    display_name: str = "VWAP 成交量加权平均"
    
    default_setting: dict = {
        "volume_profile": [],    # List of volume percentages per interval
        "interval": 60,          # Interval in seconds
        "max_order_size": 100,   # Maximum order size
        "price_limit": 0.02      # Price deviation limit (2%)
    }
    
    variables: list = [
        "current_interval",
        "target_volume",
        "total_volume_profile"
    ]
    
    def __init__(
        self,
        algo_engine,
        algo_name,
        vt_symbol,
        direction,
        offset,
        price,
        volume,
        setting
    ):
        super().__init__(
            algo_engine, algo_name, vt_symbol,
            direction, offset, price, volume, setting
        )
        
        # Parameters
        self.volume_profile = setting.get("volume_profile", [])
        self.interval = setting["interval"]
        self.max_order_size = setting["max_order_size"]
        self.price_limit = setting["price_limit"]
        
        # Calculate total profile weight
        self.total_volume_profile = sum(self.volume_profile)
        
        # Variables
        self.current_interval = 0
        self.target_volume = 0
        
        # Historical volume tracking (for real-time VWAP calculation)
        self.bar_volume = 0
        self.bar_vwap = 0
        
        self.put_event()
    
    def on_start(self) -> None:
        """Algorithm started"""
        # Subscribe to market data
        self.write_log(f"VWAP算法启动，目标数量：{self.volume}")
    
    def on_tick(self, tick: TickData) -> None:
        """Tick update"""
        # Check price limit
        if self.direction == Direction.LONG:
            max_price = self.price * (1 + self.price_limit)
            if tick.ask_price_1 > max_price:
                return  # Price too high, wait
        else:
            min_price = self.price * (1 - self.price_limit)
            if tick.bid_price_1 < min_price:
                return  # Price too low, wait
        
        # Execute if within price limit
        self.check_and_send_order(tick)
    
    def on_timer(self) -> None:
        """Called every second"""
        self.current_interval += 1
        
        # Calculate target volume for current interval based on profile
        if self.volume_profile:
            profile_index = min(
                self.current_interval - 1,
                len(self.volume_profile) - 1
            )
            profile_weight = self.volume_profile[profile_index] / self.total_volume_profile
            self.target_volume = self.volume * profile_weight
        
        # Check if we should trade this interval
        if self.current_interval % self.interval == 0:
            tick = self.get_tick()
            if tick:
                self.check_and_send_order(tick)
    
    def check_and_send_order(self, tick: TickData) -> None:
        """Check conditions and send order"""
        # Cancel pending orders
        self.cancel_all()
        
        # Calculate remaining volume
        remaining = self.volume - self.traded
        if remaining <= 0:
            self.finish()
            return
        
        # Calculate order volume based on VWAP profile
        if self.target_volume > 0:
            order_volume = min(
                self.target_volume - self.traded,
                remaining,
                self.max_order_size
            )
        else:
            # Default: equal distribution
            order_volume = min(remaining / 10, self.max_order_size)
        
        if order_volume <= 0:
            return
        
        # Round to contract size
        contract = self.get_contract()
        if contract:
            order_volume = round_to(order_volume, contract.min_volume)
        
        # Send order
        if self.direction == Direction.LONG:
            self.buy(tick.ask_price_1, order_volume)
        else:
            self.sell(tick.bid_price_1, order_volume)
    
    def on_trade(self, trade: TradeData) -> None:
        """Trade fill callback"""
        self.write_log(f"成交：{trade.direction} {trade.volume} @ {trade.price}")
        
        if self.traded >= self.volume:
            self.finish()
            self.write_log(f"VWAP算法完成，总成交：{self.traded}, 均价：{self.traded_price:.2f}")
    
    def on_order(self, order: OrderData) -> None:
        """Order update callback"""
        # Track active orders
        pass
    
    def finish(self) -> None:
        """Algorithm finished"""
        self.cancel_all()
        super().finish()
```

### Usage Example

```python
from vnpy_algotrading import AlgoEngine
from vnpy.trader.constant import Direction, Offset

# Start VWAP algorithm
algo_engine.start_algo(
    template_name="VwapAlgo",
    vt_symbol="RELIANCE.NSE",
    direction=Direction.LONG,
    offset=Offset.OPEN,
    price=2450.00,           # Reference price
    volume=10000,            # Total quantity
    setting={
        "volume_profile": [5, 8, 10, 12, 15, 15, 12, 10, 8, 5],  # Volume distribution
        "interval": 60,       # 60 seconds per interval
        "max_order_size": 500,  # Max 500 per order
        "price_limit": 0.02   # 2% price deviation limit
    }
)
```

---

## Custom Execution Logic Examples

### 1. Implementation Shortfall

```python
class ImplementationShortfallAlgo(AlgoTemplate):
    """
    Implementation Shortfall Algorithm
    
    Minimizes the difference between:
    - Decision price (when signal generated)
    - Actual execution price
    """
    
    display_name: str = "Implementation Shortfall"
    
    default_setting: dict = {
        "decision_price": 0,      # Price when decision made
        "urgency": 0.5,           # 0=patient, 1=urgent
        "max_participation": 0.1  # Max 10% of market volume
    }
    
    def __init__(self, ...):
        super().__init__(...)
        
        self.decision_price = setting["decision_price"]
        self.urgency = setting["urgency"]
        self.max_participation = setting["max_participation"]
        
        # Calculate target based on urgency
        self.aggressiveness = 1 - self.urgency
    
    def on_tick(self, tick: TickData) -> None:
        """Execute based on price movement from decision"""
        
        # Calculate slippage
        if self.direction == Direction.LONG:
            price_diff = tick.ask_price_1 - self.decision_price
            slippage_pct = price_diff / self.decision_price
        else:
            price_diff = self.decision_price - tick.bid_price_1
            slippage_pct = price_diff / self.decision_price
        
        # More urgent = more aggressive pricing
        if slippage_pct > 0:  # Price moved against us
            # Aggressive: use marketable limit
            if self.direction == Direction.LONG:
                exec_price = tick.ask_price_1 + tick.pricetick
            else:
                exec_price = tick.bid_price_1 - tick.pricetick
        else:
            # Patient: use limit at mid
            exec_price = (tick.bid_price_1 + tick.ask_price_1) / 2
        
        # Calculate participation rate
        market_volume = tick.volume  # Current bar volume
        max_order = market_volume * self.max_participation
        
        # Send order
        remaining = self.volume - self.traded
        order_volume = min(remaining, max_order)
        
        if order_volume > 0:
            if self.direction == Direction.LONG:
                self.buy(exec_price, order_volume)
            else:
                self.sell(exec_price, order_volume)
```

### 2. Adaptive TWAP (Market-Responsive)

```python
class AdaptiveTwapAlgo(AlgoTemplate):
    """
    Adaptive TWAP - Adjusts execution based on market conditions
    
    - Speeds up when volume is high
    - Slows down when volume is low
    - Pauses during adverse price movement
    """
    
    display_name: str = "Adaptive TWAP"
    
    default_setting: dict = {
        "base_interval": 60,
        "volume_threshold": 2.0,   # 2x average volume
        "price_impact_limit": 0.01  # 1% adverse move
    }
    
    def __init__(self, ...):
        super().__init__(...)
        
        self.base_interval = setting["base_interval"]
        self.volume_threshold = setting["volume_threshold"]
        self.price_impact_limit = setting["price_impact_limit"]
        
        self.dynamic_interval = self.base_interval
        self.reference_price = 0
        self.avg_volume = 0
    
    def on_timer(self) -> None:
        """Adjust interval based on market conditions"""
        
        tick = self.get_tick()
        if not tick:
            return
        
        # Update reference price
        if self.reference_price == 0:
            self.reference_price = tick.last_price
        
        # Calculate volume ratio
        volume_ratio = tick.volume / self.avg_volume if self.avg_volume > 0 else 1
        
        # Adjust interval
        if volume_ratio > self.volume_threshold:
            # High volume: execute faster
            self.dynamic_interval = self.base_interval * 0.5
        elif volume_ratio < 0.5:
            # Low volume: execute slower
            self.dynamic_interval = self.base_interval * 2
        
        # Check price impact
        if self.direction == Direction.LONG:
            adverse_move = (tick.last_price - self.reference_price) / self.reference_price
        else:
            adverse_move = (self.reference_price - tick.last_price) / self.reference_price
        
        if adverse_move > self.price_impact_limit:
            # Pause execution during adverse move
            self.write_log(f"价格不利变动 {adverse_move:.2%}, 暂停执行")
            return
        
        # Execute
        self.send_slice_order(tick)
```

### 3. POV (Percentage of Volume)

```python
class PovAlgo(AlgoTemplate):
    """
    POV - Percentage of Volume
    
    Execute X% of market volume
    """
    
    display_name: str = "POV 成交量占比"
    
    default_setting: dict = {
        "participation_rate": 0.1,  # 10% of market volume
        "max_order_size": 1000,
        "min_order_interval": 5     # Minimum seconds between orders
    }
    
    variables: list = [
        "market_volume",
        "our_volume",
        "actual_participation"
    ]
    
    def __init__(self, ...):
        super().__init__(...)
        
        self.participation_rate = setting["participation_rate"]
        self.max_order_size = setting["max_order_size"]
        self.min_order_interval = setting["min_order_interval"]
        
        self.market_volume = 0
        self.last_order_time = 0
    
    def on_trade(self, trade: TradeData) -> None:
        """Track our executed volume"""
        self.our_volume += trade.volume
        self.actual_participation = self.our_volume / self.market_volume if self.market_volume > 0 else 0
    
    def on_timer(self) -> None:
        """Check if we should participate"""
        import time
        current_time = time.time()
        
        if current_time - self.last_order_time < self.min_order_interval:
            return
        
        tick = self.get_tick()
        if not tick:
            return
        
        # Update market volume
        self.market_volume = tick.volume
        
        # Calculate target volume
        target_our_volume = self.market_volume * self.participation_rate
        additional_needed = target_our_volume - self.our_volume
        
        if additional_needed <= 0:
            return
        
        # Send order
        order_volume = min(additional_needed, self.max_order_size)
        
        if self.direction == Direction.LONG:
            self.buy(tick.ask_price_1, order_volume)
        else:
            self.sell(tick.bid_price_1, order_volume)
        
        self.last_order_time = current_time
```

---

## Integration with Strategy Layer

### Option 1: Direct Algo Start from Strategy

```python
from vnpy_ctastrategy import CtaTemplate

class MyCtaStrategy(CtaTemplate):
    def on_bar(self, bar: BarData):
        # Generate signal
        if self.buy_signal:
            # Instead of direct buy, use algo execution
            algo_engine = self.cta_engine.main_engine.get_engine("algo")
            
            algo_engine.start_algo(
                template_name="TwapAlgo",
                vt_symbol=self.vt_symbol,
                direction=Direction.LONG,
                offset=Offset.OPEN,
                price=bar.close_price,
                volume=1000,  # Large order
                setting={
                    "time": 1800,    # 30 minutes
                    "interval": 60   # 1 minute slices
                }
            )
```

### Option 2: Strategy Sends to AlgoEngine

```python
# In CtaEngine or PortfolioStrategy Engine
def send_order(
    self,
    strategy,
    direction,
    offset,
    price,
    volume,
    stop,
    lock,
    net
):
    """Override to use algo execution for large orders"""
    
    # Check if volume exceeds threshold
    if volume > self.large_order_threshold:
        # Use TWAP for large orders
        algo_engine = self.main_engine.get_engine("algo")
        
        algo_engine.start_algo(
            template_name="TwapAlgo",
            vt_symbol=strategy.vt_symbol,
            direction=direction,
            offset=offset,
            price=price,
            volume=volume,
            setting={"time": 1800, "interval": 60}
        )
        return []  # No direct order
    else:
        # Small order: send directly
        return super().send_order(...)
```

---

## UI Integration

VeighNa provides a UI module for algo trading:

```python
# vnpy_algotrading/ui/widget.py
class AlgoWidget(QWidget):
    """Algorithm trading widget"""
    
    def __init__(self, algo_engine: AlgoEngine):
        self.algo_engine = algo_engine
        
        # Algorithm selection
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(list(algo_engine.algo_templates.keys()))
        
        # Parameter inputs
        self.symbol_line = QLineEdit()
        self.direction_combo = QComboBox()
        self.volume_spin = QSpinBox()
        self.price_spin = QDoubleSpinBox()
        
        # Start button
        self.start_button = QPushButton("启动算法")
        self.start_button.clicked.connect(self.start_algo)
        
        # Active algos table
        self.algo_table = QTableWidget()
```

---

## Summary

| Component | Purpose | Location |
|-----------|---------|----------|
| **AlgoEngine** | Manages algorithm instances | `vnpy_algotrading/engine.py` |
| **AlgoTemplate** | Base class for all algos | `vnpy_algotrading/template.py` |
| **TwapAlgo** | Time-weighted execution | `vnpy_algotrading/algos/twap_algo.py` |
| **IcebergAlgo** | Hide order size | `vnpy_algotrading/algos/iceberg_algo.py` |
| **VwapAlgo** | Volume-weighted (custom) | Your custom code |

**Execution Flow:**
```
Strategy Decision (Buy 10,000)
    ↓
AlgoEngine.start_algo()
    ↓
AlgoTemplate instance created
    ↓
on_tick() / on_timer() callbacks
    ↓
Child orders (Buy 100, Buy 100, ...)
    ↓
OMS → Gateway → Exchange
```

**For Indian Markets:**
- Use **TWAP** for liquid stocks (RELIANCE, TCS, INFY)
- Use **VWAP** for better volume-weighted execution
- Use **POV** for passive execution
- Customize based on NSE/BSE market conditions
