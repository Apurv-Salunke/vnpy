# Script Trader Module for VeighNa

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-1.1.1-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg" />
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

## Description

Application module for trading script execution. The main difference from other strategy modules is its **time-driven** **synchronous logic**. Also supports trading operations via REPL commands in command line (Jupyter Notebook). This module has **no backtesting** functionality.

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

**Install via pip:**
```bash
pip install vnpy_scripttrader
```

**Install from source:**
```bash
cd vnpy_scripttrader
pip install .
```

## Key Features

- **Synchronous API:** Blocking calls (waits for order fill)
- **Multi-asset Support:** Trade multiple symbols in one script
- **REPL Trading:** Interactive trading in Jupyter/CLI
- **Custom Calculations:** Execute any Python code
- **Algorithm Support:** Launch execution algorithms

## Difference from Other Strategy Modules

| Feature | CTA/Portfolio | Script Trader |
|---------|---------------|---------------|
| **Driver** | Event-driven | Time-driven (synchronous) |
| **Order Execution** | Async (callback) | Sync (blocking) |
| **Backtesting** | ✅ Yes | ❌ No |
| **Use Case** | Automated strategies | Ad-hoc trading, research |

## Usage Example

```python
# script.py
from vnpy_scripttrader import init_cli_trading
from vnpy.trader.constant import Direction

def run(engine):
    """Main script function"""
    
    # Get market data
    tick = engine.get_tick("RB2401.SHFE")
    print(f"Current price: {tick.last_price}")
    
    # Get positions
    positions = engine.get_all_positions()
    for pos in positions:
        print(f"{pos.vt_symbol}: {pos.volume} lots")
    
    # Get account
    account = engine.get_account()
    print(f"Balance: {account.balance}")
    
    # Trading (blocking - waits for fill)
    engine.buy("RB2401.SHFE", tick.ask_price_1, 10)
    engine.sell("RB2401.SHFE", tick.bid_price_1, 5)
    
    # Algorithm trading (non-blocking)
    engine.send_algo(
        algo_name="twap",
        vt_symbol="IF2401.CFFEX",
        direction=Direction.LONG,
        volume=1000,
        price=3200,
        setting={"time": 1800, "interval": 60}
    )
    
    # Query trades
    trades = engine.get_all_trades()
    for trade in trades:
        print(f"Trade: {trade.vt_symbol} {trade.volume} @ {trade.price}")
```

## Run Script

**Command Line:**
```bash
python -m vnpy_scripttrader script.py
```

**Jupyter Notebook:**
```python
from vnpy_scripttrader import init_cli_trading

engine = init_cli_trader()

# Interactive trading
engine.buy("RB2401.SHFE", 3800, 10)
engine.get_pos("RB2401.SHFE")
```

## API Reference

| Method | Description |
|--------|-------------|
| `get_tick(vt_symbol)` | Get latest tick data |
| `get_pos(vt_symbol)` | Get position for symbol |
| `get_account()` | Get account data |
| `buy/sell/short/cover()` | Trading functions (blocking) |
| `send_algo()` | Launch execution algorithm |
| `get_all_ticks/orders/trades/positions()` | Query all data |

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_scripttrader
