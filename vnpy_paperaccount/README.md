# Paper Account Module for VeighNa

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

PaperAccount is a module for local simulated trading. Users can perform local simulated trading based on real-time market data through its UI interface.

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

**Install via pip:**
```bash
pip install vnpy_paperaccount
```

**Install from source:**
```bash
# Download and extract source code
cd vnpy_paperaccount
pip install .
```

## Features

- **Real-time Market Data:** Uses live market data from gateways
- **Local Matching:** Simulated order matching locally
- **Position Tracking:** Tracks simulated positions
- **Account Management:** Simulated account balance and PnL
- **No Risk:** Test strategies without real money

## Usage

1. Launch VeighNa Trader
2. Add PaperAccount gateway
3. Configure initial capital
4. Start trading with real-time market data

## Use Cases

### Strategy Testing

Test your trading strategies with real-time market data before going live.

### API Testing

Test your gateway connections and order routing without risking real capital.

### Training

Learn trading operations without financial risk.

## Configuration

Edit `.vntrader/paper_account_setting.json`:

```json
{
    "initial_balance": 1000000,
    "gateway_name": "CTP"
}
```

## Limitations

- **No Market Impact:** Orders don't affect market prices
- **Simplified Matching:** Matching logic is simplified
- **No Slippage Control:** Slippage is simulated

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_paperaccount
