# Portfolio Strategy Module for VeighNa

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-1.2.2-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg" />
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

## Description

Application module for multi-asset portfolio strategies. Used to implement historical backtesting, parameter optimization, and live automated trading for strategies trading multiple contracts simultaneously.

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

**Install via pip:**
```bash
pip install vnpy_portfoliostrategy
```

**Install from source:**
```bash
cd vnpy_portfoliostrategy
pip install .
```

## Features

- **Multi-Asset Support:** Trade multiple contracts simultaneously
- **Backtesting Engine:** Portfolio-level backtesting with daily PnL calculation
- **Strategy Template:** `StrategyTemplate` with `on_bar()` for any symbol in portfolio
- **Real-time Trading:** Live portfolio rebalancing
- **Parameter Optimization:** Grid search and genetic algorithms

## Built-in Strategies (4)

| Strategy | Description |
|----------|-------------|
| `PairTradingStrategy` | Pairs trading with cointegration test |
| `PcpArbitrageStrategy` | Period conversion arbitrage |
| `PortfolioBollChannelStrategy` | Multi-asset Bollinger Bands strategy |
| `TrendFollowingStrategy` | Multi-asset trend following |

## Difference from CTA Strategy

| Feature | CTA Strategy | Portfolio Strategy |
|---------|--------------|-------------------|
| **Assets** | Single contract | Multiple contracts |
| **on_bar()** | One symbol only | Any symbol in portfolio |
| **Position** | `self.pos` | `self.get_pos(vt_symbol)` |
| **Use Case** | Futures, crypto | Alpha, options arbitrage |

## Strategy Template Example

```python
from vnpy_portfoliostrategy import StrategyTemplate
from vnpy.trader.constant import Direction

class MyPortfolioStrategy(StrategyTemplate):
    def on_init(self):
        self.write_log("Strategy initialized")
        
    def on_bar(self, bar):
        # Bar can be from ANY symbol in portfolio
        vt_symbol = bar.vt_symbol
        
        # Get position for this symbol
        pos = self.get_pos(vt_symbol)
        
        # Your strategy logic
        if self.buy_signal(vt_symbol):
            self.buy(vt_symbol, bar.close_price, 1)
```

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_portfoliostrategy
