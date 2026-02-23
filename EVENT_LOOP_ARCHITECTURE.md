# VeighNa Event Loop Architecture

Complete guide to understanding how events flow through the VeighNa trading platform.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         VeighNa Platform                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │   Gateway 1  │    │   Gateway 2  │    │   Gateway N  │          │
│  │   (CTP/IB)   │    │  (Binance)   │    │   (XTP)      │          │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘          │
│         │                   │                   │                   │
│         └───────────────────┼───────────────────┘                   │
│                             ↓                                       │
│                  ┌────────────────────┐                             │
│                  │    Event Engine    │ ←── EVENT_TIMER (1s)        │
│                  │  (Pub/Sub Queue)   │                             │
│                  └────────────────────┘                             │
│                             │                                       │
│         ┌───────────────────┼───────────────────┐                   │
│         ↓                   ↓                   ↓                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │ OMS Engine   │    │ CTA Engine   │    │ Log Engine   │          │
│  │ (State Mgmt) │    │ (Strategies) │    │ (Logging)    │          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Event Engine (The Heart)

**Location:** `vnpy/event/engine.py`

```python
class EventEngine:
    def __init__(self, interval: int = 1):
        self._interval = interval          # Timer interval (seconds)
        self._queue = Queue()              # Thread-safe event queue
        self._active = False               # Engine running flag
        self._thread = Thread(target=self._run)    # Event processing thread
        self._timer = Thread(target=self._run_timer)  # Timer thread
        self._handlers = defaultdict(list)  # Event type → handlers mapping
        self._general_handlers = []         # Global handlers (all events)
```

**Event Flow:**
```
1. Producer puts event → Queue
2. Event thread gets event from Queue
3. Event distributed to registered handlers
4. Handlers process event synchronously
```

**Event Structure:**
```python
class Event:
    def __init__(self, type: str, data: Any = None):
        self.type = type    # Event type string (e.g., "eTick.", "eOrder.")
        self.data = data    # Data object (TickData, OrderData, etc.)
```

---

### 2. Event Types

**Location:** `vnpy/trader/event.py`

| Event Type | String | Data Object | Frequency |
|------------|--------|-------------|-----------|
| `EVENT_TICK` | `"eTick."` | `TickData` | High (market data) |
| `EVENT_TRADE` | `"eTrade."` | `TradeData` | Medium (fills) |
| `EVENT_ORDER` | `"eOrder."` | `OrderData` | Medium (order updates) |
| `EVENT_POSITION` | `"ePosition."` | `PositionData` | Low (position changes) |
| `EVENT_ACCOUNT` | `"eAccount."` | `AccountData` | Low (balance updates) |
| `EVENT_CONTRACT` | `"eContract."` | `ContractData` | Once (startup) |
| `EVENT_LOG` | `"eLog"` | `LogData` | Medium (logs) |
| `EVENT_TIMER` | `"eTimer"` | `None` | 1 Hz (every second) |

**Event Naming Convention:**
- General events: `"eTick."` (all ticks)
- Specific events: `"eTick.BTCUSDT.BINANCE"` (specific symbol)

---

## Complete Event Loop Flow

### Scenario 1: Tick Data Processing

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Gateway receives tick from exchange                     │
└─────────────────────────────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Gateway pushes event to Event Engine                    │
│  self.event_engine.put(Event(EVENT_TICK, tick))                 │
└─────────────────────────────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Event Engine queues event                               │
│  _queue.put(event)                                              │
└─────────────────────────────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Event Thread processes event                            │
│  event = _queue.get()                                           │
│  _process(event)                                                │
└─────────────────────────────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Event distributed to registered handlers                │
│  for handler in _handlers[EVENT_TICK]:                          │
│      handler(event)                                             │
└─────────────────────────────────────────────────────────────────┘
    │
    ├─────────────────┬─────────────────┬─────────────────┐
    ↓                 ↓                 ↓                 ↓
