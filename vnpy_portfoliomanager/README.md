# Portfolio Manager Module for VeighNa

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

Application module for trading portfolio tracking and management. Based on independent strategy portfolios (sub-accounts), provides order and trade record management, automatic position tracking, and real-time daily PnL statistics.

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

**Install via pip:**
```bash
pip install vnpy_portfoliomanager
```

**Install from source:**
```bash
cd vnpy_portfoliomanager
pip install .
```

## Features

- **Sub-Accounts:** Multiple independent portfolios
- **Position Tracking:** Automatic position updates from trades
- **PnL Calculation:** Realized and unrealized PnL
- **Daily Reports:** End-of-day PnL summary
- **Trade Blotter:** Complete trade history per portfolio
- **Multi-Strategy:** Track different strategies separately

## Portfolio Structure

```
Portfolio Manager
├── Portfolio 1 (e.g., CTA Strategy A)
│   ├── Positions
│   ├── Trades
│   └── Daily PnL
├── Portfolio 2 (e.g., CTA Strategy B)
│   ├── Positions
│   ├── Trades
│   └── Daily PnL
└── Portfolio 3 (e.g., Alpha Strategy)
    ├── Positions
    ├── Trades
    └── Daily PnL
```

## Usage Example

```python
from vnpy_portfoliomanager import PortfolioManager

# Create portfolio
portfolio = PortfolioManager(
    name="My CTA Portfolio",
    initial_capital=1_000_000
)

# Add trades (automatically from event engine)
portfolio.add_trade(trade_data)

# Get PnL
daily_pnl = portfolio.calculate_daily_pnl(date)
total_pnl = portfolio.calculate_total_pnl()

# Get positions
positions = portfolio.get_all_positions()

# Generate report
report = portfolio.generate_daily_report()
```

## Performance Metrics

- **Total PnL:** Cumulative profit/loss
- **Daily PnL:** Day-by-day PnL breakdown
- **Realized PnL:** Closed position PnL
- **Unrealized PnL:** Open position PnL
- **Win Rate:** Percentage of profitable days
- **Max Drawdown:** Largest peak-to-trough decline

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_portfoliomanager
