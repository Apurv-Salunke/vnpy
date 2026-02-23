# Spread Trading Module for VeighNa

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-1.3.1-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg" />
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

## Description

Application module designed for multi-leg spread trading. Covers the complete workflow including spread quote calculation, spread algorithm execution, and spread strategy development.

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

**Install via pip:**
```bash
pip install vnpy_spreadtrading
```

**Install from source:**
```bash
cd vnpy_spreadtrading
pip install .
```

## Important Note

Does not support spread trading contracts composed of exchange arbitrage orders.

## Features

- **Spread Definition:** Custom spread = Leg1 - Leg2 + Leg3 ...
- **Spread Quote:** Real-time spread price calculation
- **Spread Chart:** Visual spread price history
- **Algorithm Trading:** Auto-execute spread orders
- **Strategy Template:** `SpreadStrategyTemplate` for custom strategies
- **Backtesting:** Spread strategy historical backtesting

## Built-in Strategies (2)

| Strategy | Description |
|----------|-------------|
| `BasicSpreadStrategy` | Manual spread trading with price limits |
| `StatisticalArbitrageStrategy` | Statistical arbitrage based on spread mean reversion |

## Spread Definition Example

```python
from vnpy_spreadtrading import SpreadData, LegData
from vnpy.trader.constant import Direction

# Define legs
leg1 = LegData("RB2401.SHFE")  # Rebar January
leg2 = LegData("RB2405.SHFE")  # Rebar May

# Define spread: Long RB2401 - Short RB2405
spread = SpreadData(
    name="RB Spread",
    legs=[leg1, leg2],
    variable_symbols={"A": "RB2401.SHFE", "B": "RB2405.SHFE"},
    variable_directions={"A": Direction.LONG, "B": Direction.SHORT},
    price_multipliers={"A": 1, "B": -1},
    trading_multipliers={"A": 1, "B": 1}
)
```

## Strategy Template

```python
from vnpy_spreadtrading import SpreadStrategyTemplate

class MySpreadStrategy(SpreadStrategyTemplate):
    def on_init(self):
        self.write_log("Strategy initialized")
        
    def on_bar(self, bar):
        # Spread bar data
        spread_price = bar.close_price
        
        # Your strategy logic here
        if spread_price > self.entry_price:
            self.buy_spread(spread_price, 1)
```

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_spreadtrading
