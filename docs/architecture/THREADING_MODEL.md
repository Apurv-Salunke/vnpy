# VeighNa Threading Model

Detailed explanation of the threading architecture in VeighNa.

---

## Thread Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         VeighNa Threads                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Main Thread (Qt GUI Event Loop)                             │
│  2. Event Thread (Event Processing)                             │
│  3. Timer Thread (1Hz Heartbeat)                                │
│  4. Gateway Threads (Network I/O, multiple)                     │
│  5. Database Threads (Async I/O)                                │
│  6. RPC Threads (ZeroMQ, multiple)                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Main Thread (Qt GUI)

**Purpose:** GUI event loop and user interactions.

**Responsibilities:**
- Qt widget event processing
- User input handling (button clicks, menu selections)
- UI updates from engine events
- Exception handling for UI thread

**Code:**
```python
from vnpy.trader.ui import MainWindow, create_qapp

def main():
    qapp = create_qapp()  # Creates QApplication
    
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    
    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()
    
    qapp.exec()  # Main thread event loop
```

**Characteristics:**
- **Priority:** Normal
- **Blocking:** Yes (blocked during long operations)
- **Thread-safe:** Qt widgets must be accessed from this thread only

---

## 2. Event Thread

**Purpose:** Process ALL events from queue sequentially.

**Responsibilities:**
- Get events from queue
- Distribute to registered handlers
- Maintain event ordering (FIFO)

**Code:**
```python
class EventEngine:
    def _run(self) -> None:
        """Event processing loop"""
        while self._active:
            try:
                event: Event = self._queue.get(block=True, timeout=1)
                self._process(event)
            except Empty:
                pass
    
    def _process(self, event: Event) -> None:
        """Distribute event to handlers"""
        # Call type-specific handlers
        if event.type in self._handlers:
            [handler(event) for handler in self._handlers[event.type]]
        
        # Call general handlers
        if self._general_handlers:
            [handler(event) for handler in self._general_handlers]
```

**Characteristics:**
- **Priority:** High (time-critical)
- **Blocking:** No (must process events quickly)
- **Thread-safe:** All event handlers run in this thread (no concurrent access)

**Why Single Thread?**
```
┌─────────────────────────────────────────────────────────────────┐
│ Single Thread Benefits:                                         │
│                                                                  │
│ 1. Deterministic Ordering                                       │
│    Tick 1 → Tick 2 → Tick 3 (always this order)                │
│                                                                  │
│ 2. No Race Conditions                                           │
│    Strategy logic doesn't need locks                            │
│                                                                  │
│ 3. Easier Debugging                                             │
│    Event flow is predictable and traceable                      │
│                                                                  │
│ 4. Backtest Compatibility                                       │
│    Same event flow works for live and backtest                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Timer Thread

**Purpose:** Generate 1Hz timer events.

**Responsibilities:**
- Sleep for 1 second intervals
- Generate `EVENT_TIMER` events
- Provide heartbeat for time-based operations

**Code:**
```python
class EventEngine:
    def _run_timer(self) -> None:
        """Timer generation loop"""
        while self._active:
            sleep(self._interval)  # 1 second
            event: Event = Event(EVENT_TIMER)
            self.put(event)
```

**Characteristics:**
- **Priority:** Low (best effort)
- **Blocking:** Yes (blocks on sleep)
- **Independent:** Doesn't block event processing

**Use Cases:**
```python
# Algo slicing (TWAP)
def on_timer(self):
    self.timer_count += 1
    if self.timer_count >= self.interval:  # Every 60 seconds
        self.send_slice_order()
        self.timer_count = 0

# Keep-alive (Binance listen key)
def on_timer(self):
    self.keep_alive_count += 1
    if self.keep_alive_count >= 600:  # Every 10 minutes
        self.rest_api.keep_user_stream()
        self.keep_alive_count = 0

# Risk checks
def on_timer(self):
    self.check_position_limits()
    self.check_order_frequency()
```

---

## 4. Gateway Threads

**Purpose:** Network I/O for each gateway.

**Responsibilities:**
- Connect to exchange/broker APIs
- Receive callbacks from external APIs
- Convert external data to VeighNa format
- Push events to Event Engine

**Characteristics:**
- **Priority:** High (don't block network I/O)
- **Multiple:** One thread per gateway (CTP, IB, Binance, etc.)
- **Asynchronous:** Network callbacks are non-blocking

**Example (CTP Gateway):**
```python
class CtpGateway(BaseGateway):
    def connect(self, setting: dict) -> None:
        # CTP API runs in its own thread
        self.api.registerFront()
        self.api.init()  # Non-blocking, returns immediately
        
    def OnFrontConnected(self):
        """Callback from CTP thread"""
        # This runs in CTP's thread, not Event Thread
        self.write_log("Connection established")
        
    def OnRtnDepthMarketData(self, data: dict):
        """Tick callback from CTP thread"""
        tick = self._parse_tick(data)
        self.on_tick(tick)  # Pushes to Event Engine queue
