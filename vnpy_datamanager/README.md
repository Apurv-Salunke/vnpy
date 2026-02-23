# Data Manager Module for VeighNa

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-1.2.0-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg" />
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

## Description

Intuitively query data overview in database through UI interface. Select any time period to view field details. Supports CSV file data import and export.

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

**Install via pip:**
```bash
pip install vnpy_datamanager
```

**Install from source:**
```bash
cd vnpy_datamanager
pip install .
```

## Features

- **Data Tree:** Browse database by symbol and interval
- **Data View:** View OHLCV data in table format
- **Import/Export:** CSV import and export
- **Data Statistics:** Count, date range, missing data detection
- **Data Update:** Manual data correction and deletion
- **Download:** Download historical data from datafeed

## Supported Data Types

| Type | Description |
|------|-------------|
| **Tick Data** | Level-1 market data (bid/ask, volume) |
| **1min Bars** | 1-minute OHLCV bars |
| **Hour Bars** | 1-hour OHLCV bars |
| **Daily Bars** | Daily OHLCV bars |

## Usage

1. Launch VeighNa Trader
2. Click "Data Manager" app
3. Select symbol and interval from tree view
4. View data in table format
5. Use toolbar functions:
   - **Import:** Load data from CSV
   - **Export:** Save data to CSV
   - **Delete:** Remove selected data
   - **Download:** Fetch from datafeed service

## CSV Format

**Bar Data:**
```csv
datetime,open,high,low,close,volume,turnover,open_interest
2024-01-15 09:15:00,3800,3810,3795,3805,10000,38050000,5000
2024-01-15 09:16:00,3805,3815,3800,3810,8000,30480000,5010
```

**Tick Data:**
```csv
datetime,last_price,volume,bid_price_1,bid_volume_1,ask_price_1,ask_volume_1
2024-01-15 09:15:30,3805,100,3804,50,3806,75
```

## Database Support

| Database | Support |
|----------|---------|
| SQLite | ✅ Default |
| MySQL | ✅ Supported |
| PostgreSQL | ✅ Supported |
| MongoDB | ✅ Supported |
| TDengine | ✅ Supported |
| DolphinDB | ✅ Supported |

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_datamanager
