# REST API Client for VeighNa

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

Multi-threaded REST API client based on requests, used for developing high-performance REST trading interfaces.

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

**Install via pip:**
```bash
pip install vnpy_rest
```

**Install from source:**
```bash
# Download and extract source code
cd vnpy_rest
pip install .
```

## Features

- **Multi-threaded:** Thread-safe request execution
- **Request Class:** Standardized request data structure
- **Response Class:** Standardized response handling
- **Error Handling:** Automatic retry and error logging
- **Rate Limiting:** Built-in request rate limiting support

## Usage Example

```python
from vnpy_rest import RestClient, Request

class MyRestClient(RestClient):
    def __init__(self):
        super().__init__()
        
    def sign(self, request: Request) -> Request:
        """Add signature to request"""
        # Add API key and signature
        request.headers["X-API-KEY"] = self.api_key
        return request
    
    def query_balance(self):
        """Query account balance"""
        self.add_request(
            method="GET",
            path="/api/v1/balance",
            callback=self.on_query_balance
        )
    
    def on_query_balance(self, data: dict, request: Request):
        """Balance query callback"""
        print(f"Balance: {data['balance']}")

# Usage
client = MyRestClient()
client.init("https://api.example.com")
client.start()
client.query_balance()
```

## Key Classes

### RestClient

| Method | Description |
|--------|-------------|
| `init(base_url, proxy_host, proxy_port)` | Initialize client |
| `start()` | Start client (multi-threaded) |
| `stop()` | Stop client |
| `add_request(method, path, callback, ...)` | Add request to queue |

### Request

| Field | Description |
|-------|-------------|
| `method` | HTTP method (GET, POST, etc.) |
| `path` | Request path |
| `params` | URL query parameters |
| `data` | Request body data |
| `headers` | HTTP headers |
| `callback` | Response callback function |

### Response

| Field | Description |
|-------|-------------|
| `status_code` | HTTP status code |
| `text` | Response text |
| `json()` | Parse as JSON |
| `request` | Original request object |

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_rest