┌─────────┐    ┌───────────┐    ┌──────────┐    ┌────────────┐
│   OMS   │    │   CTA     │    │  Data    │    │   Chart    │
│ Engine  │    │  Engine   │    │ Recorder │    │  Wizard    │
└─────────┘    └───────────┘    └──────────┘    └────────────┘
```

**Handler Code Examples:**

**OMS Engine (state management):**
```python
# vnpy/trader/engine.py - OmsEngine
def register_event(self) -> None:
    self.event_engine.register(EVENT_TICK, self.process_tick_event)

def process_tick_event(self, event: Event) -> None:
    tick: TickData = event.data
    self.ticks[tick.vt_symbol] = tick  # Update cache
```

**CTA Engine (strategy execution):**
```python
# vnpy_ctastrategy/engine.py - CtaEngine
def register_event(self) -> None:
    self.event_engine.register(EVENT_TICK, self.process_tick_event)

def process_tick_event(self, event: Event) -> None:
    tick: TickData = event.data
    
    # Get all strategies subscribed to this symbol
    strategies: list = self.symbol_strategy_map[tick.vt_symbol]
    
    for strategy in strategies:
        if strategy.inited:
            # Call strategy's on_tick method
            self.call_strategy_func(strategy, strategy.on_tick, tick)
```

**Data Recorder (persistence):**
```python
# vnpy_datarecorder/engine.py
def process_tick_event(self, event: Event) -> None:
    tick: TickData = event.data
    
    # Save to database
    self.database.save_tick_data([tick])
```

---

### Scenario 2: Order Placement Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Strategy sends order                                    │
│  self.buy(price, volume)  # In CtaTemplate                      │
└─────────────────────────────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: CTA Engine sends order via MainEngine                   │
│  vt_orderid = self.main_engine.send_order(req, gateway_name)    │
└─────────────────────────────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: MainEngine routes to Gateway                            │
│  gateway = self.gateways[gateway_name]                          │
│  return gateway.send_order(req)                                 │
└─────────────────────────────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Gateway sends to exchange & creates OrderData           │
│  order = req.create_order_data(orderid, gateway_name)           │
│  order.status = Status.SUBMITTING                               │
│  self.on_order(order)  # Callback                               │
└─────────────────────────────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Gateway pushes order event                              │
│  self.on_event(EVENT_ORDER, order)                              │
│  self.on_event(EVENT_ORDER + order.vt_orderid, order)           │
└─────────────────────────────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 6: Event Engine distributes to handlers                    │
│  - OMS Engine: Update order cache                               │
│  - CTA Engine: Call strategy.on_order()                         │
│  - UI: Update order widget                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

### Scenario 3: Trade Fill Flow

```
Exchange/Broker
    │
    ↓ (trade confirmation)
┌─────────────────────────────────────────────────────────────────┐
│ Gateway receives trade fill                                     │
│  trade = TradeData(...)                                         │
│  self.on_trade(trade)                                           │
└─────────────────────────────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Gateway pushes trade event                                      │
│  self.on_event(EVENT_TRADE, trade)                              │
│  self.on_event(EVENT_TRADE + trade.vt_tradeid, trade)           │
└─────────────────────────────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Event Engine distributes                                        │
└─────────────────────────────────────────────────────────────────┘
    │
    ├─────────────────┬─────────────────┐
    ↓                 ↓                 ↓
┌─────────┐    ┌───────────┐    ┌──────────────┐
│   OMS   │    │   CTA     │    │  Portfolio   │
│ Engine  │    │  Engine   │    │   Manager    │
│         │    │           │    │              │
│ Update  │    │ Update    │    │ Calculate    │
│ trade   │    │ strategy  │    │ PnL          │
│ cache   │    │ position  │    │              │
└─────────┘    └───────────┘    └──────────────┘
```

**CTA Engine Trade Processing:**
```python
def process_trade_event(self, event: Event) -> None:
    trade: TradeData = event.data
    
    # Filter duplicate trade push
    if trade.vt_tradeid in self.vt_tradeids:
        return
    self.vt_tradeids.add(trade.vt_tradeid)
    
    # Find strategy that placed this order
    strategy: CtaTemplate = self.orderid_strategy_map.get(trade.vt_orderid)
    if not strategy:
        return
    
    # Update strategy position BEFORE calling on_trade
    if trade.direction == Direction.LONG:
        strategy.pos += trade.volume
    else:
        strategy.pos -= trade.volume
    
    # Call strategy callback
    self.call_strategy_func(strategy, strategy.on_trade, trade)
    
    # Sync strategy data to file
    self.sync_strategy_data(strategy)
