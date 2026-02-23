# VeighNa Extensions Catalog

Complete catalog of official VeighNa extension packages. All extensions follow a plugin architecture and are distributed as separate PyPI packages.

**Legend:** :arrow_up: = Upgraded to v4.0 compatible

---

## Gateway Extensions (Trading Interfaces)

Gateway extensions provide connectivity to trading venues and brokers.

### Domestic Market (China)

#### Futures & Options

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_ctp](https://github.com/vnpy/vnpy_ctp) | CTP | Domestic futures and options (SHFE, ZCE, DCE) | :arrow_up: |
| [vnpy_mini](https://github.com/vnpy/vnpy_mini) | CTP Mini | Domestic futures and options (CTP Mini system) | :arrow_up: |
| [vnpy_femas](https://github.com/vnpy/vnpy_femas) | Femas | Domestic futures (Pegasus system) | :arrow_up: |
| [vnpy_uft](https://github.com/vnpy/vnpy_uft) | Hundsun UFT | Domestic futures, ETF options | :arrow_up: |
| [vnpy_esunny](https://github.com/vnpy/vnpy_esunny) | Esunny | Domestic futures, Gold TD | :arrow_up: |
| [vnpy_tts](https://github.com/vnpy/vnpy_tts) | TTS | Domestic futures (paper trading simulation) | :arrow_up: |
| [vnpy_sgit](https://github.com/vnpy/vnpy_sgit) | Sgit | Gold TD, domestic futures | - |

#### ETF Options

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_sopt](https://github.com/vnpy/vnpy_sopt) | CTP Securities | ETF options (CTP Securities system) | :arrow_up: |
| [vnpy_hts](https://github.com/vnpy/vnpy_hts) | Hundsun HTS | ETF options | :arrow_up: |
| [vnpy_sec](https://github.com/vnpy/vnpy_sec) | Hundsun Feichuang | ETF options | :arrow_up: |

#### A-Shares (Stocks)

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_xtp](https://github.com/vnpy/vnpy_xtp) | Zhongtai XTP | A-shares, ETF options | :arrow_up: |
| [vnpy_tora](https://github.com/vnpy/vnpy_tora) | Tora | A-shares, ETF options | :arrow_up: |
| [vnpy_ost](https://github.com/vnpy/vnpy_ost) | Orient Securities OST | A-shares | - |
| [vnpy_emt](https://github.com/vnpy/vnpy_emt) | East Money EMT | A-shares | - |

#### Gold

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_ksgold](https://github.com/vnpy/vnpy_ksgold) | Kingstar Gold | Gold TD | :arrow_up: |

#### Asset Management

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_lstar](https://github.com/vnpy/vnpy_lstar) | Lstar | Futures asset management | :arrow_up: |
| [vnpy_rohon](https://github.com/vnpy/vnpy_rohon) | Rohon | Futures asset management | :arrow_up: |
| [vnpy_jees](https://github.com/vnpy/vnpy_jees) | Jees | Futures asset management | :arrow_up: |

#### Interbank Market

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_comstar](https://github.com/vnpy/vnpy_comstar) | Comstar | Interbank market | - |

---

### Overseas Market

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_ib](https://github.com/vnpy/vnpy_ib) | Interactive Brokers | International securities, futures, options, metals | :arrow_up: |
| [vnpy_tap](https://github.com/vnpy/vnpy_tap) | Esunny 9.0 | International futures | :arrow_up: |
| [vnpy_da](https://github.com/vnpy/vnpy_da) | Direct Futures | International futures | :arrow_up: |

---

### Special Applications

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_rqdata](https://github.com/vnpy/vnpy_rqdata) | RQData | Cross-market real-time quotes (stocks, indices, ETFs, futures) | :arrow_up: |
| [vnpy_xt](https://github.com/vnpy/vnpy_xt) | Xuntou | Cross-market real-time quotes (stocks, indices, convertibles, ETFs, futures, options) | :arrow_up: |
| [vnpy_rpcservice](https://github.com/vnpy/vnpy_rpcservice) | RPC Service | Inter-process communication for distributed architecture | :arrow_up: |

---

## App Extensions (Trading Applications)

App extensions provide trading strategy engines, backtesting tools, and management utilities.

### Strategy Engines

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_ctastrategy](https://github.com/vnpy/vnpy_ctastrategy) | CTA Strategy | CTA strategy engine with fine-grained order control | :arrow_up: |
| [vnpy_spreadtrading](https://github.com/vnpy/vnpy_spreadtrading) | Spread Trading | Spread trading with custom spreads and auto-strategies | :arrow_up: |
| [vnpy_portfoliostrategy](https://github.com/vnpy/vnpy_portfoliostrategy) | Portfolio Strategy | Multi-contract strategies (Alpha, options arbitrage) | :arrow_up: |
| [vnpy_algotrading](https://github.com/vnpy/vnpy_algotrading) | Algo Trading | Smart trading algorithms (TWAP, Sniper, Iceberg, BestLimit) | :arrow_up: |
| [vnpy_scripttrader](https://github.com/vnpy/vnpy_scripttrader) | Script Trader | Script-based strategies, multi-asset quant strategies, REPL trading | :arrow_up: |

### Backtesting

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_ctabacktester](https://github.com/vnpy/vnpy_ctabacktester) | CTA Backtester | CTA strategy backtesting with GUI analysis tools | :arrow_up: |

### Options Trading

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_optionmaster](https://github.com/vnpy/vnpy_optionmaster) | Option Master | Options trading with pricing models, IV surface, Greeks tracking | :arrow_up: |

### Simulation

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_paperaccount](https://github.com/vnpy/vnpy_paperaccount) | Paper Account | Local simulation trading based on real-time quotes | :arrow_up: |

### Portfolio Management

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_portfoliomanager](https://github.com/vnpy/vnpy_portfoliomanager) | Portfolio Manager | Sub-account management, trade tracking, PnL statistics | :arrow_up: |

### Data Management

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_datamanager](https://github.com/vnpy/vnpy_datamanager) | Data Manager | Historical data management, tree view, CSV import/export | :arrow_up: |
| [vnpy_datarecorder](https://github.com/vnpy/vnpy_datarecorder) | Data Recorder | Real-time Tick/K-line recording to database | :arrow_up: |

### Charting & Visualization

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_chartwizard](https://github.com/vnpy/vnpy_chartwizard) | Chart Wizard | K-line charts with historical data + real-time updates | :arrow_up: |

### Risk Management

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_riskmanager](https://github.com/vnpy/vnpy_riskmanager) | Risk Manager | Risk controls: flow limits, order size, active order limits | :arrow_up: |

### Web & Integration

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_webtrader](https://github.com/vnpy/vnpy_webtrader) | Web Trader | Web server with REST API + Websocket push (B-S architecture) | :arrow_up: |
| [vnpy_excelrtd](https://github.com/vnpy/vnpy_excelrtd) | Excel RTD | Excel real-time data service via PyXLL | :arrow_up: |

---

## Database Extensions

Database adapters provide persistence for market data, orders, positions, and trades.

### SQL Databases

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_sqlite](https://github.com/vnpy/vnpy_sqlite) | SQLite | Lightweight single-file database, default option, beginner-friendly | :arrow_up: |
| [vnpy_mysql](https://github.com/vnpy/vnpy_mysql) | MySQL | Mainstream RDBMS, compatible with TiDB and other NewSQL | :arrow_up: |
| [vnpy_postgresql](https://github.com/vnpy/vnpy_postgresql) | PostgreSQL | Feature-rich RDBMS with extension support | :arrow_up: |

### NoSQL Databases

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_mongodb](https://github.com/vnpy/vnpy_mongodb) | MongoDB | Document database with BSON format, in-memory hot data cache | :arrow_up: |
| [vnpy_taos](https://github.com/vnpy/vnpy_taos) | TDengine | Distributed time-series database with built-in cache and stream processing | :arrow_up: |
| [vnpy_dolphindb](https://github.com/vnpy/vnpy_dolphindb) | DolphinDB | High-performance distributed time-series database for low-latency tasks | - |

---

## Datafeed Extensions (Historical Data Providers)

Datafeed adapters provide historical market data for backtesting and research.

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_xt](https://github.com/vnpy/vnpy_xt) | Xuntou | Stocks, futures, options, funds, bonds | :arrow_up: |
| [vnpy_rqdata](https://github.com/vnpy/vnpy_rqdata) | RQData (Ricequant) | Stocks, futures, options, funds, bonds, Gold TD | :arrow_up: |
| [vnpy_mcdata](https://github.com/vnpy/vnpy_mcdata) | MultiCharts | Futures, futures options | :arrow_up: |
| [vnpy_tushare](https://github.com/vnpy/vnpy_tushare) | TuShare | Stocks, futures, options, funds | :arrow_up: |
| [vnpy_wind](https://github.com/vnpy/vnpy_wind) | Wind | Stocks, futures, funds, bonds | :arrow_up: |
| [vnpy_ifind](https://github.com/vnpy/vnpy_ifind) | iFinD (Homashare) | Stocks, futures, funds, bonds | :arrow_up: |
| [vnpy_tqsdk](https://github.com/vnpy/vnpy_tqsdk) | TQSDK | Futures | :arrow_up: |
| [vnpy_gm](https://github.com/vnpy/vnpy_gm) | Goldminer (MyQuant) | Stocks | :arrow_up: |
| [vnpy_polygon](https://github.com/vnpy/vnpy_polygon) | Polygon | US stocks, futures, options | :arrow_up: |

---

## Core API Extensions

Core infrastructure components for building trading systems.

| Package | Name | Description | Status |
|---------|------|-------------|--------|
| [vnpy_rest](https://github.com/vnpy/vnpy_rest) | REST Client | High-performance async REST API client based on coroutines | :arrow_up: |
| [vnpy_websocket](https://github.com/vnpy/vnpy_websocket) | Websocket Client | High-performance async Websocket client | :arrow_up: |

---

## AI/ML Module (Built-in)

AI-powered quantitative strategies module (included in main vnpy package since v4.0).

| Module | Description |
|--------|-------------|
| `vnpy.alpha.dataset` | Factor feature engineering, includes Alpha158 factor set |
| `vnpy.alpha.model` | ML model training (Lasso, LightGBM, MLP) |
| `vnpy.alpha.strategy` | Strategy development (cross-sectional, time-series) |
| `vnpy.alpha.lab` | Research workflow management with visualization tools |

---

## Installation

### Install Main Framework
```bash
pip install vnpy
```

### Install with AI/ML Features
```bash
pip install "vnpy[alpha]"
```

### Install Extensions
```bash
# Example: Install CTP gateway and CTA strategy
pip install vnpy-ctp vnpy-ctastrategy vnpy-ctabacktester

# Example: Install database adapter
pip install vnpy-sqlite

# Example: Install datafeed
pip install vnpy-rqdata
```

### Install from Source
```bash
git clone https://github.com/vnpy/vnpy_<package>.git
cd vnpy_<package>
pip install .
```

---

## Usage Example

```python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

# Import gateway and apps
from vnpy_ctp import CtpGateway
from vnpy_ctastrategy import CtaStrategyApp
from vnpy_ctabacktester import CtaBacktesterApp
from vnpy_sqlite import SqliteDatabase
from vnpy_rqdata import RqdataDatafeed

def main():
    qapp = create_qapp()
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    
    # Add gateway
    main_engine.add_gateway(CtpGateway)
    
    # Add apps
    main_engine.add_app(CtaStrategyApp)
    main_engine.add_app(CtaBacktesterApp)
    
    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()
    qapp.exec()

if __name__ == "__main__":
    main()
```

---

## Repository Structure

All extension packages follow a consistent structure:

```
vnpy_<name>/
├── vnpy/
│   └── <name>/
│       ├── __init__.py
│       ├── gateway.py      # For gateway extensions
│       ├── engine.py       # For app extensions
│       ├── ui/             # GUI components
│       └── ...
├── setup.py
├── pyproject.toml
└── README.md
```

---

## Statistics

| Category | Count |
|----------|-------|
| Gateway Extensions | 24 |
| App Extensions | 16 |
| Database Adapters | 6 |
| Datafeed Adapters | 9 |
| Core API Extensions | 2 |

**Total Packages:** 57+

---

## Resources

- **Main Repository:** https://github.com/vnpy/vnpy
- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **PyPI:** https://pypi.org/user/vnpy/
