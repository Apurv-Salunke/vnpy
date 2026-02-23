# Algorithmic Trading Module for VeighNa

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

Application module for algorithmic trading execution. Provides multiple smart trading algorithms: TWAP, Sniper, Iceberg, BestLimit, and Stop. Supports multiple invocation methods including UI interface, CSV batch import, and external module access.

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

**Install via pip:**
```bash
pip install vnpy_algotrading
```

**Install from source:**
```bash
cd vnpy_algotrading
pip install .
```

## Built-in Algorithms (5)

| Algorithm | Description |
|-----------|-------------|
| `TwapAlgo` | Time-Weighted Average Price - Slices large orders over time |
| `IcebergAlgo` | Iceberg order - Hides true order size from market |
| `SniperAlgo` | Sniper - Executes when price reaches target level |
| `BestLimitAlgo` | Best Limit - Queues at best bid/ask prices |
| `StopAlgo` | Stop loss - Auto-executes when stop price triggered |

## Features

- **Algorithm Templates:** `AlgoTemplate` base class for custom algorithms
- **Real-time Monitoring:** Track algorithm progress and status
- **Multi-Algo Support:** Run multiple algorithms simultaneously
- **Event-Driven:** Reacts to tick data and timer events
- **Pause/Resume:** Control algorithm execution

## Usage Example

```python
from vnpy_algotrading import AlgoEngine
from vnpy.trader.constant import Direction, Offset

# Start TWAP algorithm
algo_engine.start_algo(
    template_name="TwapAlgo",
    vt_symbol="RB2401.SHFE",
    direction=Direction.LONG,
    offset=Offset.OPEN,
    price=3800.00,
    volume=1000,
    setting={
        "time": 1800,      # Execute over 30 minutes
        "interval": 60     # Send order every 60 seconds
    }
)

# Start Iceberg algorithm
algo_engine.start_algo(
    template_name="IcebergAlgo",
    vt_symbol="IF2401.CFFEX",
    direction=Direction.SHORT,
    offset=Offset.OPEN,
    price=3200.00,
    volume=500,
    setting={
        "visible_volume": 10,  # Show only 10 lots at a time
        "price_add": 1         # Price offset for limit order
    }
)
```

## Custom Algorithm Template

```python
from vnpy_algotrading import AlgoTemplate

class MyAlgo(AlgoTemplate):
    display_name: str = "My Custom Algo"
    
    default_setting: dict = {
        "param1": 100,
        "param2": 0.5
    }
    
    variables: list = ["var1", "var2"]
    
    def on_tick(self, tick):
        # React to tick data
        pass
    
    def on_timer(self):
        # Called every second
        pass
    
    def on_trade(self, trade):
        # Trade fill callback
        pass
```

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_algotrading
