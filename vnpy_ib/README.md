# Interactive Brokers Gateway for VeighNa

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-10.40.1.2-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg" />
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

## Description

Interactive Brokers trading gateway developed based on ibapi version 10.40.1.

IbGateway supports two contract code styles: numeric codes and string codes.

### Numeric Codes (ConId)

Based on IB platform ConId. To find ConId: In TWS software, right-click any contract → Financial Product Info → Details, then find the contract's ConId on the popup webpage.

### String Codes

Based on contract description information. Naming rules and examples:

| Contract Type | Code Rule | Code (symbol) | Exchange |
|---------------|-----------|---------------|----------|
| Stock | Name-Currency-Type | SPY-USD-STK | SMART |
| Forex | Name-Currency-Type | EUR-USD-CASH | IDEALPRO |
| Precious Metals | Name-Currency-Type | XAUUSD-USD-CMDTY | SMART |
| Futures | Name-Expiry-Currency-Type | ES-202002-USD-FUT | GLOBEX |
| Futures (Specify Multiplier) | Name-Expiry-Multiplier-Type | SI-202006-1000-USD-FUT | NYMEX |
| Futures Options | Name-Expiry-Type-Strike-Multiplier-Currency-Type | ES-2020006-C-2430-50-USD-FOP | GLOBEX |

Order, trade, and position contract codes default to numeric codes (ConId). If user subscribed to market data using string codes, string codes are used.

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

### Install ibapi

1. Download TWS API .msi installer from [IBKR website](https://interactivebrokers.github.io/#)
2. Run the installer
3. Find `source\pythonclient` folder in installation directory
4. Run in cmd:
```bash
python setup.py install
```

### Install vnpy_ib

**Via pip:**
```bash
pip install vnpy_ib
```

**From source:**
```bash
# Download and extract source code
cd vnpy_ib
pip install .
```

## Usage

Start with script (script/run.py):

```python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

from vnpy_ib import IbGateway


def main():
    """Main entry function"""
    qapp = create_qapp()

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    main_engine.add_gateway(IbGateway)

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()


if __name__ == "__main__":
    main()
```

## Supported Assets

| Asset | Symbol Format | Exchange |
|-------|--------------|----------|
| Stock | SPY-USD-STK | SMART |
| Forex | EUR-USD-CASH | IDEALPRO |
| Commodity | XAUUSD-USD-CMDTY | SMART |
| Futures | ES-202002-USD-FUT | GLOBEX |
| Futures Options | ES-2020006-C-2430-50-USD-FOP | GLOBEX |

## Features

- **Global Markets:** Access to stocks, futures, options, forex worldwide
- **Real-time Data:** Real-time market data streaming
- **Historical Data:** Query historical K-line data
- **Order Types:** Market, limit, stop orders
- **Account Management:** Real-time account updates

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_ib
- **IBKR:** https://www.interactivebrokers.com/
