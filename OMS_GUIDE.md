# VeighNa OMS (Order Management System)

Complete guide to the Order Management System in VeighNa.

---

## OMS Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    VeighNa OMS Architecture                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    OmsEngine                              │   │
│  │  (vnpy/trader/engine.py)                                  │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │                                                           │   │
│  │  State Cache (In-Memory):                                 │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐            │   │
│  │  │  Ticks    │  │  Orders   │  │  Trades   │            │   │
│  │  │  (cache)  │  │  (cache)  │  │  (cache)  │            │   │
│  │  └───────────┘  └───────────┘  └───────────┘            │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐            │   │
│  │  │ Positions │  │ Accounts  │  │ Contracts │            │   │
│  │  │  (cache)  │  │  (cache)  │  │  (cache)  │            │   │
│  │  └───────────┘  └───────────┘  └───────────┘            │   │
│  │                                                           │   │
│  │  Active Tracking:                                         │   │
│  │  - active_orders (working orders)                         │   │
│  │  - active_quotes (working quotes)                         │   │
│  │                                                           │   │
│  │  Position Management:                                     │   │
│  │  - OffsetConverter (per gateway)                          │   │
│  │  - PositionHolding (per symbol)                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. OmsEngine

**Location:** `vnpy/trader/engine.py`

**Purpose:** Central state cache for all trading data

```python
class OmsEngine(BaseEngine):
    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        super().__init__(main_engine, event_engine, "oms")
        
        # State caches
        self.ticks: dict[str, TickData] = {}           # vt_symbol → TickData
        self.orders: dict[str, OrderData] = {}         # vt_orderid → OrderData
        self.trades: dict[str, TradeData] = {}         # vt_tradeid → TradeData
        self.positions: dict[str, PositionData] = {}   # vt_positionid → PositionData
        self.accounts: dict[str, AccountData] = {}     # vt_accountid → AccountData
        self.contracts: dict[str, ContractData] = {}   # vt_symbol → ContractData
        self.quotes: dict[str, QuoteData] = {}         # vt_quoteid → QuoteData
        
        # Active tracking
        self.active_orders: dict[str, OrderData] = {}  # Working orders only
        self.active_quotes: dict[str, QuoteData] = {}  # Working quotes only
        
        # Position offset conversion (for Chinese futures)
        self.offset_converters: dict[str, OffsetConverter] = {}
```

---

### 2. Event Registration

```python
def register_event(self) -> None:
    """Register event handlers"""
    self.event_engine.register(EVENT_TICK, self.process_tick_event)
    self.event_engine.register(EVENT_ORDER, self.process_order_event)
    self.event_engine.register(EVENT_TRADE, self.process_trade_event)
    self.event_engine.register(EVENT_POSITION, self.process_position_event)
    self.event_engine.register(EVENT_ACCOUNT, self.process_account_event)
    self.event_engine.register(EVENT_CONTRACT, self.process_contract_event)
    self.event_engine.register(EVENT_QUOTE, self.process_quote_event)
```

**Event Flow:**
```
Gateway → Event Engine → OmsEngine handlers → Update cache
```

---

### 3. Event Handlers

#### Tick Event
```python
def process_tick_event(self, event: Event) -> None:
    tick: TickData = event.data
    self.ticks[tick.vt_symbol] = tick  # Update cache
```

#### Order Event
```python
def process_order_event(self, event: Event) -> None:
    order: OrderData = event.data
    self.orders[order.vt_orderid] = order
    
    # Track active orders
    if order.is_active():
        self.active_orders[order.vt_orderid] = order
    elif order.vt_orderid in self.active_orders:
        self.active_orders.pop(order.vt_orderid)  # Remove filled/cancelled
    
    # Update offset converter
    converter = self.offset_converters.get(order.gateway_name)
    if converter:
        converter.update_order(order)
```

#### Trade Event
```python
def process_trade_event(self, event: Event) -> None:
    trade: TradeData = event.data
    self.trades[trade.vt_tradeid] = trade
    
    # Update offset converter
    converter = self.offset_converters.get(trade.gateway_name)
    if converter:
        converter.update_trade(trade)
```

#### Position Event
```python
def process_position_event(self, event: Event) -> None:
    position: PositionData = event.data
    self.positions[position.vt_positionid] = position
    
    # Update offset converter
    converter = self.offset_converters.get(position.gateway_name)
    if converter:
        converter.update_position(position)
```

---

### 4. Query API

