# RPC Datafeed Service

Used to share datafeed services that are limited to single sign-on (IP or process) across multiple VeighNa Trader processes. Only recommended for use on local machine or within LAN.

Place the `datafeed_server.py` and `run_trader.py` startup scripts in separate directories, each containing an independent `.vntrader` folder:

**datafeed_server.py:**
- In the `.vntrader/vt_setting.json` of its directory, configure datafeed-related fields to the actual datafeed service to use (e.g., rqdata)

**run_trader.py:**
- In the `.vntrader/vt_setting.json` of its directory, modify datafeed-related fields referencing the SETTINGS content at the top of `run_trader.py` file

**Note:** Port numbers on both sides must match.

## Usage

### Start Datafeed Server

```bash
# In datafeed_server directory
python datafeed_server.py
```

### Start Trader Clients

```bash
# In each trader directory
python run_trader.py
```

## Configuration

### Datafeed Server Settings

```json
{
    "datafeed.name": "rqdata",
    "datafeed.username": "your_username",
    "datafeed.password": "your_password"
}
```

### Trader Client Settings

```json
{
    "datafeed.name": "rpc",
    "datafeed.username": "rpc",
    "datafeed.password": "rpc",
    "datafeed.rpc_address": "tcp://localhost:2013"
}
```

## Use Cases

### 1. Single Datafeed License

Share one RQData license across multiple trading strategies running in separate processes.

### 2. Centralized Data Cache

Cache historical data in one process, serve to multiple strategy processes.

### 3. LAN Distribution

Share datafeed from one machine to multiple trading machines on same network.

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_rpcservice
