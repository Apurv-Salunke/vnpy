# Option Master Module for VeighNa

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

Application module designed for option volatility trading strategies. Supports real-time volatility surface tracking, option portfolio Greeks risk management, automatic Delta hedging algorithms, Electronic Eye volatility execution algorithm, and scenario analysis stress testing.

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

**Install via pip:**
```bash
pip install vnpy_optionmaster
```

**Install from source:**
```bash
cd vnpy_optionmaster
pip install .
```

## Features

- **Volatility Surface:** Real-time implied volatility calculation and display
- **Greeks Tracking:** Delta, Gamma, Theta, Vega for portfolio risk management
- **Pricing Models:** Black-Scholes, Black-76, Binomial Tree
- **Delta Hedging:** Automatic delta neutral hedging algorithm
- **Scenario Analysis:** PnL simulation under different market conditions
- **Electronic Eye:** Smart volatility execution algorithm

## Pricing Models

| Model | Use Case |
|-------|----------|
| Black-Scholes | European stock options |
| Black-76 | European futures options (NIFTY, BANKNIFTY) |
| Binomial Tree | American options |

## Key Components

### 1. Option Chain Management
- Automatic option chain updates
- Strike and expiry selection
- ATM/OTM/ITM classification

### 2. Volatility Surface
- Real-time IV calculation
- IV surface visualization
- IV rank and percentile

### 3. Greeks Risk Management
- Portfolio-level Greeks
- Delta hedging alerts
- Gamma/Theta/Vega limits

### 4. Execution Algorithms
- **Electronic Eye:** Auto-quote based on IV
- **Delta Hedge:** Auto-rebalance delta neutrality

### 5. Scenario Analysis
- PnL simulation under price/IV changes
- Stress testing
- Risk reports

## Usage Example

```python
from vnpy_optionmaster import OptionEngine
from vnpy.trader.engine import MainEngine

# Add to main engine
option_engine = main_engine.add_engine(OptionEngine)

# Add option portfolio
option_engine.add_portfolio("My Portfolio")

# Add option chain
option_engine.add_chain("NIFTY", underlying_price=22000)

# View Greeks
greeks = option_engine.get_portfolio_greeks("My Portfolio")
print(f"Delta: {greeks.delta}, Gamma: {greeks.gamma}")

# Run scenario analysis
scenario = option_engine.run_scenario(
    underlying_move=0.02,  # 2% move
    iv_change=0.05         # 5% IV change
)
```

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_optionmaster