```

**Thread Communication:**
```
┌─────────────────┐         ┌─────────────────┐
│  CTP Thread     │         │  Event Thread   │
│                 │         │                 │
│  on_tick(tick)  │─────→   │  event_queue    │
│                 │  put()  │                 │
│                 │         │  _process()     │
│                 │         │                 │
└─────────────────┘         └─────────────────┘
```

---

## 5. Database Threads

**Purpose:** Async database writes.

**Responsibilities:**
- Batch write market data
- Query historical data
- Manage database connections

**Characteristics:**
- **Priority:** Low (background)
- **Blocking:** Yes (database I/O can be slow)
- **Pooled:** Uses connection pooling

**Example:**
```python
class SqliteDatabase(BaseDatabase):
    def save_bar_data(self, bars: list[BarData], stream: bool = True) -> bool:
        """Save bar data asynchronously"""
        if stream:
            # Run in background thread
            executor.submit(self._save_bars, bars)
            return True
        else:
            # Run synchronously
            return self._save_bars(bars)
```

---

## 6. RPC Threads

**Purpose:** ZeroMQ communication for distributed systems.

**Responsibilities:**
- REQ/REP pattern (request/response)
- PUB/SUB pattern (publish/subscribe)
- Cross-process communication

**Characteristics:**
- **Priority:** Normal
- **Multiple:** Separate threads for REQ and SUB sockets
- **Non-blocking:** Uses ZeroMQ async I/O

**Example:**
```python
class RpcServer:
    def __init__(self):
        self.context = zmq.Context()
        
        # REP socket (request/response)
        self.socket_rep = self.context.socket(zmq.REP)
        self.socket_rep.bind(rep_address)
        
        # PUB socket (publish/subscribe)
        self.socket_pub = self.context.socket(zmq.PUB)
        self.socket_pub.bind(pub_address)
        
        # Start threads
        self.thread_rep = Thread(target=self.run_rep)
        self.thread_sub = Thread(target=self.run_pub)
        
    def run_rep(self):
        """Request/response thread"""
        while self.active:
            req = self.socket_rep.recv()
            result = self.process(req)
            self.socket_rep.send(result)
    
    def run_pub(self):
        """Publish thread"""
        while self.active:
            event = self.queue.get()
            self.socket_pub.send(event)
