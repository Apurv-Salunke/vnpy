# VeighNa Gateway Architecture Analysis

This document analyzes the architecture of VeighNa gateway extensions using **Binance** and **Interactive Brokers (IB)** gateways as examples.

---

## Repository Structure

Both gateways follow the same standard structure:

```
vnpy_<name>/
├── vnpy_<name>/
│   ├── __init__.py          # Package exports
│   └── <name>_gateway.py    # Main gateway implementation
├── script/                   # Example startup scripts
├── pyproject.toml           # Package configuration
├── README.md                # Documentation
└── LICENSE                  # MIT License
```

---

## Core Architecture Pattern

All gateways inherit from `BaseGateway` and follow this pattern:

```
┌─────────────────────────────────────────────────────┐
│                   BaseGateway                        │
│  (vnpy.trader.gateway - defines interface contract) │
└─────────────────────────────────────────────────────┘
                          ↑
        ┌─────────────────┴─────────────────┐
        │                                   │
┌───────────────────┐              ┌───────────────────┐
│ BinanceLinearGateway │              │     IbGateway      │
│  (vnpy_binance)    │              │    (vnpy_ib)      │
└───────────────────┘              └───────────────────┘
```

---

## Gateway Components

### 1. Main Gateway Class

**Purpose:** Acts as the bridge between external API and VeighNa framework

**Common Interface (required methods):**

| Method | Purpose |
|--------|---------|
| `connect(setting)` | Establish connection with credentials |
| `subscribe(req)` | Subscribe to market data |
| `send_order(req)` | Send new order |
| `cancel_order(req)` | Cancel existing order |
| `query_account()` | Query account balance |
| `query_position()` | Query positions |
| `query_history(req)` | Query historical data |
| `close()` | Close connection |

**Binance Example:**
```python
class BinanceLinearGateway(BaseGateway):
    default_name: str = "BINANCE_LINEAR"
    
    default_setting: dict = {
        "API Key": "",
        "API Secret": "",
        "Server": ["REAL", "TESTNET"],
        "Proxy Host": "",
        "Proxy Port": 0
    }
    
    def __init__(self, event_engine: EventEngine, gateway_name: str):
        super().__init__(event_engine, gateway_name)
        
        # Compose multiple API clients
        self.trade_api = TradeApi(self)      # Order execution
        self.user_api = UserApi(self)        # User data stream
        self.md_api = MdApi(self)            # Market data
        self.rest_api = RestApi(self)        # REST queries
        
        self.orders = {}
        self.symbol_contract_map = {}
```

**IB Example:**
```python
class IbGateway(BaseGateway):
    default_name: str = "IB"
    
    default_setting: dict = {
        "TWS Address": "127.0.0.1",
        "TWS Port": 7497,
        "Client ID": 1,
        "Trading Account": ""
    }
    
    def __init__(self, event_engine: EventEngine, gateway_name: str):
        super().__init__(event_engine, gateway_name)
        
        # Single API wrapper (IB provides unified SDK)
        self.api = IbApi(self)
```

---

### 2. API Client Layers

Gateways decompose into multiple API clients based on functionality:

#### Binance Architecture (4 components)

```
┌──────────────────────────────────────────────────────────┐
│               BinanceLinearGateway                        │
├──────────────────────────────────────────────────────────┤
│  RestApi    │  TradeApi    │  UserApi    │  MdApi        │
│  (REST)     │  (Websocket) │  (Websocket)│  (Websocket)  │
│  - Query    │  - Orders    │  - Account  │  - Ticks      │
│  - History  │  - Cancel    │  - Position │  - K-lines    │
└──────────────────────────────────────────────────────────┘
```

| Component | Base Class | Purpose |
|-----------|-----------|---------|
| `RestApi` | `RestClient` | HTTP requests (queries, signed requests) |
| `TradeApi` | `WebsocketClient` | Order execution via websocket |
| `UserApi` | `WebsocketClient` | Account/position updates via websocket |
| `MdApi` | `WebsocketClient` | Market data streaming |

**Key Implementation - RestApi:**
```python
class RestApi(RestClient):
    def sign(self, request: Request) -> Request:
        """Sign REST requests with HMAC-SHA256"""
        timestamp = int(time.time() * 1000)
        query = urllib.parse.urlencode(sorted(request.params.items()))
        signature = hmac.new(
            self.secret,
            query.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        
        request.headers = {"X-MBX-APIKEY": self.key}
        return request
```

#### IB Architecture (1 unified component)

```
┌──────────────────────────────────────────────────────────┐
│                   IbGateway                               │
├──────────────────────────────────────────────────────────┤
│                    IbApi                                  │
│         (wraps ibapi.EClient + ibapi.EWrapper)           │
│  - Market Data  - Orders  - Accounts  - History          │
└──────────────────────────────────────────────────────────┘
```

**Key Implementation - IbApi:**
```python
class IbApi(EWrapper):
    """Wraps IB's EClient and EWrapper"""
    
    def __init__(self, gateway: IbGateway):
        super().__init__()
        self.client = EClient(self)  # IB's REST-like client
        
    def connect(self, host: str, port: int, clientid: int, account: str):
        """Connect to TWS/Gateway"""
        self.client.eConnect(host, port, clientid)
```

---

### 3. Data Mapping Tables

Both gateways define constant mappings for data conversion:

**Binance:**
```python
STATUS_BINANCE2VT = {
    "NEW": Status.NOTTRADED,
    "PARTIALLY_FILLED": Status.PARTTRADED,
    "FILLED": Status.ALLTRADED,
    "CANCELED": Status.CANCELLED,
}

DIRECTION_VT2BINANCE = {
    Direction.LONG: "BUY",
    Direction.SHORT: "SELL"
}

ORDERTYPE_VT2BINANCE = {
    OrderType.LIMIT: ("LIMIT", "GTC"),
    OrderType.MARKET: ("MARKET", "GTC"),
}
```

