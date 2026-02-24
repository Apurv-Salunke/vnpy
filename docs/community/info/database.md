# Database

VeighNa Trader currently supports the following eight databases:

## SQL Database Introduction

### SQLite (Default)

SQLite is a lightweight embedded database that does not require installation and configuration of a data service program. It is VeighNa's **default database**, suitable for beginner users. Its features include:
 - Stored in a single cross-platform disk file;
 - No need to configure, install, and manage in the system;
 - No need for a separate server process.

#### SQLite Configuration Fields

When configuring SQLite in VeighNa Trader, the following fields need to be filled:

| Field Name             | Value | Required |
|---------           |---- | --- |
|database.name     | sqlite | Optional (defaults to sqlite if not filled)
|database.database   | Database file (relative to trader directory) | Required |

SQLite configuration example is shown below:

| Field Name            | Value |
|---------           |---- |
|database.name     | sqlite |
|database.database   | database.db |

### MySQL

MySQL is currently the mainstream open-source relational database. Its features include:
 - Rich documentation, active community and users;
 - Supports multiple operating systems and multiple development languages;
 - Can be replaced with other high-performance NewSQL database compatible implementations (such as TiDB).

#### MySQL Configuration Fields

When configuring MySQL in VeighNa Trader, the following fields need to be filled:

| Field Name            | Value | Required |
|---------           |---- | ---- |
|database.name     | "mysql"| Required |
|database.host       | Address | Required |
|database.port       | Port | Required |
|database.database   | Database name | Required |
|database.user       | Username | Optional |
|database.password   | Password | Optional |

MySQL configuration example is shown below:

| Field Name            | Value |
|---------           |----  |
|database.name     | mysql |
|database.host       | localhost |
|database.port       | 3306 |
|database.database   | vnpy |
|database.user       | root |
|database.password   |      |

### PostgreSQL

PostgreSQL is an open-source relational database with richer features, recommended only for experienced users. Compared to MySQL, its features include:
 - Uses a multi-process structure;
 - Supports adding new features through extension plugins.

#### PostgreSQL Configuration Fields

When configuring PostgreSQL in VeighNa Trader, the following fields need to be filled:

| Field Name            | Value | Required |
|---------           |---- | ---- |
|database.name     | "postgresql" | Required |
|database.host       | Address | Required |
|database.port       | Port | Required |
|database.database   | Database name | Required |
|database.user       | Username | Required |
|database.password   | Password | Required |

PostgreSQL configuration example is shown below:

| Field Name            | Value |
|---------           |----  |
|database.name     | postgresql |
|database.host       | localhost |
|database.port       | 5432 |
|database.database   | vnpy |
|database.user       | postgres |
|database.password   | 123456 |

Please note that VeighNa will not actively create databases for relational databases, so please ensure that the database corresponding to the database.database field has been created. If the database has not been created, please manually connect to the database and run this command:
```sql
    create database <filled database.database>;
```


## Non-SQL Database Introduction

### MongoDB

MongoDB is a non-relational database based on distributed file storage (bson format). Its features include:
 - Document-oriented storage with simple operations;
 - Supports rich storage types and data operations;
 - Built-in hot data memory cache for faster read and write speeds.

#### MongoDB Configuration Fields

When configuring MongoDB in VeighNa Trader, the following fields need to be filled:

| Field Name               |   Value |          Required|
|---------           |---- |  ---|
|database.name     | "mongodb" | Required |
|database.host       | Address| Required |
|database.port       | Port| Required |
|database.database   | Database name| Required |
|database.user       | Username| Optional |
|database.password   | Password| Optional |
|database.authentication_source   | [Database used to create users][AuthSource]| Optional |

MongoDB configuration example with authentication is shown below:

| Field Name             | Value |
|---------           |----  |
|database.name     | mongodb |
|database.host       | localhost |
|database.port       | 27017 |
|database.database   | vnpy |
|database.user       | root |
|database.password   |      |
|database.authentication_source   | vnpy |

[AuthSource]: https://docs.mongodb.com/manual/core/security-users/#user-authentication-database

### InfluxDB

InfluxDB is a non-relational database specifically designed for time series data storage. Its features include:
- Columnar data storage provides extremely high read and write efficiency;
- Operates as a standalone service process, supporting multi-process concurrent access requirements.