```

---

## Thread Model

```
┌─────────────────────────────────────────────────────────────────┐
│                         Main Thread                              │
│  - Qt GUI event loop (if UI enabled)                            │
│  - User interactions                                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      Event Thread                                │
│  - while _active:                                               │
│      event = _queue.get(block=True, timeout=1)                  │
│      self._process(event)  # Handler calls                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       Timer Thread                               │
│  - while _active:                                               │
│      sleep(self._interval)  # 1 second                          │
│      event = Event(EVENT_TIMER)                                 │
│      self.put(event)                                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     Gateway Threads                              │
│  - REST API threads (query responses)                           │
│  - Websocket threads (market data, order updates)               │
│  - TCP threads (IB TWS connection)                              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    Strategy Threads                              │
│  - CTA Engine: ThreadPoolExecutor for strategy init             │
│  - Each strategy runs in main event thread (callbacks)          │
└─────────────────────────────────────────────────────────────────┘
```

**Thread Safety:**
- Event queue is thread-safe (`queue.Queue`)
- Handlers are called sequentially in event thread
- Gateways push events from their threads → thread-safe
- Strategies should NOT modify shared state across threads

---

## Advanced Use Cases

### 1. Multi-Gateway Architecture

```python
# Multiple gateways can run simultaneously
main_engine.add_gateway(CtpGateway)      # Domestic futures
main_engine.add_gateway(IbGateway)       # International markets
main_engine.add_gateway(BinanceGateway)  # Crypto

# Each gateway has independent event stream
# OMS Engine consolidates all positions/orders
```

**Event Flow:**
```
CTP Gateway ──┐
              ├→ Event Engine ─→ OMS (unified view)
IB Gateway ───┘
```

---

### 2. Distributed Architecture (RPC)

```
┌─────────────────────────────────────────────────────────────┐
│                    Server Process                            │
│  ┌─────────────┐    ┌──────────────┐                        │
│  │  Gateway    │    │   OMS        │                        │
│  │  (CTP/IB)   │    │   Engine     │                        │
│  └──────┬──────┘    └──────┬───────┘                        │
│         │                  │                                 │
│         └──────────────────┘                                 │
│                    ↓                                         │
│         ┌──────────────────┐                                 │
│         │  RPC Server      │  ← Publishes events            │
│         └──────────────────┘                                 │
└─────────────────────────────────────────────────────────────┘
                    ↓
         (ZeroMQ RPC/RPC)
                    ↓
┌─────────────────────────────────────────────────────────────┐
│                   Client Process 1                           │
│  ┌─────────────┐    ┌──────────────┐                        │
│  │  CTA        │    │   RPC        │                        │
│  │  Engine     │    │   Client     │                        │
│  └─────────────┘    └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   Client Process 2                           │
│  ┌─────────────┐    ┌──────────────┐                        │
│  │  Portfolio  │    │   RPC        │                        │
│  │  Strategy   │    │   Client     │                        │
│  └─────────────┘    └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

---

### 3. Strategy Event Filtering

```python
# CTA Engine only sends relevant events to each strategy
def process_tick_event(self, event: Event) -> None:
    tick: TickData = event.data
    
    # Get ONLY strategies subscribed to this symbol
    strategies: list = self.symbol_strategy_map[tick.vt_symbol]
    
    for strategy in strategies:
        if strategy.inited:
            self.call_strategy_func(strategy, strategy.on_tick, tick)

# symbol_strategy_map built during strategy initialization
def add_strategy(self, strategy_class: type, setting: dict) -> None:
    # ...
    for vt_symbol in strategy.vt_symbols:
        self.symbol_strategy_map[vt_symbol].append(strategy)
```

