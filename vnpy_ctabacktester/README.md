# CTA Backtester Module for VeighNa

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-1.3.0-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg" />
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

## Description

Graphical CTA strategy backtesting module. Implements data download, historical backtesting, and parameter optimization research functions through a user-friendly graphical interface.

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

**Install via pip:**
```bash
pip install vnpy_ctabacktester
```

**Install from source:**
```bash
cd vnpy_ctabacktester
pip install .
```

## Features

- **Data Download:** Download historical data from datafeed services
- **Backtesting:** Event-driven backtesting engine
- **Parameter Optimization:** Grid search and genetic algorithm optimization
- **Performance Statistics:** Sharpe ratio, max drawdown, win rate, profit factor
- **Charts:** Equity curve, drawdown chart, daily PnL chart, histogram

## Usage

1. Launch VeighNa Trader
2. Click "CTA Backtester" app
3. Select strategy class
4. Configure strategy parameters
5. Set backtesting period and interval
6. Set rate, slippage, size, pricetick, capital
7. Click "Start Backtesting"
8. View results and optimize parameters

## Performance Metrics

- **Sharpe Ratio:** Risk-adjusted return
- **Max Drawdown:** Largest peak-to-trough decline
- **Win Rate:** Percentage of profitable trades
- **Profit Factor:** Gross profit / Gross loss
- **Total Trades:** Number of trades executed
- **Daily PnL:** Profit and loss by day

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_ctabacktester