Please select InfluxDB version 2.0 during installation.

Please note that the cmd running influxd.exe needs to remain running. If closed, it will cause InfluxDB to exit. Alternatively, you can use some auxiliary tools to register it as a Windows service running in the background.

#### InfluxDB Configuration Fields
When configuring InfluxDB in VeighNa Trader, the following fields need to be filled:

| Field Name            | Value | Required |
|---------           |---- | ---- |
|database.name     | "influxdb" | Required |
|database.host       | Address| Required |
|database.port       | Port| Required |
|database.database   | Database name| Required |
|database.user       | Username| Required |
|database.password   | Password| Required |

InfluxDB configuration example is shown below:

| Field Name             | Value |
|---------           |----  |
|database.name     | influxdb |
|database.host       | localhost |
|database.port       | 8086 |
|database.database   | vnpy |
|database.user       | root |
|database.password   | 12345678 |

### DolphinDB

DolphinDB is a high-performance distributed time-series database developed by Zhejiang Zhiyu Technology Co., Ltd. It is particularly suitable for low-latency or real-time tasks that require high speed. Its features include:
- Columnar analytical (OLAP) database using a hybrid engine (based on memory and disk), fully utilizing cache for acceleration;
- Native partitioned table storage, reasonable partitioning schemes can allow CPU multi-threaded parallel loading of data within each partition;
- Supports efficient data compression, significantly reducing disk storage space while greatly reducing IO communication overhead.

Although DolphinDB is commercial software, it also provides a free community edition. Please select [2.0 Beta](https://github.com/dolphindb/release/blob/master/2.00/README.md) version during installation.

Please note:
 - The cmd running dolphindb.exe needs to remain running. If closed, it will cause DolphinDB to exit. Alternatively, you can use some auxiliary tools to register it as a Windows service running in the background;
 - Because DolphinDB currently does not support Python 3.10, VeighNa Studio 3.0.0 does not provide DolphinDB support.

#### DolphinDB Configuration Fields

The following fields need to be filled:

| Field Name        | Value | Required |
|---------          |---- | ---- |
|database.name      | "dolphindb"| Required |
|database.host      | Address | Required |
|database.port      | Port | Required |
|database.database  | Database name | Required |
|database.user      | Username | Required |
|database.password  | Password | Required |

DolphinDB configuration example is shown below:

| Field Name            | Value |
|---------          |----  |
|database.name      | dolphindb |
|database.host      | localhost |
|database.port      | 8848 |
|database.database  | vnpy |
|database.user      | admin |
|database.password  | 123456|

### Arctic

Arctic is a high-performance financial time-series database developed by UK quantitative hedge fund Man AHL based on MongoDB. Its features include:
- Supports direct storage of pandas DataFrame and numpy ndarray objects;
- Allows versioning of data (similar to git in databases), facilitating data iteration management during factor mining;
- Based on chunked storage and LZ4 compression, saves significant resources in network and disk IO, achieving ultra-high-performance data queries.

Please note that because Arctic currently does not support Python 3.10, VeighNa Studio 3.0.0 does not provide Arctic support.

#### Arctic Configuration Fields

| Field Name          | Value | Required |
|---------        |---- | ---- |
|database.name    | "arctic"| Required |
|database.host    | Address | Required |
|database.port    | Port | Required |

Arctic configuration example is shown below:

| Field Name          | Value |
|---------        |----  |
|database.name    | arctic |
|database.host    | localhost |
|database.database    | vnpy |

### LevelDB
LevelDB is a high-performance Key/Value database launched by Google. Its features include:
- Positioned as a general-purpose data storage solution;
- Implements in-process storage engine based on LSM algorithm;
- Supports billions of levels of massive data.

Please note that because LevelDB currently does not support Python 3.10, VeighNa Studio 3.0.0 does not provide LevelDB support.

#### LevelDB Configuration Fields
| Field Name            | Value | Required |
|---------          |---- | ---- |
|database.name      | "leveldb"| Required |
|database.database  | Database name | Required |
|database.port    | Port | Required |

LevelDB configuration example is shown below:

| Field Name            | Value |
|---------          |  ----  |
|database.name      | leveldb |
|database.database  | vnpy_data |


## Database Configuration (Using MySQL as an Example)

This document uses MySQL as an example to introduce the database configuration process.

First, download the Windows version installation package [MySQL Installer for Windows] from the [MySQL official website](https://dev.mysql.com/downloads/), as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/database/1.png)

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/database/2.png)

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/database/3.png)