```python
# Get single item
oms.get_tick("RELIANCE.NSE")           # → TickData or None
oms.get_order("IB.12345")              # → OrderData or None
oms.get_trade("IB.67890")              # → TradeData or None
oms.get_position("CTP.RB2401.LONG")    # → PositionData or None
oms.get_account("IB.U123456")          # → AccountData or None
oms.get_contract("IF2401.CFFEX")       # → ContractData or None

# Get all items
oms.get_all_ticks()                    # → list[TickData]
oms.get_all_orders()                   # → list[OrderData]
oms.get_all_trades()                   # → list[TradeData]
oms.get_all_positions()                # → list[PositionData]
oms.get_all_accounts()                 # → list[AccountData]
oms.get_all_contracts()                # → list[ContractData]

# Get active orders only
oms.get_all_active_orders()            # → list[OrderData] (working orders)
```

---

## PositionHolding: Advanced Position Tracking

**Location:** `vnpy/trader/converter.py`

### Purpose

Track position details for Chinese futures markets:
- **Today's position (td)** vs **Yesterday's position (yd)**
- **Frozen positions** (reserved for pending close orders)
- **Offset conversion** (CLOSE → CLOSETODAY/CLOSEYESTERDAY)

### Data Structure

```python
class PositionHolding:
    def __init__(self, contract: ContractData):
        self.vt_symbol: str = contract.vt_symbol
        self.exchange: Exchange = contract.exchange
        
        # Position volumes
        self.long_pos: float = 0      # Total long position
        self.long_yd: float = 0       # Yesterday's long
        self.long_td: float = 0       # Today's long
        
        self.short_pos: float = 0     # Total short position
        self.short_yd: float = 0      # Yesterday's short
        self.short_td: float = 0      # Today's short
        
        # Frozen volumes (reserved for pending close orders)
        self.long_pos_frozen: float = 0
        self.long_yd_frozen: float = 0
        self.long_td_frozen: float = 0
        
        self.short_pos_frozen: float = 0
        self.short_yd_frozen: float = 0
        self.short_td_frozen: float = 0
        
        # Active orders affecting this position
        self.active_orders: dict[str, OrderData] = {}
```

### Position Update Flow

```python
def update_position(self, position: PositionData) -> None:
    """Update from exchange position push"""
    if position.direction == Direction.LONG:
        self.long_pos = position.volume
        self.long_yd = position.yd_volume  # Yesterday's position
        self.long_td = self.long_pos - self.long_yd  # Today's = Total - Yesterday's
    else:
        self.short_pos = position.volume
        self.short_yd = position.yd_volume
        self.short_td = self.short_pos - self.short_yd
```

### Trade Update Flow

```python
def update_trade(self, trade: TradeData) -> None:
    """Update position from trade fill"""
    
    if trade.direction == Direction.LONG:
        if trade.offset == Offset.OPEN:
            self.long_td += trade.volume  # Open new long
        elif trade.offset == Offset.CLOSETODAY:
            self.short_td -= trade.volume  # Close today's short
        elif trade.offset == Offset.CLOSEYESTERDAY:
            self.short_yd -= trade.volume  # Close yesterday's short
        elif trade.offset == Offset.CLOSE:
            # Auto-detect for non-SHFE/INE exchanges
            if trade.exchange in {Exchange.SHFE, Exchange.INE}:
                self.short_yd -= trade.volume  # SHFE/INE: close yesterday first
            else:
                self.short_td -= trade.volume  # Others: close today first
                if self.short_td < 0:
                    self.short_yd += self.short_td  # Overflow to yesterday
                    self.short_td = 0
    else:  # SHORT direction
        if trade.offset == Offset.OPEN:
            self.short_td += trade.volume
        elif trade.offset == Offset.CLOSETODAY:
            self.long_td -= trade.volume
        elif trade.offset == Offset.CLOSEYESTERDAY:
            self.long_yd -= trade.volume
        elif trade.offset == Offset.CLOSE:
            if trade.exchange in {Exchange.SHFE, Exchange.INE}:
                self.long_yd -= trade.volume
            else:
                self.long_td -= trade.volume
                if self.long_td < 0:
                    self.long_yd += self.long_td
                    self.long_td = 0
    
    # Recalculate totals
    self.long_pos = self.long_td + self.long_yd
    self.short_pos = self.short_td + self.short_yd
```

---

## OffsetConverter: Chinese Futures Position Rules

### Why Offset Conversion is Needed

**Chinese Futures Market Rules:**

1. **SHFE (Shanghai Futures Exchange) & INE (INE):**
   - Must specify `CLOSETODAY` or `CLOSEYESTERDAY` explicitly
   - `CLOSE` is not accepted

2. **Other Exchanges (DCE, CZCE, CFFEX):**
   - `CLOSE` automatically closes today's position first
   - If today's position insufficient, close yesterday's

3. **Stocks (NSE, BSE):**
   - Net position mode (no td/yd distinction)
   - `CLOSE` is sufficient

### OffsetConverter Class

