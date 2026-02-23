# CTA Strategy Module for VeighNa

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-1.4.1-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg" />
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

## Description

Application module designed for single-asset CTA (Commodity Trading Advisor) quantitative strategies. Used to implement the complete workflow of CTA strategies including code development, historical backtesting, parameter optimization, and automated trading.

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

**Install via pip:**
```bash
pip install vnpy_ctastrategy
```

**Install from source:**
```bash
# Download and extract source code
cd vnpy_ctastrategy
pip install .
```

## Features

- **Strategy Template:** `CtaTemplate` with callbacks (`on_init`, `on_start`, `on_stop`, `on_tick`, `on_bar`, `on_trade`, `on_order`)
- **Backtesting Engine:** Event-driven backtesting with realistic fill models
- **Parameter Optimization:** Grid search and genetic algorithms
- **Live Trading:** Automatic order execution based on strategy signals
- **Stop Orders:** Local stop order support for exchanges without server-side stop orders

## Built-in Strategies (9 Examples)

| Strategy | Description |
|----------|-------------|
| `AtrRsiStrategy` | ATR + RSI combined signal strategy |
| `BollChannelStrategy` | Bollinger Bands channel breakout |
| `DoubleMaStrategy` | Dual moving average crossover |
| `DualThrustStrategy` | Dual Thrust range breakout |
| `KingKeltnerStrategy` | Keltner Channel trend following |
| `MultiSignalStrategy` | Multiple signal combination |
| `MultiTimeframeStrategy` | Multi-timeframe analysis |
| `TurtleSignalStrategy` | Turtle Trading rules |
| `TestStrategy` | Template for testing |

## Usage Example

```python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

from vnpy_ctp import CtpGateway
from vnpy_ctastrategy import CtaStrategyApp

def main():
    qapp = create_qapp()
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    
    main_engine.add_gateway(CtpGateway)
    main_engine.add_app(CtaStrategyApp)
    
    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()
    qapp.exec()

if __name__ == "__main__":
    main()
```

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_ctastrategy