After downloading, you will get an msi format installation package. Double-click to open it and select [Full] mode to install MySQL, then click the [Next] button all the way to complete the installation.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/database/4.png)

During installation, relevant components will be automatically downloaded from the website. First click the [Execute] button to complete, then click the [Next] button.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/database/5.png)

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/database/6.png)

During installation, you will be asked to enter the password 3 times. For demonstration purposes, we will set the password to 1001. Please use a more complex and secure password during your own installation.
After installation is complete, MySQL's graphical management tool MySQL WorkBench will automatically open. Click the menu bar [Database] -> [Connect to Database], as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/database/7.png)

In the dialog box that appears, directly select the default database Local Instance MySQL, then click the [OK] button to connect to the MySQL database server.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/database/8.png)

In the automatically opened database management interface, click the button in the red box in the menu bar as shown in the figure below to create a new database. Enter "vnpy" in [Name], then click the [Apply] button below to confirm.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/database/9.png)

In the database script execution confirmation dialog box that appears subsequently, just click [Apply], and all operations in MySQL WorkBench are complete.

Then start VeighNa Trader, click the [Configuration] in the menu bar, and set the database-related fields:

- name should be changed to mysql (please note the case);
- database should be changed to vnpy;
- host is the local IP, i.e., localhost or 127.0.0.1;
- port is MySQL's default port 3306;
- user username is root
- password is the previously set 1001.

```json
        database.name: mysql
        database.database: vnpy
        database.host: localhost
        database.port: 3306
        database.user: root
        database.password: 1001
```

After filling in, it should look like the image below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/database/22.png)

After saving the configuration changes, restart VeighNa Trader to enable the new database configuration. After restarting, if there are no error prompts during the process of opening VeighNa Trader, it means the MySQL database configuration was successful.


## Script Usage

Before using the script, please configure the database to be used according to the above instructions, and call the corresponding function interfaces when using.

### Script Loading

#### Load required packages and data structures in the script

```python3
from datetime import datetime
from typing import List
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.database import get_database
from vnpy.trader.object import BarData, TickData

# Get database instance
database = get_database()
```

#### Configure specific parameter data for the required contract

```python3
# Contract code, 888 is Ricequant's continuous contract, for demonstration only, please change the contract code according to your needs
symbol = "cu888"

# Exchange, the exchange of the target contract
exchange = Exchange.SHFE

# Historical data start time, precise to the day
start = datetime(2019, 1, 1)

# Historical data end time, precise to the day
end = datetime(2021, 1, 20)

# Data time granularity, daily level is used in this example
interval = Interval.DAILY
```

#### Database Read Operations

If there is no data in the specified time period in the database, an empty list is returned

```python3
# Read k-line data from database
bar1 = database.load_bar_data(
    symbol=symbol,
    exchange=exchange,
    interval=interval,
    start=start,
    end=end
)

# Read tick data from database
tick1 = database.load_tick_data(
    symbol=symbol,
    exchange=exchange,
    start=start,
    end=end
)
```

#### Database Write Operations

Please note that **bar_data** and **tick_data** in the example do not show the acquisition and conversion methods. If you want to write in script mode, please refer to the source code or other methods to convert to the data structure in the example.

```python3
# K-line data to be stored, please obtain and convert to the required form
bar_data: List[BarData] = None

database.save_bar_data(bar_data)

# Tick data to be stored, please obtain and convert to the required form
tick_data: List[TickData] = None

# Store tick data in database
database.save_tick_data(tick_data)
```

#### Database Delete Operations

Cannot be recovered, please operate with caution

```python3
# Delete k-line data from database
database.delete_bar_data(
    symbol=symbol,
    exchange=exchange,
    interval=interval
)

# Delete tick data from database
database.delete_tick_data(
    symbol=symbol,
    exchange=exchange
)
```
