# RQData Datafeed for VeighNa

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-3.2.14.1-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg" />
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

## Description

Developed based on Ricequant rqdatac module version 3.1.4. Supports K-line and Tick data for the following Chinese financial markets:

**Futures and Futures Options:**
- CFFEX: China Financial Futures Exchange
- SHFE: Shanghai Futures Exchange
- DCE: Dalian Commodity Exchange
- CZCE: Zhengzhou Commodity Exchange
- INE: Shanghai International Energy Exchange
- GFEX: Guangzhou Futures Exchange

**Precious Metals Spot:**
- SGE: Shanghai Gold Exchange

**Stocks and ETF Options:**
- SSE: Shanghai Stock Exchange
- SZSE: Shenzhen Stock Exchange

**Note:** Requires appropriate data service subscription. Apply for trial [here](https://www.ricequant.com/welcome/purchase?utm_source=vnpy).

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

**Install via pip:**
```bash
pip install vnpy_rqdata
```

**Install from source:**
```bash
# Download and extract source code
cd vnpy_rqdata
pip install .
```

## Usage

When using Ricequant RQData in VeighNa, configure the following fields in global settings:

| Name | Description | Required | Example |
|------|-------------|----------|---------|
| datafeed.name | Datafeed name | Yes | rqdata |
| datafeed.username | Username | Yes | (Your license) |
| datafeed.password | Password | Yes | (RQData token after purchase/trial) |

## Supported Data Types

| Type | Description |
|------|-------------|
| 1m | 1-minute K-line |
| 5m | 5-minute K-line |
| 15m | 15-minute K-line |
| 30m | 30-minute K-line |
| 1h | 1-hour K-line |
| 1d | Daily K-line |
| tick | Tick data |

## Example

```python
from vnpy.trader.datafeed import get_datafeed

datafeed = get_datafeed()

# Query historical data
bars = datafeed.query_bar_history(
    symbol="IF2401",
    exchange=Exchange.CFFEX,
    interval=Interval.MINUTE,
    start=datetime(2024, 1, 1),
    end=datetime(2024, 12, 31)
)
```

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_rqdata
- **RQData:** https://www.ricequant.com/
