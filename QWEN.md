# VeighNa Project Context

## Project Overview

**VeighNa** (formerly vnpy) is an open-source Python-based quantitative trading system framework, designed "By Traders, For Traders, AI-Powered." It has evolved into a multi-functional quantitative trading platform used by financial institutions including hedge funds, securities firms, and futures companies.

**Current Version:** 4.3.0

### Core Architecture

VeighNa follows an **event-driven architecture** with the following key components:

```
vnpy/
├── event/          # Event-driven engine core
├── trader/         # Trading engine, UI, and core abstractions
├── alpha/          # AI/ML quantitative strategies (v4.0+)
├── chart/          # High-performance K-line charts
└── rpc/            # Cross-process communication
```

### Key Modules

| Module | Description |
|--------|-------------|
| **EventEngine** | Core event-driven engine with timer support |
| **MainEngine** | Central hub integrating gateways, engines, and apps |
| **OmsEngine** | Order Management System (positions, orders, accounts) |
| **LogEngine** | Centralized logging system |
| **EmailEngine** | Email notification system |
| **Alpha** | ML-based strategy framework (Lasso, LightGBM, MLP) |

### Data Abstractions

Core data classes in `vnpy/trader/object.py`:
- `TickData` - Real-time market tick data
- `BarData` - OHLCV candlestick data
- `OrderData` / `OrderRequest` - Order management
- `TradeData` - Trade fill records
- `PositionData` - Position holdings
- `AccountData` - Account balance info
- `ContractData` - Contract/instrument metadata

## Building and Running

### Environment Requirements

- **Python:** 3.10+ (64-bit), **recommended: Python 3.13**
- **OS:** Windows 11+ / Windows Server 2022+ / Ubuntu 22.04 LTS+ / macOS
- **Recommended:** Use [VeighNa Studio](https://download.vnpy.com/veighna_studio-4.3.0.exe) - pre-built distribution with VeighNa Station

### Installation

**Standard Installation:**
```bash
# Windows
install.bat

# Ubuntu/Linux
bash install.sh

# macOS
bash install_osx.sh
```

**Manual Installation:**
```bash
pip install -e .

# With AI/ML features
pip install -e ".[alpha]"

# For development
pip install -e ".[dev]"
```

### Running VeighNa Trader

**Via VeighNa Station:**
1. Launch VeighNa Station
2. Login with forum credentials
3. Click "VeighNa Trader" button

**Via Script:**
```python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

from vnpy_ctp import CtpGateway
from vnpy_ctastrategy import CtaStrategyApp
from vnpy_ctabacktester import CtaBacktesterApp

def main():
    qapp = create_qapp()
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    
    main_engine.add_gateway(CtpGateway)
    main_engine.add_app(CtaStrategyApp)
    main_engine.add_app(CtaBacktesterApp)
    
    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()
    qapp.exec()

if __name__ == "__main__":
    main()
```

## Development Conventions

### Code Quality Tools

**Linting (ruff):**
```bash
ruff check .
```

**Type Checking (mypy):**
```bash
mypy vnpy
```

### Configuration

**pyproject.toml** defines:
- Ruff linting rules (B, E, F, UP, W codes)
- MyPy strict type checking settings
- Package build configuration (hatchling)

### Project Structure

```
vnpy/
├── vnpy/                   # Core framework
│   ├── event/              # Event engine
│   ├── trader/             # Trading core
│   │   ├── engine.py       # MainEngine, OmsEngine, LogEngine
│   │   ├── object.py       # Data classes
│   │   ├── constant.py     # Enum constants
│   │   ├── ui/             # Qt-based GUI
│   │   └── locale/         # i18n translations
│   ├── alpha/              # AI/ML strategies
│   │   ├── dataset/        # Feature engineering
│   │   ├── model/          # ML models
│   │   ├── strategy/       # Strategy base classes
│   │   └── lab.py          # Research workflow
│   ├── chart/              # K-line visualization
│   └── rpc/                # RPC components
├── examples/               # Usage examples
│   ├── alpha_research/     # ML research notebooks
│   ├── cta_backtesting/    # CTA strategy backtesting
│   └── veighna_trader/     # Trader startup example
├── tests/                  # Test suite
├── docs/                   # Documentation (Sphinx)
└── pyproject.toml          # Project configuration
```

### Key Design Patterns

1. **Event-Driven:** All components communicate via `EventEngine` using pub/sub pattern
2. **Gateway Abstraction:** Trading interfaces implement `BaseGateway` for uniform access
3. **Data Classes:** All data objects use `@dataclass` with typed fields
4. **Type Hints:** Full type annotations throughout the codebase

### Testing

Limited test coverage in the repository. Main test file:
- `tests/test_alpha101.py` - Alpha factor testing

### External Dependencies

**Core:**
- `PySide6` - Qt6 bindings for GUI
- `numpy`, `pandas` - Data processing
- `ta-lib` - Technical analysis
- `pyqtgraph` - Charting
- `loguru` - Logging

**AI/ML (optional):**
- `polars` - Fast DataFrame
- `scikit-learn`, `lightgbm`, `torch` - Machine learning
- `scipy` - Scientific computing

## Gateway and App Ecosystem

VeighNa uses a plugin architecture. Core functionality is extended via external packages:

**Gateways (Trading Interfaces):**
- `vnpy_ctp` - CTP (domestic futures/options)
- `vnpy_ib` - Interactive Brokers
- `vnpy_xtp` - XTP (A-shares, ETF options)
- And 20+ other gateways

**Apps (Trading Applications):**
- `vnpy_ctastrategy` - CTA strategy engine
- `vnpy_ctabacktester` - CTA backtesting
- `vnpy_spreadtrading` - Spread trading
- `vnpy_portfoliostrategy` - Portfolio strategies

## Alpha Module (AI/ML)

The v4.0+ `vnpy.alpha` module provides:

```python
from vnpy.alpha import AlphaLab, AlphaDataset, AlphaModel, AlphaStrategy

# Workflow
lab = AlphaLab()
dataset = AlphaDataset()
model = AlphaModel()
strategy = AlphaStrategy()
```

**Components:**
- `dataset` - Feature engineering (Alpha158, custom factors)
- `model` - ML models (Lasso, LightGBM, MLP)
- `strategy` - Strategy templates (cross-sectional, time-series)
- `lab` - Research workflow management

## Useful Commands

```bash
# Install with all dependencies
pip install -e ".[alpha,dev]"

# Run linting
ruff check .

# Run type checking
mypy vnpy

# Run tests
pytest tests/
```

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy
- **Examples:** See `examples/` directory for usage patterns