**IB:**
```python
STATUS_IB2VT = {
    "ApiPending": Status.SUBMITTING,
    "Submitted": Status.NOTTRADED,
    "Filled": Status.ALLTRADED,
    "Cancelled": Status.CANCELLED,
}

PRODUCT_IB2VT = {
    "STK": Product.EQUITY,
    "CASH": Product.FOREX,
    "FUT": Product.FUTURES,
    "OPT": Product.OPTION,
}
```

---

### 4. Data Object Conversion

**Binance - Tick Data:**
```python
def on_tick_message(self, data: dict):
    tick = TickData(
        symbol=contract.symbol,
        exchange=Exchange.GLOBAL,
        datetime=datetime.now(UTC_TZ),
        name=contract.name,
        last_price=float(data["p"]),
        volume=float(data["v"]),
        bid_price_1=float(data["b"]),
        ask_price_1=float(data["a"]),
        bid_volume_1=float(data["B"]),
        ask_volume_1=float(data["A"]),
        gateway_name=self.gateway_name
    )
    self.gateway.on_tick(tick)
```

**IB - Tick Data:**
```python
def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
    tick = self.ticks.get(reqId)
    if not tick:
        return
    
    field = TICKFIELD_IB2VT.get(tickType)
    if field:
        setattr(tick, field, price)
    
    self.gateway.on_tick(copy(tick))
```

---

### 5. Event Engine Integration

Gateways push data to VeighNa via event engine:

```python
# In BaseGateway (parent class)
def on_tick(self, tick: TickData):
    """Push tick data to event engine"""
    event = Event(EVENT_TICK, tick)
    self.event_engine.put(event)

def on_order(self, order: OrderData):
    """Push order update to event engine"""
    event = Event(EVENT_ORDER, order)
    self.event_engine.put(event)

def on_trade(self, trade: TradeData):
    """Push trade data to event engine"""
    event = Event(EVENT_TRADE, trade)
    self.event_engine.put(event)
```

---

## Key Differences

| Aspect | Binance Gateway | IB Gateway |
|--------|----------------|------------|
| **API Type** | REST + Websocket | TWS SDK (EClient/EWrapper) |
| **Authentication** | HMAC-SHA256 signature | TWS/Gateway login |
| **Connection** | Multiple websocket streams | Single TCP connection |
| **Contract Format** | Simple symbol (BTCUSDT) | Complex string format or ConId |
| **Asset Classes** | Crypto (spot, futures) | Stocks, Forex, Futures, Options |
| **Complexity** | ~1,650 lines | ~1,220 lines |

---

## Common Patterns

### 1. Request-Response Pattern (REST)
```python
def query_account(self):
    path = "/fapi/v3/account"
    self.add_request(
        method="GET",
        path=path,
        callback=self.on_query_account
    )

def on_query_account(self, data: dict, request: Request):
    # Process response
    account = AccountData(...)
    self.gateway.on_account(account)
```

### 2. Subscription Pattern (Websocket)
```python
def subscribe(self, req: SubscribeRequest):
    self.subscribed[req.vt_symbol] = req
    
    # Send subscription message
    params = {"method": "SUBSCRIBE", "params": ["btcusdt@trade"]}
    self.send_packet(params)
```

### 3. Order Management Pattern
```python
def send_order(self, req: OrderRequest):
    # Generate unique order ID
    orderid = f"{self.order_prefix}_{self.orderid}"
    self.orderid += 1
    
    # Send to exchange
    self._send_order(req, orderid)
    
    return orderid  # Return to caller
```

---

## Extension Development Checklist

To create a new gateway:

1. **Inherit BaseGateway**
   - Implement all required methods
   - Define `default_name` and `default_setting`

2. **Create API Clients**
   - REST client for queries (if needed)
   - Websocket/TCP client for real-time data
   - Handle authentication

3. **Define Mappings**
   - Status, Direction, OrderType, Product, Exchange

4. **Implement Data Conversion**
   - TickData, BarData, OrderData, TradeData, PositionData, AccountData, ContractData

5. **Event Publishing**
   - Use `self.gateway.on_tick()`, `on_order()`, etc.

6. **Error Handling**
   - Connection errors
   - API errors
   - Reconnection logic

---

## Files to Study

For deep understanding, read in this order:

### Binance Gateway
1. `vnpy_binance/__init__.py` - Package exports
2. `vnpy_binance/linear_gateway.py` - Lines 1-300 (BinanceLinearGateway class)
3. `vnpy_binance/linear_gateway.py` - Lines 300-600 (RestApi class)
4. `vnpy_binance/linear_gateway.py` - Lines 600+ (Websocket APIs)

### IB Gateway
1. `vnpy_ib/__init__.py` - Package exports
2. `vnpy_ib/ib_gateway.py` - Lines 1-250 (IbGateway + IbApi init)
3. `vnpy_ib/ib_gateway.py` - Lines 250-600 (Market data callbacks)
4. `vnpy_ib/ib_gateway.py` - Lines 600+ (Order/account callbacks)

---

## Resources

- **BaseGateway:** `/Users/apurv/Desktop/algo-trading/vnpy/vnpy/trader/gateway.py`
- **Data Objects:** `/Users/apurv/Desktop/algo-trading/vnpy/vnpy/trader/object.py`
- **Event Engine:** `/Users/apurv/Desktop/algo-trading/vnpy/vnpy/event/engine.py`
- **REST Client:** `/Users/apurv/Desktop/algo-trading/vnpy/vnpy_rest/`
- **Websocket Client:** `/Users/apurv/Desktop/algo-trading/vnpy/vnpy_websocket/`
