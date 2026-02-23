# GUI & Web Integration in VeighNa

Analysis of how the graphical interfaces are integrated with the trading engine.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    VeighNa GUI Architecture                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────┐         ┌─────────────────────┐       │
│  │   Desktop GUI       │         │     Web GUI         │       │
│  │   (PySide6/Qt)      │         │   (FastAPI + Vue)   │       │
│  │   vnpy.trader.ui    │         │   vnpy_webtrader    │       │
│  └──────────┬──────────┘         └──────────┬──────────┘       │
│             │                                │                   │
│             │ Direct Python Call             │ RPC/WebSocket     │
│             │                                │                   │
│             └──────────────┬─────────────────┘                   │
│                            ↓                                     │
│                 ┌──────────────────────┐                        │
│                 │    MainEngine        │                        │
│                 │  (vnpy.trader.engine)│                        │
│                 │                      │                        │
│                 │  - OmsEngine         │                        │
│                 │  - CtaEngine         │                        │
│                 │  - AlgoEngine        │                        │
│                 │  - LogEngine         │                        │
│                 └──────────┬───────────┘                        │
│                            │                                     │
│                            ↓                                     │
│                 ┌──────────────────────┐                        │
│                 │    EventEngine       │                        │
│                 │  (Pub/Sub Queue)     │                        │
│                 └──────────┬───────────┘                        │
│                            │                                     │
│             ┌──────────────┼──────────────┐                     │
│             ↓              ↓              ↓                     │
│       ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│       │ Gateway  │  │ Gateway  │  │ Gateway  │                 │
│       │   CTP    │  │   IB     │  │ Binance  │                 │
│       └──────────┘  └──────────┘  └──────────┘                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Desktop GUI (PySide6/Qt)

### Integration: **Tightly Coupled**

**Location:** `vnpy/trader/ui/`

**Key Components:**

```python
# vnpy/trader/ui/__init__.py
from .qt import create_qapp
from .mainwindow import MainWindow

# Usage
qapp = create_qapp()
main_engine = MainEngine(event_engine)
main_window = MainWindow(main_engine, event_engine)
main_window.showMaximized()
qapp.exec()
```

### MainWindow Structure

```python
# vnpy/trader/ui/mainwindow.py
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        super().__init__()
        
        self.main_engine = main_engine    # ← Direct reference
        self.event_engine = event_engine  # ← Direct reference
        
        self.init_ui()
        
    def init_ui(self):
        # Create dock widgets
        self.trading_widget, trading_dock = self.create_dock(
            TradingWidget, "交易", LeftDockWidgetArea
        )
        self.order_widget, order_dock = self.create_dock(
            OrderMonitor, "委托", RightDockWidgetArea
        )
        self.position_widget, position_dock = self.create_dock(
            PositionMonitor, "持仓", BottomDockWidgetArea
        )
        # ... more widgets
        
    def create_dock(self, widget_class, title, area):
        """Create dock widget"""
        widget = widget_class(self.main_engine, self.event_engine)
        # ... dock setup
        return widget, dock
```

### Widget Integration Pattern

**All UI widgets receive direct references to engines:**

```python
# vnpy/trader/ui/widget.py
class TradingWidget(QtWidgets.QWidget):
    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        super().__init__()
        
        self.main_engine = main_engine    # ← Direct access
        self.event_engine = event_engine  # ← Direct access
        
        # Use engine directly
        self.send_order_button.clicked.connect(self.send_order)
        
    def send_order(self):
        """Send order via engine"""
        req = OrderRequest(...)
        vt_orderid = self.main_engine.send_order(req, gateway_name)
```

### Event Engine Integration

**UI widgets subscribe to events directly:**

```python
# vnpy/trader/ui/widget.py
class TickMonitor(QtWidgets.QTableWidget):
    def __init__(self, main_engine, event_engine):
        super().__init__()
        
        # Subscribe to tick events
        event_engine.register(EVENT_TICK, self.process_tick_event)
        
    def process_tick_event(self, event: Event):
        tick: TickData = event.data
        # Update UI with tick data
        self.update_row(tick)
```

### Desktop GUI Characteristics

| Aspect | Implementation |
|--------|----------------|
| **Coupling** | 🔴 Tight - Direct Python references |
| **Communication** | Direct method calls |
| **Event Handling** | Direct event engine subscription |
| **Threading** | Qt event loop + engine threads |
| **Deployment** | Single process, desktop only |

**Pros:**
- ✅ Fast (no serialization overhead)
- ✅ Simple (direct object references)
- ✅ Full access to all engine methods

**Cons:**
- ❌ Must run on same machine
- ❌ No remote access
- ❌ Single user only
- ❌ Python-only (tightly coupled)

---

## Web GUI (FastAPI + RPC)

### Integration: **Loosely Coupled via RPC**

