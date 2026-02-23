# Data Recorder Module for VeighNa

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

DataRecorder is a module for real-time market data recording. Users can use this module to record real-time Tick data and K-line data, and automatically save it to the database.

Recorded data can be viewed through the DataManager module, and can also be used for:
- CtaBacktester historical backtesting
- CtaStrategy strategy initialization
- PortfolioStrategy strategy initialization

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

**Install via pip:**
```bash
pip install vnpy_datarecorder
```

**Install from source:**
```bash
# Download and extract source code
cd vnpy_datarecorder
pip install .
```

## Features

- **Tick Recording:** Record real-time tick data
- **K-line Recording:** Record real-time K-line data
- **Auto Save:** Automatically save to database
- **Selective Recording:** Choose which symbols to record
- **Interval Options:** Support multiple time intervals

## Usage

1. Launch VeighNa Trader
2. Click "Data Recorder" app
3. Select symbol and interval to record
4. Click "Start Recording"

## Data Usage

### Backtesting

```python
from vnpy_ctastrategy import BacktestingEngine

engine = BacktestingEngine()
engine.set_parameters(
    vt_symbol="RB2401.SHFE",
    interval="1m",
    start=datetime(2024, 1, 1),
    end=datetime(2024, 12, 31),
)
# Data recorded by DataRecorder will be used automatically
```

### Strategy Initialization

```python
# CTA Strategy
# Historical data recorded by DataRecorder is used for initialization
strategy.on_init()
```

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_datarecorder
