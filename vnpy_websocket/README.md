# Websocket Client for VeighNa

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-1.0.0-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg" />
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

## Description

Async Websocket API client based on asyncio and aiohttp, used for developing high-performance real-time market data and trading interfaces.

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

**Install via pip:**
```bash
pip install vnpy_websocket
```

**Install from source:**
```bash
# Download and extract source code
cd vnpy_websocket
pip install .
```

## Features

- **Async IO:** High-performance async websocket connection
- **Auto Reconnect:** Automatic reconnection on disconnection
- **Heartbeat:** Built-in heartbeat mechanism
- **Subscription Management:** Subscribe/unsubscribe topics
- **Error Handling:** Automatic error recovery

## Usage Example

```python
from vnpy_websocket import WebsocketClient

class MyWebsocketClient(WebsocketClient):
    def __init__(self):
        super().__init__()
        
    def on_connected(self):
        """Connection established"""
        print("Connected to server")
        
    def on_disconnected(self):
        """Connection lost"""
        print("Disconnected from server")
        
    def on_packet(self, packet: dict):
        """Receive data packet"""
        print(f"Received: {packet}")
        
    def on_error(self, exception_type: type, exception_value: Exception, tb):
        """Error occurred"""
        print(f"Error: {exception_type}, {exception_value}")
    
    def subscribe(self, topic: str):
        """Subscribe to topic"""
        req = {"op": "subscribe", "topic": topic}
        self.send_packet(req)

# Usage
ws = MyWebsocketClient()
ws.start("wss://ws.example.com/market")
ws.subscribe("ticker.BTCUSDT")
```

## Key Methods

### WebsocketClient

| Method | Description |
|--------|-------------|
| `start(url, proxy_host, proxy_port)` | Start websocket connection |
| `stop()` | Stop connection |
| `send_packet(packet: dict)` | Send data packet |
| `subscribe(topic)` | Subscribe to topic |
| `unsubscribe(topic)` | Unsubscribe from topic |

### Callbacks

| Callback | Trigger |
|----------|---------|
| `on_connected()` | Connection established |
| `on_disconnected()` | Connection lost |
| `on_packet(packet)` | Data received |
| `on_error(exception)` | Error occurred |

## Features

### Auto Reconnect

Automatically reconnects when connection is lost:
```python
def on_disconnected(self):
    """Auto reconnect after 5 seconds"""
    import threading
    threading.Timer(5.0, self.start).start()
```

### Heartbeat

Sends heartbeat every 30 seconds by default:
```python
def send_heartbeat(self):
    """Send heartbeat packet"""
    self.send_packet({"op": "ping"})
```

### Subscription Management

Manage subscriptions with automatic resend on reconnect:
```python
def on_connected(self):
    """Resubscribe after reconnection"""
    for topic in self.topics:
        self.subscribe(topic)
```

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_websocket