**Location:** `vnpy_webtrader/`

**Architecture:**

```
┌─────────────────┐         ┌─────────────────┐
│   Web Browser   │         │  Desktop Client │
│   (Vue.js/JS)   │         │   (Python/RPC)  │
└────────┬────────┘         └────────┬────────┘
         │                           │
         │ HTTP/WebSocket            │ RPC (ZeroMQ)
         │                           │
         └──────────────┬────────────┘
                        ↓
              ┌──────────────────┐
              │  WebEngine       │
              │  (FastAPI app)   │
              │                  │
              │  - REST API      │
              │  - WebSocket     │
              │  - JWT Auth      │
              └────────┬─────────┘
                       │
                       │ RPC Client
                       ↓
              ┌──────────────────┐
              │  RpcServer       │
              │  (ZeroMQ)        │
              └────────┬─────────┘
                       │
                       ↓
              ┌──────────────────┐
              │  MainEngine      │
              │  (Trading Core)  │
              └──────────────────┘
```

### WebEngine Components

```python
# vnpy_webtrader/vnpy_webtrader/engine.py
class WebEngine(BaseEngine):
    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        super().__init__(main_engine, event_engine, APP_NAME)
        
        # RPC Server for client connections
        self.server = RpcServer()
        
        # Register engine methods
        self.init_server()
        self.register_event()
    
    def init_server(self):
        """Register RPC methods"""
        # Trading functions
        self.server.register(self.main_engine.connect)
        self.server.register(self.main_engine.subscribe)
        self.server.register(self.main_engine.send_order)
        self.server.register(self.main_engine.cancel_order)
        
        # Query functions
        self.server.register(self.main_engine.get_contract)
        self.server.register(self.main_engine.get_all_positions)
        self.server.register(self.main_engine.get_all_accounts)
        # ...
    
    def register_event(self):
        """Publish events to clients"""
        self.event_engine.register(EVENT_TICK, self.process_event)
        self.event_engine.register(EVENT_ORDER, self.process_event)
        self.event_engine.register(EVENT_TRADE, self.process_event)
        self.event_engine.register(EVENT_POSITION, self.process_event)
    
    def process_event(self, event: Event):
        """Forward event to RPC clients"""
        self.server.publish(event.type, event.data)
```

### Web API Layer

```python
# vnpy_webtrader/vnpy_webtrader/web.py
from fastapi import FastAPI, WebSocket, Depends
from jose import jwt

app = FastAPI()

# JWT Authentication
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm) -> dict:
    # Validate credentials
    access_token = create_access_token({"sub": username})
    return {"access_token": access_token}

# REST API for trading
@app.post("/order")
async def send_order(
    request: OrderRequest,
    token: str = Depends(get_access)  # JWT auth
):
    # Call RPC server
    vt_orderid = rpc_client.send_order(
        symbol=request.symbol,
        exchange=request.exchange,
        direction=request.direction,
        ...
    )
    return {"vt_orderid": vt_orderid}

# WebSocket for real-time data
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Subscribe to events
    def on_event(event):
        data = to_dict(event.data)
        asyncio.run(websocket.send_json(data))
    
    rpc_client.subscribe(on_event)
    
    try:
        while True:
            # Keep connection alive
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        rpc_client.unsubscribe(on_event)
```

### RPC Client (Bridge)

```python
# vnpy_webtrader/vnpy_webtrader/web.py
from vnpy.rpc import RpcClient

class TradingRpcClient(RpcClient):
    """RPC client for web server"""
    
    def __init__(self):
        super().__init__()
        self.callbacks = {}
    
    def subscribe(self, callback):
        """Subscribe to events"""
        self.callback = callback
    
    def callback(self, topic, data):
        """Called when event received from server"""
        # Forward to WebSocket clients
        for ws in self.websockets:
            ws.send_json({"type": topic, "data": data})
    
    # Proxy methods
    def send_order(self, **kwargs):
        return self.send("send_order", kwargs)
    
    def cancel_order(self, **kwargs):
        return self.send("cancel_order", kwargs)
    
    def get_all_positions(self):
        return self.send("get_all_positions")
```

### Web GUI Characteristics

| Aspect | Implementation |
|--------|----------------|
| **Coupling** | 🟢 Loose - RPC separation |
| **Communication** | HTTP REST + WebSocket |
| **Event Handling** | WebSocket push |
| **Threading** | AsyncIO + FastAPI |
| **Deployment** | Client-server architecture |

**Pros:**
- ✅ Remote access (any browser)
- ✅ Multi-user support
- ✅ Platform independent
- ✅ Can run server separately

**Cons:**
- ❌ More complex setup
- ❌ Network latency
- ❌ Serialization overhead
- ❌ Requires RPC server running

---

## Comparison: Desktop vs Web GUI