```python
class OffsetConverter:
    def __init__(self, oms_engine: OmsEngine):
        self.holdings: dict[str, PositionHolding] = {}  # vt_symbol → PositionHolding
        self.get_contract = oms_engine.get_contract
    
    def convert_order_request(
        self,
        req: OrderRequest,
        lock: bool = False,
        net: bool = False
    ) -> list[OrderRequest]:
        """
        Convert order request based on exchange rules
        
        Returns list of requests (may split into multiple orders)
        """
        if not self.is_convert_required(req.vt_symbol):
            return [req]  # No conversion needed (net position mode)
        
        holding = self.get_position_holding(req.vt_symbol)
        
        if lock:
            return holding.convert_order_request_lock(req)
        elif net:
            return holding.convert_order_request_net(req)
        elif req.exchange in {Exchange.SHFE, Exchange.INE}:
            return holding.convert_order_request_shfe(req)
        else:
            return [req]  # Other exchanges: no conversion needed
```

### SHFE/INE Conversion Example

```python
def convert_order_request_shfe(self, req: OrderRequest) -> list[OrderRequest]:
    """
    Convert CLOSE to CLOSETODAY/CLOSEYESTERDAY for SHFE/INE
    """
    if req.offset == Offset.OPEN:
        return [req]  # No conversion for OPEN
    
    # Calculate available positions
    if req.direction == Direction.LONG:  # Closing short position
        pos_available = self.short_pos - self.short_pos_frozen
        td_available = self.short_td - self.short_td_frozen
    else:  # Closing long position
        pos_available = self.long_pos - self.long_pos_frozen
        td_available = self.long_td - self.long_td_frozen
    
    if req.volume > pos_available:
        return []  # Insufficient position
    elif req.volume <= td_available:
        # All from today's position
        req_td = copy(req)
        req_td.offset = Offset.CLOSETODAY
        return [req_td]
    else:
        # Split: today + yesterday
        req_list = []
        
        if td_available > 0:
            req_td = copy(req)
            req_td.offset = Offset.CLOSETODAY
            req_td.volume = td_available
            req_list.append(req_td)
        
        req_yd = copy(req)
        req_yd.offset = Offset.CLOSEYESTERDAY
        req_yd.volume = req.volume - td_available
        req_list.append(req_yd)
        
        return req_list
```

**Example:**
```
Position: Long RB2401
  - long_td = 5 lots (today)
  - long_yd = 3 lots (yesterday)
  - long_pos = 8 lots (total)

User sends: SELL 6, offset=CLOSE

Converted to:
  1. SELL 5, offset=CLOSETODAY
  2. SELL 1, offset=CLOSEYESTERDAY
```

---

## Frozen Position Calculation

```python
def calculate_frozen(self) -> None:
    """Calculate frozen positions from active close orders"""
    
    self.long_pos_frozen = 0
    self.long_yd_frozen = 0
    self.long_td_frozen = 0
    self.short_pos_frozen = 0
    self.short_yd_frozen = 0
    self.short_td_frozen = 0
    
    for order in self.active_orders.values():
        if order.offset == Offset.OPEN:
            continue  # Ignore open orders
        
        frozen = order.volume - order.traded  # Remaining volume
        
        if order.direction == Direction.LONG:  # Closing short
            if order.offset == Offset.CLOSETODAY:
                self.short_td_frozen += frozen
            elif order.offset == Offset.CLOSEYESTERDAY:
                self.short_yd_frozen += frozen
            elif order.offset == Offset.CLOSE:
                self.short_td_frozen += frozen
                if self.short_td_frozen > self.short_td:
                    self.short_yd_frozen += (self.short_td_frozen - self.short_td)
                    self.short_td_frozen = self.short_td
        else:  # Closing long
            if order.offset == Offset.CLOSETODAY:
                self.long_td_frozen += frozen
            elif order.offset == Offset.CLOSEYESTERDAY:
                self.long_yd_frozen += frozen
            elif order.offset == Offset.CLOSE:
                self.long_td_frozen += frozen
                if self.long_td_frozen > self.long_td:
                    self.long_yd_frozen += (self.long_td_frozen - self.long_td)
                    self.long_td_frozen = self.long_td
    
    # Ensure frozen doesn't exceed available
    self.sum_pos_frozen()
```

**Purpose:** Prevent double-counting positions when calculating available volume for new orders.

---

## Usage in Strategies

### Query Position via OMS

