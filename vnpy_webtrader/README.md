# Web Trader Module for VeighNa

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-1.1.0-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg" />
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

## Description

Web service application module designed for B-S (Browser-Server) architecture. Implements a web server providing active function calls (REST) and passive data push (Websocket).

Currently provides basic trading and management interfaces. Users can extend web interfaces for other VeighNa application modules (such as CTA strategy auto-trading) according to their needs.

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

**Install via pip:**
```bash
pip install vnpy_webtrader
```

**Install from source:**
```bash
# Download and extract source code
cd vnpy_webtrader
pip install .
```

## Architecture

### REST API (Active Function Calls)

Based on FastAPI-RESTful implementation:

1. User clicks a button in browser, initiates RESTful call
2. Web server receives RESTful request, converts to RPC call and sends to trading server
3. Trading server receives RPC request, executes function logic, returns result
4. Web server returns RESTful response to browser

### WebSocket (Passive Data Push)

Based on FastAPI-WebSocket implementation:

1. Trading server's event engine forwards event push to RPC client (web server)
2. Web server receives event push, converts to JSON format, sends via WebSocket
3. Browser receives push data via WebSocket, renders in web frontend

### Two-Process Design

Reasons for separating into two processes:

1. **Performance:** Trading server runs strategies and calculations requiring low latency
2. **Security:** Web server faces internet access, separating trading logic improves security

## Usage

### Start Trading Server

```python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

from vnpy_ctp import CtpGateway
from vnpy_webtrader import WebTraderApp

def main():
    qapp = create_qapp()
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    
    main_engine.add_gateway(CtpGateway)
    main_engine.add_app(WebTraderApp)
    
    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()
    qapp.exec()

if __name__ == "__main__":
    main()
```

### Access Web Interface

1. Open browser
2. Navigate to `http://localhost:8000`
3. Login with credentials
4. Use web interface for trading

## API Endpoints

### REST APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/token` | POST | Get access token |
| `/order` | POST | Send order |
| `/cancel` | POST | Cancel order |
| `/position` | GET | Get positions |
| `/account` | GET | Get account |

### WebSocket

| Topic | Description |
|-------|-------------|
| `tick` | Tick data push |
| `trade` | Trade fill push |
| `order` | Order update push |
| `position` | Position update push |

## Configuration

Edit `web_trader_setting.json`:

```json
{
    "username": "admin",
    "password": "your_password",
    "req_address": "tcp://localhost:2014",
    "sub_address": "tcp://localhost:4102"
}
```

## Extending Web Interfaces

Add custom endpoints in `web.py`:

```python
@app.get("/api/strategy/start")
async def start_strategy(
    strategy_name: str,
    token: str = Depends(get_access)
):
    """Start CTA strategy"""
    result = rpc_client.call("start_strategy", strategy_name)
    return {"result": result}
```

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_webtrader
