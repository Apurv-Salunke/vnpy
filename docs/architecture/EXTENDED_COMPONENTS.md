# VeighNa Extended Components

Detailed architecture of additional VeighNa components including Risk Manager, Portfolio Manager, Data Recorder, and more.

---

## Complete Component Ecosystem

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        VeighNa Complete Ecosystem                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                         Strategy Layer                                      │ │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐      │ │
│  │  │ CtaStrategy  │ │SpreadStrategy│ │PortfStrategy │ │ScriptStrategy│      │ │
│  │  │ (Single)     │ │ (Multi-leg)  │ │ (Multi-asset)│ │ (Custom)     │      │ │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘      │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                             │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                         Execution Layer                                     │ │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐      │ │
│  │  │AlgoTrading   │ │ OptionMaster │ │ PaperAccount │ │  (More...)   │      │ │
│  │  │(TWAP/Iceberg)│ │(Greeks/IV)   │ │(Simulation)  │ │              │      │ │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘      │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                             │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                         Risk & Control Layer                                │ │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐      │ │
│  │  │RiskManager   │ │PortfManager  │ │ DataRecorder │ │  DataManager │      │ │
│  │  │(Pre-trade)   │ │ (PnL Track)  │ │(Market Data) │ │ (History)    │      │ │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘      │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                             │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                         Gateway Layer                                       │ │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐      │ │
│  │  │ CtpGateway   │ │  IbGateway   │ │BinanceGateway│ │  More...     │      │ │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘      │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Risk Manager Component

**Package:** `vnpy_riskmanager`

**Purpose:** Pre-trade risk control to prevent erroneous orders and enforce trading limits.

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    RiskManager Engine                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Order Request (from Strategy)                                  │
│            ↓                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Risk Rule Engine                              │  │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐      │  │
│  │  │ActiveOrder   │ │ DailyLimit   │ │ OrderSize    │      │  │
│  │  │Rule          │ │ Rule         │ │ Rule         │      │  │
│  │  └──────────────┘ └──────────────┘ └──────────────┘      │  │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐      │  │
│  │  │Duplicate     │ │ OrderValidity│ │ CustomRule   │      │  │
│  │  │OrderRule     │ │ Rule         │ │ (Plugin)     │      │  │
│  │  └──────────────┘ └──────────────┘ └──────────────┘      │  │
│  └───────────────────────────────────────────────────────────┘  │
│            ↓                                                     │
│       Allowed?                                                   │
│      ↙          ↘                                               │
│    YES          NO                                              │
│     ↓            ↓                                               │
│  Forward to    Reject + Log                                     │
│  Gateway                                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Risk Rules (Built-in)

| Rule | Check | Example |
|------|-------|---------|
| **ActiveOrderRule** | Max active orders | Max 10 working orders |
| **DailyLimitRule** | Max orders/day | Max 100 orders per day |
| **DuplicateOrderRule** | Duplicate detection | Same price/volume in 1s |
| **OrderSizeRule** | Max order size | Max 100 lots per order |
| **OrderValidityRule** | Order validity | Price tick, max volume |

### Usage

```python
from vnpy_riskmanager import RiskEngine, RuleTemplate

class MyCustomRule(RuleTemplate):
    """Custom risk rule"""
    
    name: str = "MyCustomRule"
    
    parameters: dict[str, str] = {
        "max_volume": "Maximum volume per order"
    }
    
    def on_init(self) -> None:
        self.max_volume: int = 100
    
    def check_allowed(self, req: OrderRequest, gateway_name: str) -> bool:
        if req.volume > self.max_volume:
            msg = f"Volume {req.volume} exceeds limit {self.max_volume}"
            self.write_log(msg)
            return False
        return True

# Register rule
risk_engine.add_rule(MyCustomRule)
```

### Integration with MainEngine

```python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy_riskmanager import RiskManagerApp

event_engine = EventEngine()
main_engine = MainEngine(event_engine)

# Add risk manager (auto-starts)
main_engine.add_app(RiskManagerApp)

# Now all orders go through risk checks
main_engine.send_order(req, gateway_name)
# ↓
# RiskManager.check_allowed(req)
# ↓
# If allowed → Gateway.send_order(req)
# If rejected → Log + Return
```

---

## 2. Portfolio Manager Component

**Package:** `vnpy_portfoliomanager`