| Feature | Desktop GUI | Web GUI |
|---------|-------------|---------|
| **Technology** | PySide6 (Qt) | FastAPI + WebSocket |
| **Integration** | Direct Python | RPC (ZeroMQ) |
| **Access** | Local only | Remote (browser) |
| **Users** | Single | Multi-user |
| **Latency** | Low (direct) | Medium (network) |
| **Deployment** | Simple | Complex |
| **Auth** | None | JWT tokens |
| **Real-time** | Event engine | WebSocket |

---

## How Tightly Integrated?

### Desktop GUI: **Very Tight**

```python
# Can directly access ANY engine method
main_window.main_engine.get_all_positions()
main_window.event_engine.register(EVENT_TICK, handler)

# Can call internal methods
main_window.trading_widget.some_internal_method()

# No serialization, no network, direct memory access
```

**Implications:**
- ✅ Fast, no overhead
- ✅ Full access to everything
- ❌ Can't separate processes
- ❌ Can't run remotely
- ❌ Python-only (no other language)

### Web GUI: **Loose**

```python
# Only exposed RPC methods available
rpc_client.send_order(...)  # ← Only registered methods
rpc_client.get_all_positions()

# Events pushed via WebSocket
websocket.send_json({"type": "eTick.", "data": {...}})

# JSON serialization, network transport
```

**Implications:**
- ✅ Process separation
- ✅ Remote access
- ✅ Multi-language clients possible
- ❌ Only exposed methods accessible
- ❌ Serialization overhead

---

## Can You Use Engine Without GUI?

### Yes! **Both GUIs are optional.**

**Headless Mode (No GUI):**

```python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy_ctp import CtpGateway
from vnpy_ctastrategy import CtaStrategyApp

# Just engines, no GUI
event_engine = EventEngine()
main_engine = MainEngine(event_engine)

# Add gateway and apps
main_engine.add_gateway(CtpGateway)
main_engine.add_app(CtaStrategyApp)

# Run strategies without any GUI
# Can run as service/daemon
```

**Custom GUI:**

```python
# Build your own UI
from vnpy.trader.engine import MainEngine

class MyCustomUI:
    def __init__(self, main_engine):
        self.main_engine = main_engine
        
    def on_button_click(self):
        # Use engine directly
        self.main_engine.send_order(...)
```

**Web/Mobile App:**

```python
# Use WebEngine as backend
from vnpy_webtrader import WebEngine

main_engine.add_engine(WebEngine)

# Build custom frontend (React, Vue, mobile app)
# Connect via REST/WebSocket
```

---

## Extension Points

### 1. Custom Desktop Widgets

```python
# vnpy/trader/ui/widget.py
from vnpy.trader.ui import QtWidgets
from vnpy.trader.engine import MainEngine, EventEngine

class MyCustomWidget(QtWidgets.QWidget):
    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        super().__init__()
        
        self.main_engine = main_engine
        self.event_engine = event_engine
        
        # Build UI
        self.init_ui()
        
        # Subscribe to events
        event_engine.register(EVENT_TICK, self.process_tick)
    
    def process_tick(self, event: Event):
        # Update UI
        pass
```

### 2. Custom Web API Endpoints

```python
# Add to vnpy_webtrader/web.py

@app.get("/api/strategy/status")
async def get_strategy_status(token: str = Depends(get_access)):
    """Custom API endpoint"""
    positions = rpc_client.get_all_positions()
    return {"positions": positions}

@app.post("/api/strategy/start")
async def start_strategy(
    name: str,
    token: str = Depends(get_access)
):
    """Start strategy"""
    result = rpc_client.call("start_strategy", name)
    return {"result": result}
```

### 3. Custom RPC Methods

```python
# In WebEngine
class WebEngine(BaseEngine):
    def init_server(self):
        # Register custom methods
        self.server.register(self.my_custom_function)
    
    def my_custom_function(self, param1, param2):
        # Custom logic
        return result
```

---

## Summary

| Question | Answer |
|----------|--------|
| **Is GUI required?** | ❌ No, engines work standalone |
| **Can I use custom GUI?** | ✅ Yes, just need MainEngine reference |
| **Can I use web without desktop?** | ⚠️ No, Web GUI needs RPC server (which needs desktop process) |
| **How tight is desktop integration?** | 🔴 Very tight - direct Python references |
| **How tight is web integration?** | 🟢 Loose - RPC separation |
| **Can I build mobile app?** | ✅ Yes, use WebEngine REST/WebSocket API |
| **Can I run headless?** | ✅ Yes, engines work without any GUI |

**Architecture Quality:**

- ✅ **Modular** - GUI is separate layer
- ✅ **Flexible** - Can swap/extend GUIs
- ✅ **Testable** - Engines work without GUI
- ⚠️ **Desktop coupling** - Too tight for some use cases
- ✅ **Web decoupling** - Good separation of concerns