---

### 4. Timer-Based Operations

```python
# Strategies can use timer events for periodic tasks
def register_event(self) -> None:
    self.event_engine.register(EVENT_TIMER, self.process_timer_event)

def process_timer_event(self, event: Event) -> None:
    # Called every 1 second
    self.timer_count += 1
    
    # Execute every 60 seconds
    if self.timer_count >= 60:
        self.timer_count = 0
        self.refresh_data()
```

**Common Timer Uses:**
- Heartbeat/keep-alive (Binance listen key)
- Periodic data refresh
- Risk checks
- PnL calculation

---

### 5. Custom Event Types

```python
# Define custom event type
EVENT_MY_STRATEGY = "eMyStrategy."

# Push custom event
event = Event(EVENT_MY_STRATEGY, data)
event_engine.put(event)

# Register handler
event_engine.register(EVENT_MY_STRATEGY, self.my_handler)

def my_handler(self, event: Event):
    data = event.data
    # Process custom event
```

---

## Performance Considerations

### Event Processing Bottlenecks

| Issue | Impact | Solution |
|-------|--------|----------|
| Slow handler | Blocks all events | Keep handlers fast, offload heavy work |
| High-frequency ticks | Queue buildup | Filter ticks, sample data |
| Synchronous callbacks | Strategy blocks others | Use ThreadPoolExecutor for init |
| Duplicate events | Wasted processing | Filter by vt_tradeid, vt_orderid |

### CTA Engine Optimizations

```python
# 1. Filter duplicate trade events
self.vt_tradeids: set = set()  # Track processed trades

def process_trade_event(self, event: Event) -> None:
    trade: TradeData = event.data
    if trade.vt_tradeid in self.vt_tradeids:
        return  # Skip duplicate
    self.vt_tradeids.add(trade.vt_tradeid)

# 2. Async strategy initialization
self.init_executor = ThreadPoolExecutor(max_workers=1)

def init_strategy(self, strategy_name: str) -> None:
    self.init_executor.submit(self._init_strategy, strategy_name)

# 3. Batch database writes
self.database.save_tick_data(batch_of_ticks)
```

---

## Debugging Event Flow

### 1. Enable Event Logging

```python
# In MainEngine or custom handler
def process_tick_event(self, event: Event) -> None:
    tick: TickData = event.data
    self.write_log(f"Tick received: {tick.vt_symbol} @ {tick.last_price}")
    # ...
```

### 2. Track Event Flow

```python
# Add general handler to log all events
def log_all_events(event: Event) -> None:
    print(f"Event: {event.type}, Data: {event.data}")

event_engine.register_general(log_all_events)
```

### 3. Monitor Queue Depth

```python
# Check event queue size
queue_size = event_engine._queue.qsize()
if queue_size > 1000:
    print(f"Warning: Event queue backing up ({queue_size})")
```

---

## Summary

| Component | Responsibility | Thread |
|-----------|---------------|--------|
| **Gateway** | External API, data ingestion | Gateway threads |
| **Event Engine** | Pub/sub, event distribution | Event thread |
| **OMS Engine** | State management, caching | Event thread |
| **CTA Engine** | Strategy execution | Event thread |
| **Log Engine** | Logging | Event thread |
| **Strategy** | Trading logic | Event thread (callbacks) |

**Event Flow:**
```
Gateway → Event Engine → [OMS, CTA, Log, UI, Recorder, ...]
```

**Key Design Principles:**
1. **Decoupling:** Gateways don't know about strategies
2. **Pub/Sub:** Producers/consumer independent
3. **Sequential:** Events processed in order (per type)
4. **Thread-safe:** Queue protects shared state
5. **Extensible:** Add handlers without modifying core
