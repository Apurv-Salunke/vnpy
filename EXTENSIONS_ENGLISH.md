# VeighNa Extensions - English Documentation

Complete English translations of all major extension modules (excluding gateways).

---

## Table of Contents

1. [CTA Strategy](#1-cta-strategy-vnpy_ctastrategy)
2. [CTA Backtester](#2-cta-backtester-vnpy_ctabacktester)
3. [Spread Trading](#3-spread-trading-vnpy_spreadtrading)
4. [Portfolio Strategy](#4-portfolio-strategy-vnpy_portfoliostrategy)
5. [Algorithmic Trading](#5-algorithmic-trading-vnpy_algotrading)
6. [Script Trader](#6-script-trader-vnpy_scripttrader)
7. [Option Master](#7-option-master-vnpy_optionmaster)
8. [Portfolio Manager](#8-portfolio-manager-vnpy_portfoliomanager)
9. [Data Manager](#9-data-manager-vnpy_datamanager)
10. [Risk Manager](#10-risk-manager-vnpy_riskmanager)

---

## 1. CTA Strategy (`vnpy_ctastrategy`)

**Version:** 1.4.1

### Description

Application module designed for single-asset CTA (Commodity Trading Advisor) quantitative strategies. Used to implement the complete workflow of CTA strategies including:
- Code development
- Historical backtesting
- Parameter optimization
- Automated trading

### Installation

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

### Key Features

- **Strategy Template:** `CtaTemplate` with callbacks (`on_init`, `on_start`, `on_stop`, `on_tick`, `on_bar`, `on_trade`, `on_order`)
- **Backtesting Engine:** Event-driven backtesting with realistic fill models
- **Parameter Optimization:** Grid search and genetic algorithms
- **Live Trading:** Automatic order execution based on strategy signals
- **Stop Orders:** Local stop order support for exchanges without server-side stop orders

### Built-in Strategies (9 examples)

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

### Usage Example

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

---

## 2. CTA Backtester (`vnpy_ctabacktester`)

**Version:** 1.3.0

### Description

Graphical CTA strategy backtesting module. Implements data download, historical backtesting, and parameter optimization research functions through a user-friendly graphical interface.

### Installation

```bash
pip install vnpy_ctabacktester
```

### Key Features

- **Data Download:** Download historical data from datafeed services
- **Backtesting:** Event-driven backtesting engine
- **Parameter Optimization:** Grid search and genetic algorithm optimization
- **Performance Statistics:** Sharpe ratio, max drawdown, win rate, etc.
- **Charts:** Equity curve, drawdown chart, daily PnL chart

### Usage

1. Launch VeighNa Trader
2. Click "CTA Backtester" app
3. Select strategy class
4. Configure parameters
5. Set backtesting period
6. Click "Start Backtesting"

---

## 3. Spread Trading (`vnpy_spreadtrading`)

**Version:** 1.3.1

### Description

Application module designed for multi-leg spread trading. Covers the complete workflow including:
- Spread quote calculation
- Spread algorithm execution
- Spread strategy development

### Installation

```bash
pip install vnpy_spreadtrading
```

### Important Note

Does not support spread trading contracts composed of exchange arbitrage orders.

### Key Features

- **Spread Definition:** Custom spread = Leg1 - Leg2 + Leg3 ...
- **Spread Quote:** Real-time spread price calculation
- **Spread Chart:** Visual spread price history
- **Algorithm Trading:** Auto-execute spread orders
- **Strategy Template:** `SpreadStrategyTemplate` for custom strategies

### Built-in Strategies (2)

| Strategy | Description |
|----------|-------------|
| `BasicSpreadStrategy` | Manual spread trading with limits |
| `StatisticalArbitrageStrategy` | Statistical arbitrage based on spread mean reversion |

### Usage Example

```python
# Define spread: RB2401 (long) - RB2405 (short)
from vnpy_spreadtrading import SpreadData, LegData

leg1 = LegData("RB2401.SHFE")
leg2 = LegData("RB2405.SHFE")

spread = SpreadData(
    name="RB Spread",
    legs=[leg1, leg2],
    variable_symbols={"A": "RB2401.SHFE", "B": "RB2405.SHFE"},
    variable_directions={"A": Direction.LONG, "B": Direction.SHORT},
    price_multipliers={"A": 1, "B": -1},
    trading_multipliers={"A": 1, "B": 1}
)
```

---

## 4. Portfolio Strategy (`vnpy_portfoliostrategy`)

**Version:** 1.2.2

### Description

Application module for multi-asset portfolio strategies. Used to implement:
- Historical backtesting
- Parameter optimization
- Live automated trading

### Installation

```bash
pip install vnpy_portfoliostrategy
```

### Key Features

- **Multi-Asset Support:** Trade multiple contracts simultaneously
- **Backtesting Engine:** Portfolio-level backtesting
- **Strategy Template:** `StrategyTemplate` with `on_bar()` for any symbol
- **Real-time Trading:** Live portfolio rebalancing

### Built-in Strategies (4)

| Strategy | Description |
|----------|-------------|
| `PairTradingStrategy` | Pairs trading with cointegration |
| `PcpArbitrageStrategy` | Period conversion arbitrage |
| `PortfolioBollChannelStrategy` | Multi-asset Bollinger strategy |
| `TrendFollowingStrategy` | Multi-asset trend following |

### Difference from CTA Strategy

| Feature | CTA Strategy | Portfolio Strategy |
|---------|--------------|-------------------|
| **Assets** | Single contract | Multiple contracts |
| **on_bar()** | One symbol only | Any symbol in portfolio |
| **Position** | `self.pos` | `self.get_pos(vt_symbol)` |
| **Use Case** | Futures, crypto | Alpha, options arbitrage |

---

## 5. Algorithmic Trading (`vnpy_algotrading`)

**Version:** 1.1.0

### Description

Application module for algorithmic trading execution. Provides multiple smart trading algorithms:
- TWAP (Time-Weighted Average Price)
- Sniper (Price-triggered execution)
- Iceberg (Hide true order size)
- BestLimit (Queue at best bid/ask)
- Stop (Auto stop-loss)

Supports multiple invocation methods:
- UI interface
- CSV batch import
- External module access

### Installation

```bash
pip install vnpy_algotrading
```

### Built-in Algorithms (5)

| Algorithm | Description |
|-----------|-------------|
| `TwapAlgo` | Time-sliced execution over specified period |
| `IcebergAlgo` | Split large orders into smaller visible sizes |
| `SniperAlgo` | Execute when price reaches target |
| `BestLimitAlgo` | Queue at best bid/ask prices |
| `StopAlgo` | Automatic stop-loss execution |

### Usage Example

```python
from vnpy_algotrading import AlgoEngine
from vnpy.trader.constant import Direction, Offset

# Start TWAP algorithm
algo_engine.start_algo(
    template_name="TwapAlgo",
    vt_symbol="RB2401.SHFE",
    direction=Direction.LONG,
    offset=Offset.OPEN,
    price=3800.00,
    volume=1000,
    setting={
        "time": 1800,      # 30 minutes
        "interval": 60     # Order every 60 seconds
    }
)
```

---

## 6. Script Trader (`vnpy_scripttrader`)

**Version:** 1.1.1

### Description

Application module for trading script execution. The main difference from other strategy modules is:
- **Time-driven** synchronous logic
- Supports **REPL-style** trading in command line (Jupyter Notebook)
- **No backtesting** functionality

### Installation

```bash
pip install vnpy_scripttrader
```

### Key Features

- **Synchronous API:** Blocking calls (wait for fill)
- **Multi-asset Support:** Trade multiple symbols in one script
- **REPL Trading:** Interactive trading in Jupyter/CLI
- **Custom Calculations:** Any Python code execution

### Usage Example

```python
# script.py
from vnpy_scripttrader import init_cli_trading

def run(engine):
    # Get market data
    tick = engine.get_tick("RB2401.SHFE")
    print(f"Current price: {tick.last_price}")
    
    # Get positions
    positions = engine.get_all_positions()
    
    # Trading (blocking - waits for fill)
    engine.buy("RB2401.SHFE", tick.ask_price_1, 10)
    
    # Algorithm trading (non-blocking)
    engine.send_algo(
        algo_name="twap",
        vt_symbol="RB2401.SHFE",
        direction=Direction.LONG,
        volume=1000,
        price=3800,
        setting={"time": 1800}
    )

# Run from command line
# python -m vnpy_scripttrader script.py
```

---

## 7. Option Master (`vnpy_optionmaster`)

**Version:** 1.3.0

### Description

Application module designed for option volatility trading strategies. Supports:
- Real-time volatility surface tracking
- Option portfolio Greeks risk management
- Automatic Delta hedging algorithms
- Electronic Eye volatility execution algorithm
- Scenario analysis and stress testing

### Installation

```bash
pip install vnpy_optionmaster
```

### Key Features

- **Volatility Surface:** Real-time IV calculation and display
- **Greeks Tracking:** Delta, Gamma, Theta, Vega for portfolio
- **Pricing Models:** Black-Scholes, Black-76, Binomial Tree
- **Delta Hedging:** Auto-hedge delta exposure
- **Scenario Analysis:** PnL simulation under different market conditions

### Pricing Models

| Model | Use Case |
|-------|----------|
| Black-Scholes | European stock options |
| Black-76 | European futures options |
| Binomial Tree | American options |

### Usage

1. Add option contracts to portfolio
2. View volatility surface
3. Set target Greeks
4. Enable auto-hedging
5. Run scenario analysis

---

## 8. Portfolio Manager (`vnpy_portfoliomanager`)

**Version:** 1.1.0

### Description

Application module for trading portfolio tracking and management. Based on independent strategy portfolios (sub-accounts), provides:
- Order and trade record management
- Automatic position tracking
- Real-time daily PnL statistics

### Installation

```bash
pip install vnpy_portfoliomanager
```

### Key Features

- **Sub-Accounts:** Multiple independent portfolios
- **Position Tracking:** Automatic position updates
- **PnL Calculation:** Realized and unrealized PnL
- **Daily Reports:** End-of-day PnL summary
- **Trade Blotter:** Complete trade history

### Usage Example

```python
from vnpy_portfoliomanager import PortfolioManager

# Create portfolio
portfolio = PortfolioManager(
    name="My Portfolio",
    initial_capital=1_000_000
)

# Add trades
portfolio.add_trade(trade_data)

# Get PnL
daily_pnl = portfolio.calculate_daily_pnl()
total_pnl = portfolio.calculate_total_pnl()
```

---

## 9. Data Manager (`vnpy_datamanager`)

**Version:** 1.2.0

### Description

Intuitively query data overview in database through UI interface. Select any time period to view field details. Supports CSV file data import and export.

### Installation

```bash
pip install vnpy_datamanager
```

### Key Features

- **Data Tree:** Browse database by symbol/interval
- **Data View:** View OHLCV data in table format
- **Import/Export:** CSV import and export
- **Data Statistics:** Count, date range, missing data
- **Data Update:** Manual data correction

### Usage

1. Launch VeighNa Trader
2. Click "Data Manager" app
3. Select symbol and interval from tree
4. View data in table
5. Export to CSV or import from CSV

---

## 10. Risk Manager (`vnpy_riskmanager`)

**Version:** 2.0.0

### Description

Pre-trade risk control module for VeighNa framework. Provides a risk rule engine for real-time order validation during trading. All core risk rules are compiled to C extensions using **Cython**, achieving microsecond-level latency for high-frequency trading scenarios.

### Installation

**Environment Requirements:**
- Python 3.10 or above
- VeighNa 4.0.0 or above
- C++ compiler (for Cython extension compilation)
  - Windows: [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  - Linux: `sudo apt-get install build-essential`
  - macOS: `xcode-select --install`

**Install via pip:**
```bash
pip install vnpy_riskmanager
```

**Install from source:**
```bash
git clone https://github.com/vnpy/vnpy_riskmanager.git
cd vnpy_riskmanager
pip install -e .
```

### Built-in Risk Rules (5)

| Rule | Description |
|------|-------------|
| `ActiveOrderRule` | Limit on active (working) orders |
| `DailyLimitRule` | Daily order/cancel count limit |
| `DuplicateOrderRule` | Duplicate order detection |
| `OrderSizeRule` | Maximum order size limit |
| `OrderValidityRule` | Order validity check (price tick, max volume) |

### Usage Example

```python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

from vnpy_ctp import CtpGateway
from vnpy_riskmanager import RiskManagerApp

def main():
    qapp = create_qapp()
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    
    main_engine.add_gateway(CtpGateway)
    
    # Add risk manager (auto-starts)
    main_engine.add_app(RiskManagerApp)
    
    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()
    qapp.exec()

if __name__ == "__main__":
    main()
```

### Creating Custom Rules

**Python Rule (Fast Development):**

```python
# rules/my_rule.py
from vnpy.trader.object import OrderRequest
from vnpy_riskmanager.template import RuleTemplate

class MyRule(RuleTemplate):
    """My custom rule description"""
    
    name: str = "MyRule"
    
    parameters: dict[str, str] = {
        "max_volume": "Maximum volume"
    }
    
    def on_init(self) -> None:
        self.max_volume: int = 100
    
    def check_allowed(self, req: OrderRequest, gateway_name: str) -> bool:
        if req.volume > self.max_volume:
            self.write_log(f"Volume {req.volume} exceeds limit {self.max_volume}")
            return False
        return True
```

**Cython Rule (High Performance):**

```cython
# rules/my_rule_cy.pyx
from vnpy.trader.object cimport OrderRequest
from vnpy_riskmanager.template cimport RuleTemplate

cdef class MyRuleCy(RuleTemplate):
    cdef public int max_volume
    
    cpdef void on_init(self):
        self.max_volume = 100
    
    cpdef bint check_allowed(self, OrderRequest req, str gateway_name):
        if req.volume > self.max_volume:
            self.write_log(f"Volume exceeds limit")
            return False
        return True

# Python wrapper
class MyRule(MyRuleCy):
    name: str = "MyRule"
```

**Compile Cython:**
```bash
cd rules/
python rule_setup.py build_ext --inplace
```

---

## Summary Table

| Extension | Purpose | Backtest | Live | Algo |
|-----------|---------|----------|------|------|
| **CTA Strategy** | Single-asset CTA | ✅ | ✅ | ❌ |
| **CTA Backtester** | CTA backtesting | ✅ | ❌ | ❌ |
| **Spread Trading** | Multi-leg spreads | ✅ | ✅ | ❌ |
| **Portfolio Strategy** | Multi-asset portfolio | ✅ | ✅ | ❌ |
| **Algo Trading** | Smart execution | ❌ | ✅ | ✅ |
| **Script Trader** | Custom scripts | ❌ | ✅ | ✅ |
| **Option Master** | Options volatility | ❌ | ✅ | ✅ |
| **Portfolio Manager** | PnL tracking | ❌ | ✅ | ❌ |
| **Data Manager** | Data management | ❌ | ❌ | ❌ |
| **Risk Manager** | Pre-trade risk | ❌ | ✅ | ❌ |

---

## Resources

- **Main Repository:** https://github.com/vnpy/vnpy
- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **PyPI:** https://pypi.org/user/vnpy/
