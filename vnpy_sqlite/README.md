# SQLite Database Adapter for VeighNa

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-1.1.3-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg" />
</p>

## Description

SQLite database adapter developed based on peewee. No need to install additional database software, easy to use and suitable for beginner users.

## Usage

When using SQLite in VeighNa, configure the following fields in global settings:

| Name | Description | Required | Example |
|------|-------------|----------|---------|
| database.name | Database name | Yes | sqlite |
| database.database | Database file | Yes | database.db |

## Features

- **No Installation Required:** SQLite is built into Python
- **Single File:** All data stored in one file
- **Zero Configuration:** No database server setup needed
- **Portable:** Easy to backup and transfer

## Configuration

Edit `.vntrader/setting.json`:

```json
{
    "database.name": "sqlite",
    "database.database": "database.db"
}
```

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_sqlite