**Purpose:** Track PnL and positions for multiple strategy portfolios (sub-accounts).

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   PortfolioManager Engine                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              PortfolioResult (Parent)                      │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  Portfolio: "My CTA Strategy"                        │  │  │
│  │  │  - Total PnL: +$50,000                               │  │  │
│  │  │  - Daily PnL: +$2,500                                │  │  │
│  │  │  - Positions: 15 contracts                           │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │         ↓ contains                                         │  │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐      │  │
│  │  │ContractResult│ │ContractResult│ │ContractResult│      │  │
│  │  │ RB2401       │ │ IF2401       │ │ AU2406       │      │  │
│  │  │ PnL: +$10k   │ │ PnL: +$25k   │ │ PnL: +$15k   │      │  │
│  │  └──────────────┘ └──────────────┘ └──────────────┘      │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Trade Event → Update ContractResult → Update PortfolioResult   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Data Model

```python
class ContractResult:
    """Result for single contract"""
    
    def __init__(self, reference: str, vt_symbol: str):
        self.reference: str = reference          # Portfolio reference
        self.vt_symbol: str = vt_symbol          # Contract symbol
        
        self.open_pos: float = 0                 # Opening position
        self.last_pos: float = 0                 # Current position
        
        self.trading_pnl: float = 0              # Realized PnL
        self.holding_pnl: float = 0              # Unrealized PnL
        self.total_pnl: float = 0                # Total PnL
        
        self.long_volume: float = 0
        self.short_volume: float = 0
        self.long_cost: float = 0
        self.short_cost: float = 0
    
    def update_trade(self, trade: TradeData) -> None:
        """Update from trade fill"""
        if trade.direction == Direction.LONG:
            self.last_pos += trade.volume
            self.long_cost += trade.price * trade.volume
        else:
            self.last_pos -= trade.volume
            self.short_cost += trade.price * trade.volume
    
    def calculate_pnl(self, last_price: float, size: float) -> None:
        """Calculate PnL from current price"""
        # Realized PnL from trades
        long_value = self.long_volume * last_price * size
        long_pnl = long_value - self.long_cost
        
        short_value = self.short_volume * last_price * size
        short_pnl = self.short_cost - short_value
        
        self.trading_pnl = long_pnl + short_pnl
        
        # Unrealized PnL from open position
        self.holding_pnl = (last_price - tick.pre_close) * self.open_pos * size
        self.total_pnl = self.holding_pnl + self.trading_pnl


class PortfolioResult:
    """Result for entire portfolio"""
    
    def __init__(self, reference: str):
        self.reference: str = reference
        self.trading_pnl: float = 0
        self.holding_pnl: float = 0
        self.total_pnl: float = 0
    
    def add_contract_result(self, contract_result: ContractResult) -> None:
        """Aggregate contract results"""
        self.trading_pnl += contract_result.trading_pnl
        self.holding_pnl += contract_result.holding_pnl
        self.total_pnl += contract_result.total_pnl
```

### Usage

```python
from vnpy_portfoliomanager import PortfolioEngine

# Initialize
portfolio_engine = PortfolioEngine(main_engine, event_engine)

# Create portfolio
portfolio_engine.create_portfolio("My CTA Strategy")

# Add trades (automatically from event engine)
# Trade event → PortfolioEngine.process_trade_event()
# → Update ContractResult → Update PortfolioResult

# Query portfolio PnL
portfolio_data = portfolio_engine.get_portfolio_data("My CTA Strategy")
print(f"Total PnL: {portfolio_data['total_pnl']}")
```

---

## 3. Data Recorder Component

**Package:** `vnpy_datarecorder`

**Purpose:** Record real-time market data (ticks, bars) to database for later backtesting.

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DataRecorder Engine                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Tick Event (from Event Engine)                                 │
│            ↓                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Recording Filter                              │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  Active Recordings: {vt_symbol: Interval}            │  │  │
│  │  │  - "RB2401.SHFE": MINUTE                             │  │  │
│  │  │  - "IF2401.CFFEX": MINUTE                            │  │  │
│  │  │  - "AU2406.SHFE": TICK                               │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│            ↓                                                     │
│       Is Recording?                                              │
│      ↙          ↘                                               │
│    YES          NO                                              │
│     ↓            ↓                                               │
│  Buffer       Ignore                                            │
│     ↓                                                            │
│  Batch Write (every 100 bars / 1 second)                        │
│     ↓                                                            │
│  Database (SQLite/MySQL/PostgreSQL/MongoDB)                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Usage

