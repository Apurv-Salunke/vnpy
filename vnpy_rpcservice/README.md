# RPC Service for VeighNa

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

RPC (Remote Procedure Call) service module for VeighNa. Used for inter-process communication to build distributed trading systems. Supports both REQ/REP (request/response) and PUB/SUB (publish/subscribe) patterns.

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

**Install via pip:**
```bash
pip install vnpy_rpcservice
```

**Install from source:**
```bash
# Download and extract source code
cd vnpy_rpcservice
pip install .
```

## Architecture

```
┌─────────────────┐         ┌─────────────────┐
│  RPC Client     │         │  RPC Client     │
│  (Python)       │         │  (Python)       │
└────────┬────────┘         └────────┬────────┘
         │                           │
         │      REQ/REP (ZeroMQ)     │
         │      PUB/SUB (ZeroMQ)     │
         └──────────────┬────────────┘
                        ↓
              ┌──────────────────┐
              │   RPC Server     │
              │  (VeighNa Core)  │
              └──────────────────┘
```

## Features

- **REQ/REP Pattern:** Synchronous request/response communication
- **PUB/SUB Pattern:** Asynchronous event publishing
- **ZeroMQ Based:** High-performance message queue
- **Auto Reconnect:** Automatic connection recovery
- **Event Forwarding:** Forward VeighNa events to remote clients

## Server Usage

```python
from vnpy.rpc import RpcServer

class MyRpcServer(RpcServer):
    def __init__(self):
        super().__init__()
        
        # Register functions
        self.register(self.query_balance)
        self.register(self.send_order)
    
    def query_balance(self):
        """Query account balance"""
        return {"balance": 100000}
    
    def send_order(self, symbol, volume):
        """Send order"""
        order_id = "12345"
        return {"orderid": order_id}

# Start server
server = MyRpcServer()
server.start("tcp://*:2014", "tcp://*:4102")
```

## Client Usage

```python
from vnpy.rpc import RpcClient

class MyRpcClient(RpcClient):
    def __init__(self):
        super().__init__()
    
    def callback(self, topic, data):
        """Receive event push"""
        print(f"Received: {topic} - {data}")

# Connect to server
client = MyRpcClient()
client.subscribe("eTick.")  # Subscribe to tick events
client.start("tcp://localhost:2014", "tcp://localhost:4102")

# Call remote function
balance = client.call("query_balance")
print(f"Balance: {balance}")

# Send order
result = client.call("send_order", "BTCUSDT", 1)
print(f"Order ID: {result['orderid']}")
```

## Key Classes

### RpcServer

| Method | Description |
|--------|-------------|
| `register(func)` | Register function |
| `start(rep_address, pub_address)` | Start server |
| `stop()` | Stop server |
| `publish(topic, data)` | Publish event |

### RpcClient

| Method | Description |
|--------|-------------|
| `start(req_address, sub_address)` | Start client |
| `stop()` | Stop client |
| `call(function, *args)` | Call remote function |
| `subscribe(topic)` | Subscribe to topic |
| `callback(topic, data)` | Event callback |

## Communication Patterns

### REQ/REP (Request/Response)

```python
# Client sends request
result = client.call("query_balance")

# Server processes and responds
def query_balance(self):
    return {"balance": 100000}
```

### PUB/SUB (Publish/Subscribe)

```python
# Server publishes event
server.publish("eTick.", tick_data)

# Client receives event
def callback(self, topic, data):
    if topic == "eTick.":
        print(f"Tick: {data}")
```

## Use Cases

### 1. Distributed Trading System

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Strategy   │    │  Strategy   │    │  Strategy   │
│  Client 1   │    │  Client 2   │    │  Client 3   │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          ↓
              ┌──────────────────┐
              │  Trading Server  │
              │  (RPC Server)    │
              └──────────────────┘
```

### 2. Remote Monitoring

```python
# Web server connects to trading server
class WebRpcClient(RpcClient):
    def get_all_positions(self):
        return self.call("get_all_positions")
    
    def get_account(self):
        return self.call("get_account")
```

### 3. Data Recording

```python
# Record market data to separate process
class RecorderRpcClient(RpcClient):
    def callback(self, topic, data):
        if topic.startswith("eTick."):
            self.save_tick(data)
```

## Configuration

### Server Addresses

| Address | Type | Default | Description |
|---------|------|---------|-------------|
| `rep_address` | REQ/REP | `tcp://*:2014` | Request/Response address |
| `pub_address` | PUB/SUB | `tcp://*:4102` | Publish/Subscribe address |

### Client Addresses

| Address | Type | Default | Description |
|---------|------|---------|-------------|
| `req_address` | REQ/REP | `tcp://localhost:2014` | Server request address |
| `sub_address` | PUB/SUB | `tcp://localhost:4102` | Server subscribe address |

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_rpcservice