```

---

## Thread Communication Patterns

### 1. Gateway → Event Engine (Producer → Consumer)

```
┌─────────────────┐         ┌─────────────────┐
│  Gateway Thread │         │  Event Thread   │
│                 │         │                 │
│  on_tick()      │         │  process_tick() │
│      ↓          │         │      ↑          │
│  event = Event  │         │  handler(event) │
│      ↓          │   put() │      ↑          │
│  queue.put()    │ ──────→ │  queue.get()    │
│                 │         │                 │
└─────────────────┘         └─────────────────┘
```

### 2. Event Engine → Engine (Pub/Sub)

```
┌─────────────────┐
│  Event Thread   │
│                 │
│  for handler in handlers[EVENT_TICK]:
│      handler(event)
│         │
│         ├──────────────┬──────────────┬──────────────┐
│         ↓              ↓              ↓              ↓
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  │OmsEngine │  │CtaEngine │  │LogEngine │  │  UI      │
│  │          │  │          │  │          │  │ Monitor  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘
└─────────────────┘
```

### 3. Engine → Gateway (Request/Response)

```
┌─────────────────┐         ┌─────────────────┐
│  CtaEngine      │         │  Gateway Thread │
│                 │         │                 │
│  send_order()   │ ──────→ │  send_order()   │
│                 │         │      ↓          │
│                 │         │  api.ReqOrder() │
│                 │         │      ↓          │
│  vt_orderid     │ ←────── │  return orderid │
│                 │         │                 │
└─────────────────┘         └─────────────────┘
```

---

## Thread Safety Considerations

### What IS Thread-Safe

1. **Event Queue** - `queue.Queue` is thread-safe
   ```python
   # Gateway thread can safely put events
   self.event_engine.put(event)
   ```

2. **Event Distribution** - Handlers are called sequentially
   ```python
   # No concurrent access in event handlers
   def process_tick_event(self, event):
       tick = event.data
       self.ticks[tick.vt_symbol] = tick  # Safe, no lock needed
   ```

3. **Read-only Operations** - Query methods are safe
   ```python
   # Safe to call from UI thread
   tick = main_engine.get_tick("RB2401")
   ```

### What IS NOT Thread-Safe

1. **Qt Widgets** - Must be accessed from Main Thread
   ```python
   # WRONG: Don't update UI from Event Thread
   def process_tick_event(self, event):
       self.widget.update_price(tick.last_price)  # Crash!
   
   # RIGHT: Qt handles this via signals/slots
   ```

2. **Shared Mutable State** - Use Event Engine for communication
   ```python
   # WRONG: Don't share state between threads
   gateway.some_value = 123  # Gateway thread
   engine.read_value()       # Event thread - RACE CONDITION!
   
   # RIGHT: Use events
   gateway.on_event(EVENT_CUSTOM, data)  # Gateway thread
   engine.process_custom_event(event)    # Event thread
   ```

---

## Performance Characteristics

### Latency Breakdown

| Operation | Latency | Notes |
|-----------|---------|-------|
| Event queue put/get | ~10μs | Queue overhead |
| Event distribution | ~50μs | Handler dispatch |
| Gateway network I/O | 1-100ms | Exchange dependent |
| Database write | 1-10ms | Batch dependent |
| RPC call | 100μs-10ms | Network dependent |

### Throughput Limits

| Component | Max Throughput | Bottleneck |
|-----------|---------------|------------|
| Event Thread | ~10,000 events/sec | Single-threaded |
| Gateway | ~1,000 ticks/sec | Network/API |
| Database | ~100,000 bars/sec | Disk I/O |
| RPC | ~10,000 msgs/sec | Network |

---

## Best Practices

### 1. Keep Event Handlers Fast

```python
# GOOD: Fast handler
def process_tick_event(self, event):
    tick = event.data
    self.ticks[tick.vt_symbol] = tick  # Cache update only

# BAD: Slow handler
def process_tick_event(self, event):
    tick = event.data
    self.database.save_tick(tick)  # Don't do I/O in event handler!
    self.strategy.calculate_indicators()  # Don't do heavy computation!
```

### 2. Use Timer for Periodic Operations

```python
# GOOD: Use timer
def on_timer(self):
    if self.timer_count >= 60:
        self.send_heartbeat()
        self.timer_count = 0

# BAD: Don't use sleep in event handlers
def process_tick_event(self, event):
    time.sleep(1)  # Blocks all event processing!
```

### 3. Don't Block Gateway Threads

```python
# GOOD: Non-blocking
def connect(self, setting):
    self.api.init()  # Returns immediately, callbacks later

# BAD: Blocking
def connect(self, setting):
    while not self.connected:
        time.sleep(0.1)  # Blocks gateway thread!
```

### 4. Use Event Engine for Cross-Thread Communication

```python
# GOOD: Event-based
gateway.on_tick(tick)  # Pushes to queue

# BAD: Direct call
engine.process_tick(tick)  # Called from gateway thread - RACE!
```

---

## Debugging Tips

### 1. Check Thread Names

```python
import threading
print(f"Current thread: {threading.current_thread().name}")

# Expected:
# MainThread - GUI operations
# Thread-1 - Event processing
# Thread-2 - Timer
# Thread-3,4,5... - Gateway threads
```

### 2. Log Event Flow

```python
def process_tick_event(self, event):
    tick = event.data
    self.write_log(f"Tick received: {tick.vt_symbol} @ {tick.last_price}")
    # Check log timestamps to verify ordering
```

### 3. Monitor Queue Depth

```python
queue_size = event_engine._queue.qsize()
if queue_size > 1000:
    print(f"Warning: Event queue backing up ({queue_size})")
```

---

## Summary

| Thread | Purpose | Priority | Blocking |
|--------|---------|----------|----------|
| **Main** | Qt GUI | Normal | Yes |
| **Event** | Process events | High | No |
| **Timer** | 1Hz heartbeat | Low | Yes (sleep) |
| **Gateway** | Network I/O | High | No (async) |
| **Database** | Async writes | Low | Yes |
| **RPC** | ZeroMQ | Normal | No (async) |

**Key Design Principle:**
> **Minimum Viable Concurrency** - Use the fewest threads necessary to achieve required behavior. This ensures deterministic event ordering and eliminates race conditions in strategy logic.