```python
from vnpy_datarecorder import DataRecorderEngine

# Initialize
recorder_engine = DataRecorderEngine(main_engine, event_engine)

# Start recording
recorder_engine.add_bar_recording(
    vt_symbol="RB2401.SHFE",
    interval=Interval.MINUTE
)

recorder_engine.add_tick_recording(
    vt_symbol="IF2401.CFFEX"
)

# Stop recording
recorder_engine.remove_bar_recording("RB2401.SHFE")

# Query active recordings
active_recordings = recorder_engine.get_all_bar_recordings()
```

### UI Integration

```
┌─────────────────────────────────────────────────────────┐
│              DataRecorder Widget                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Symbol: [RB2401.SHFE ▼]  Interval: [1min ▼]            │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Active Recordings                                │   │
│  │  ┌────────────────────────────────────────────┐   │   │
│  │  │ RB2401.SHFE    1min      [Stop] [Remove]   │   │   │
│  │  │ IF2401.CFFEX   1min      [Stop] [Remove]   │   │   │
│  │  │ AU2406.SHFE    TICK      [Stop] [Remove]   │   │   │
│  │  └────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  [+ Add Recording]  [Start All]  [Stop All]             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Data Manager Component

**Package:** `vnpy_datamanager`

**Purpose:** Manage historical data in database (view, import, export, delete).

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DataManager Engine                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Data Tree View                                │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │ 📁 CFFEX                                             │  │  │
│  │  │   📁 IF2401 (Index)                                 │  │  │
│  │  │     📄 1min (125,430 bars)                          │  │  │
│  │  │     📄 1hour (2,091 bars)                           │  │  │
│  │  │   📁 T2406 (Index)                                  │  │  │
│  │  │     📄 1min (89,234 bars)                           │  │  │
│  │  │ 📁 SHFE                                              │  │  │
│  │  │   📁 RB2401 (Index)                                 │  │  │
│  │  │     📄 1min (156,789 bars)                          │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│            ↓ Select                                             │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Data Table View                               │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  datetime           open    high     low   close    │  │  │
│  │  │  2024-01-15 09:15   3800    3810    3795    3805   │  │  │
│  │  │  2024-01-15 09:16   3805    3815    3800    3810   │  │  │
│  │  │  ...                                                 │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  [Import CSV]  [Export CSV]  [Delete]  [Update]  [Download]    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Usage

```python
from vnpy_datamanager import DataManagerEngine

# Initialize
data_manager = DataManagerEngine(main_engine, event_engine)

# Import from CSV
data_manager.import_data_from_csv(
    vt_symbol="RB2401.SHFE",
    interval=Interval.MINUTE,
    filename="rb2401_2024_1min.csv"
)

# Export to CSV
data_manager.export_data_to_csv(
    vt_symbol="IF2401.CFFEX",
    interval=Interval.MINUTE,
    start=datetime(2024, 1, 1),
    end=datetime(2024, 12, 31),
    filename="if2401_2024_1min.csv"
)

# Delete data
data_manager.remove_data(
    vt_symbol="RB2401.SHFE",
    interval=Interval.MINUTE,
    start=datetime(2024, 1, 1),
    end=datetime(2024, 1, 31)
)

# Query data overview
overview = data_manager.get_bar_overview("RB2401.SHFE", Interval.MINUTE)
print(f"Total bars: {overview.count}")
print(f"Date range: {overview.start} to {overview.end}")
```

---

## 5. Paper Account Component

**Package:** `vnpy_paperaccount`

**Purpose:** Simulated trading based on real-time market data (paper trading).

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PaperAccount Engine                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              PaperGateway                                  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  Simulated Account                                   │  │  │
│  │  │  - Balance: ¥1,000,000                               │  │  │
│  │  │  - Available: ¥850,000                               │  │  │
│  │  │  - Frozen: ¥150,000                                  │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  Matching Engine                                     │  │  │
│  │  │  - Order book (local)                                │  │  │
│  │  │  - Fill logic (price + time priority)                │  │  │
│  │  │  - Slippage model (configurable)                     │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Real Tick Data (from Event Engine)                             │
│            ↓                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Order Matching Logic                                      │  │
│  │                                                            │  │
│  │  if order.direction == LONG:                              │  │
│  │      if tick.last_price <= order.price:                   │  │
│  │          fill_order(order, tick.last_price)               │  │
│  │  else:  # SHORT                                           │  │
│  │      if tick.last_price >= order.price:                   │  │
│  │          fill_order(order, tick.last_price)               │  │
│  └───────────────────────────────────────────────────────────┘  │
│            ↓                                                     │
│  Trade Event (pushed to Event Engine)                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Usage

```python
from vnpy_paperaccount import PaperEngine