```python
from vnpy.trader.engine import MainEngine

class MyStrategy(CtaTemplate):
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        
        # Access OMS engine
        self.oms = self.cta_engine.main_engine.get_engine("oms")
    
    def on_bar(self, bar: BarData):
        # Query current position
        position = self.oms.get_position(f"{self.gateway_name}.{bar.vt_symbol}.LONG")
        
        if position:
            print(f"Current position: {position.volume}")
            print(f"Available: {position.volume - position.frozen}")
        else:
            print("No position")
        
        # Query all positions
        all_positions = self.oms.get_all_positions()
        for pos in all_positions:
            print(f"{pos.vt_positionid}: {pos.volume}")
```

### Query Active Orders

```python
def check_pending_orders(self):
    """Check working orders"""
    active_orders = self.oms.get_all_active_orders()
    
    for order in active_orders:
        if order.vt_symbol == self.vt_symbol:
            print(f"Active order: {order.orderid} {order.direction} {order.volume}")
```

### Query Account

```python
def check_account(self):
    """Check account balance"""
    accounts = self.oms.get_all_accounts()
    
    for account in accounts:
        print(f"Account {account.accountid}:")
        print(f"  Balance: {account.balance}")
        print(f"  Available: {account.available}")
        print(f"  Frozen: {account.frozen}")
```

---

## OMS in MainEngine

```python
class MainEngine:
    def __init__(self, event_engine: EventEngine = None):
        if event_engine:
            self.event_engine = event_engine
        else:
            self.event_engine = EventEngine()
        self.event_engine.start()
        
        self.gateways: dict[str, BaseGateway] = {}
        self.engines: dict[str, BaseEngine] = {}
        self.apps: dict[str, BaseApp] = {}
        self.exchanges: list[Exchange] = []
        
        self.init_engines()  # Initialize OMS + Log engines
    
    def init_engines(self) -> None:
        """Initialize function engines"""
        self.add_engine(LogEngine)
        
        # Initialize OMS Engine
        oms_engine: OmsEngine = self.add_engine(OmsEngine)
        
        # Expose OMS query methods for convenience
        self.get_tick = oms_engine.get_tick
        self.get_order = oms_engine.get_order
        self.get_trade = oms_engine.get_trade
        self.get_position = oms_engine.get_position
        self.get_account = oms_engine.get_account
        self.get_contract = oms_engine.get_contract
        self.get_all_ticks = oms_engine.get_all_ticks
        self.get_all_orders = oms_engine.get_all_orders
        self.get_all_trades = oms_engine.get_all_trades
        self.get_all_positions = oms_engine.get_all_positions
        self.get_all_accounts = oms_engine.get_all_accounts
        self.get_all_contracts = oms_engine.get_all_contracts
        self.get_all_active_orders = oms_engine.get_all_active_orders
```

**Usage:**
```python
main_engine = MainEngine()

# Direct access via MainEngine
tick = main_engine.get_tick("RELIANCE.NSE")
position = main_engine.get_position("CTP.RB2401.LONG")
account = main_engine.get_account("CTP.123456")
```

---

## Multi-Gateway OMS

```
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Gateway OMS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Gateway: CTP                         Gateway: IB                │
│  ┌─────────────────────┐            ┌─────────────────────┐     │
│  │ OffsetConverter     │            │ OffsetConverter     │     │
│  │ (Chinese futures)   │            │ (Net position)      │     │
│  │ PositionHolding     │            │ PositionHolding     │     │
│  │ - RB2401 (SHFE)     │            │ - SPY (STK)         │     │
│  │ - IF2401 (CFFEX)    │            │ - EURUSD (CASH)     │     │
│  └─────────────────────┘            └─────────────────────┘     │
│                                                                  │
│              ↓                           ↓                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    OmsEngine                             │    │
│  │  - Unified position view across all gateways            │    │
│  │  - Per-gateway offset conversion                        │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Summary

| Component | Purpose | Location |
|-----------|---------|----------|
| **OmsEngine** | Central state cache | `vnpy/trader/engine.py` |
| **PositionHolding** | Track td/yd positions | `vnpy/trader/converter.py` |
| **OffsetConverter** | Convert offset for exchanges | `vnpy/trader/converter.py` |

**Key Features:**

1. **State Caching:** All ticks, orders, trades, positions, accounts in memory
2. **Active Tracking:** Working orders automatically tracked
3. **Position Conversion:** SHFE/INE td/yd rules handled automatically
4. **Frozen Calculation:** Prevent over-trading
5. **Multi-Gateway:** Unified view across CTP, IB, etc.

**For Indian Markets:**

- **NSE/BSE stocks:** Net position mode (no offset conversion needed)
- **Futures (if available):** Use standard `CLOSE` offset
- **No td/yd distinction:** Unlike Chinese futures

**Query API:**
```python
main_engine.get_tick("RELIANCE.NSE")
main_engine.get_position("IB.RELIANCE.LONG")
main_engine.get_account("IB.U123456")
main_engine.get_all_active_orders()
```
