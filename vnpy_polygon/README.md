# Polygon.io Datafeed for VeighNa

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-1.0.0-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg" />
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

## Description

Developed based on Polygon.io Python API, supports K-line data for US stock market.

**Note:**
- Requires appropriate data service subscription
- For option contract historical data, remove "O:" prefix from symbol

## Installation

Recommended environment: [**VeighNa Studio**](https://www.vnpy.com) version 4.0.0 or above.

**Install via pip:**
```bash
pip install vnpy_polygon
```

**Install from source:**
```bash
# Download and extract source code
cd vnpy_polygon
pip install .
```

## Usage

When using Polygon.io in VeighNa, configure the following fields in global settings:

| Name | Description | Required | Example |
|------|-------------|----------|---------|
| datafeed.name | Datafeed name | Yes | polygon |
| datafeed.password | API Key | Yes | (Your API Key) |

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_polygon