# Initialize with initial capital
paper_engine = PaperEngine(
    main_engine,
    event_engine,
    initial_balance=1_000_000
)

# Paper gateway acts like a real gateway
paper_gateway = paper_engine.get_gateway()

# Add to main engine
main_engine.add_gateway(paper_gateway)

# Now trade through paper gateway
main_engine.send_order(req, gateway_name="PAPER")
# ↓
# PaperGateway.match_order(req, tick)
# ↓
# If filled → Trade event → Event Engine
```

---

## 6. Chart Wizard Component

**Package:** `vnpy_chartwizard`

**Purpose:** Real-time K-line chart visualization.

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ChartWizard Engine                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Tick Event (from Event Engine)                                 │
│            ↓                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              BarGenerator                                  │  │
│  │  (Synthesizes 1min bars from ticks)                       │  │
│  └───────────────────────────────────────────────────────────┘  │
│            ↓                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Chart Manager                                 │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  Candlestick Series                                  │  │  │
│  │  │  - Open, High, Low, Close                            │  │  │
│  │  │  - Volume bars                                       │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  Indicator Series                                    │  │  │
│  │  │  - MA, MACD, RSI, Bollinger Bands, etc.             │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│            ↓                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Chart Widget (PyQtGraph)                      │  │
│  │  - Real-time updates                                       │  │
│  │  - Zoom, pan                                               │  │
│  │  - Multiple indicators                                     │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Usage

```python
from vnpy_chartwizard import ChartEngine
from vnpy.trader.object import BarGenerator

# Initialize
chart_engine = ChartEngine(main_engine, event_engine)

# Create chart
chart = chart_engine.create_chart(
    vt_symbol="RB2401.SHFE",
    interval=Interval.MINUTE
)

# Add indicators
chart.add_indicator("MA", period=10)
chart.add_indicator("MA", period=30)
chart.add_indicator("MACD", fast=12, slow=26, signal=9)
chart.add_indicator("RSI", period=14)

# Update chart (from bar event)
def on_bar(bar: BarData):
    chart.update_bar(bar)
```

---

## 7. Web Trader Component

**Package:** `vnpy_webtrader`

**Purpose:** Web-based trading interface (B/S architecture).

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    WebTrader Architecture                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐         ┌─────────────────┐               │
│  │   Web Browser   │         │  Mobile App     │               │
│  │   (Vue.js/JS)   │         │  (React Native) │               │
│  └────────┬────────┘         └────────┬────────┘               │
│           │                            │                        │
│           │ HTTP REST + WebSocket      │                        │
│           ↓                            ↓                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              WebEngine                                     │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  FastAPI Server                                      │  │  │
│  │  │  - REST API (order, cancel, query)                   │  │  │
│  │  │  - WebSocket (tick, order, trade push)               │  │  │
│  │  │  - JWT Authentication                                │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  RPC Client                                          │  │  │
│  │  │  - Connects to Trading Server                        │  │  │
│  │  │  - Forwards requests/responses                       │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              ↓                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │         RPC Server (Trading Server)                        │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  MainEngine + EventEngine                           │  │  │
│  │  │  - Gateways (CTP, IB, etc.)                         │  │  │
│  │  │  - Engines (OMS, CTA, etc.)                         │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### REST API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/token` | POST | Get access token |
| `/tick` | GET | Get tick data |
| `/order` | POST | Send order |
| `/cancel` | POST | Cancel order |
| `/position` | GET | Get positions |
| `/account` | GET | Get account |
| `/contract` | GET | Get contracts |

### WebSocket Events

| Event | Data |
|-------|------|
| `tick` | TickData |
| `order` | OrderData |
| `trade` | TradeData |
| `position` | PositionData |
| `account` | AccountData |

---

## 8. RPC Service Component

**Package:** `vnpy_rpcservice`

**Purpose:** Distributed architecture support (multi-process).

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    RPC Service Architecture                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Server Process                                │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  MainEngine + EventEngine                           │  │  │
│  │  │  - CtpGateway (real connection)                      │  │  │
│  │  │  - OmsEngine (state management)                      │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │            ↓                                               │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  RpcServer                                           │  │  │
│  │  │  - ZeroMQ REP socket (request/response)              │  │  │
│  │  │  - ZeroMQ PUB socket (publish/subscribe)             │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│              ↕ ZeroMQ (TCP)                                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Client Process 1                              │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  RpcClient                                           │  │  │
│  │  │  - ZeroMQ REQ socket                                 │  │  │
│  │  │  - ZeroMQ SUB socket                                 │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │            ↓                                               │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  CtaEngine + Strategies                              │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│              ↕ ZeroMQ (TCP)                                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Client Process 2                              │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  RpcClient                                           │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │            ↓                                               │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  PortfolioStrategy + Strategies                      │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Use Cases

**1. Strategy Isolation**
```
Process 1: Gateway + OMS (critical, high priority)
Process 2: CTA Strategies (can crash, isolated)
Process 3: Research/Backtesting (CPU intensive, isolated)
```

**2. Multi-Strategy Deployment**
```
Process 1: CTP Gateway + OMS (shared)
Process 2: CTA Strategy A (independent)
Process 3: CTA Strategy B (independent)
Process 4: Portfolio Strategy C (independent)
```

**3. Load Balancing**
```
Process 1: Gateway + OMS
Process 2: RPC Client + CTA Strategies (10 strategies)
Process 3: RPC Client + CTA Strategies (10 strategies)
Process 4: RPC Client + Portfolio Strategies (5 strategies)
```

---

## Component Integration Example

```python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

# Import components
from vnpy_ctp import CtpGateway
from vnpy_ctastrategy import CtaStrategyApp
from vnpy_riskmanager import RiskManagerApp
from vnpy_datamanager import DataManagerApp
from vnpy_datarecorder import DataRecorderApp
from vnpy_chartwizard import ChartWizardApp
from vnpy_portfoliomanager import PortfolioManagerApp

def main():
    qapp = create_qapp()
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    
    # Add gateway
    main_engine.add_gateway(CtpGateway)
    
    # Add strategy engine
    main_engine.add_app(CtaStrategyApp)
    
    # Add risk manager (pre-trade checks)
    main_engine.add_app(RiskManagerApp)
    
    # Add data management
    main_engine.add_app(DataManagerApp)
    main_engine.add_app(DataRecorderApp)
    
    # Add portfolio tracking
    main_engine.add_app(PortfolioManagerApp)
    
    # Add charting
    main_engine.add_app(ChartWizardApp)
    
    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()
    
    qapp.exec()

if __name__ == "__main__":
    main()
```

---

## Summary Table

| Component | Package | Layer | Purpose |
|-----------|---------|-------|---------|
| **RiskManager** | vnpy_riskmanager | Risk & Control | Pre-trade risk checks |
| **PortfolioManager** | vnpy_portfoliomanager | Risk & Control | PnL tracking per portfolio |
| **DataRecorder** | vnpy_datarecorder | Risk & Control | Real-time data recording |
| **DataManager** | vnpy_datamanager | Risk & Control | Historical data management |
| **PaperAccount** | vnpy_paperaccount | Execution | Simulated trading |
| **ChartWizard** | vnpy_chartwizard | Execution | Real-time charting |
| **WebTrader** | vnpy_webtrader | Execution | Web interface |
| **RpcService** | vnpy_rpcservice | Execution | Distributed architecture |

---

## Design Philosophy

> **Modular by Design** - Each component is independent and can be used alone or in combination.

**Benefits:**
1. **Flexibility** - Use only what you need
2. **Testability** - Test components independently
3. **Extensibility** - Add new components without modifying existing ones
4. **Maintainability** - Each component has clear responsibility

**Integration Pattern:**
```
Event Engine (Pub/Sub) ← All components communicate through events
    ↓
MainEngine (Orchestrator) ← Loads and coordinates components
    ↓
Components (Plugins) ← Independent, swappable
```

This architecture allows VeighNa to scale from a simple single-strategy setup to a complex multi-strategy, distributed trading system.
