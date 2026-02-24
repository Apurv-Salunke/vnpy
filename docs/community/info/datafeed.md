# Data Service


For data services, VeighNa provides a standardized interface BaseDatafeed (located in vnpy.trader.datafeed), implementing more flexible data service support. In global configuration, all fields related to data services use datafeed as the prefix.

The specific field meanings are as follows:
- datafeed.name: The name of the data service interface, must be full lowercase English letters;
- datafeed.username: The username for the data service;
- datafeed.password: The password for the data service.

The above fields are required for all data services. If using token authorization, please fill it in the datafeed.password field. Currently, VeighNa Trader supports the following seven data services, **specific details for each data service can be found in the corresponding project address**.

## Xuntou (XT)

Xuntou is a professional data service launched by Ruizhi Rongke Company. For most individual investors, it should be a cost-effective choice:
- Project address: [vnpy_xt](https://github.com/vnpy/vnpy_xt)
- Data categories: Stocks, futures, options, funds, contract information, financial information
- Data cycle: Daily, hourly, minute, TICK (real-time updates)
- Registration: [Xuntou](https://xuntou.net/#/signup?utm_source=vnpy)

## RQData

Ricequant RQData is a cloud data service launched by Ricequant Technology Company, providing extensive domestic financial market variety data support:
- Project address: [vnpy_rqdata](https://github.com/vnpy/vnpy_rqdata)
- Data categories: Stocks, futures, options, funds, and gold TD
- Data cycle: Daily, hourly, minute, TICK (real-time updates)
- Registration: [RICEQUANT](https://www.ricequant.com/welcome/purchase?utm_source=vnpy)

**Please note that the username and password in the configuration information are not the account and password used to log in to the Ricequant official website.**


## UData

Hengyoushu UData is a cloud data service launched by Hundsun Electronics, providing unlimited and unrestricted access to various financial data:
- Project address: [vnpy_udata](https://github.com/vnpy/vnpy_udata)
- Data categories: Stocks, futures
- Data cycle: Minute bars (post-market updates)
- Registration: [Hengyoushu UData](https://udata.hs.net/home)


## TuShare

TuShare is a well-known open-source Python financial data interface project in China, developed and maintained by the Jimmy team for a long time. In addition to market data, it also provides many alternative data types:
- Project address: [vnpy_tushare](https://www.github.com/vnpy/vnpy_tushare)
- Data categories: Stocks, futures
- Data cycle: Daily, minute bars (post-market updates)
- Registration: [Tushare Big Data Community](https://tushare.pro/)


## TQSDK
Tianqin TQSDK is a Python programmatic trading solution launched by Xinyi Technology, providing historical data acquisition since the listing of currently tradable contracts:
- Project address: [vnpy_tqsdk](https://github.com/vnpy/vnpy_tqsdk)
- Data categories: Futures
- Data cycle: Minute bars (real-time updates)
- Registration: [Tianqin Quantitative - Xinyi Technology (shinnytech.com)](https://www.shinnytech.com/tianqin)


## Wind
For practitioners working in domestic financial institutions, Wind from Wind Information is already the standard configuration for work. Whether it's stocks, bonds, or commodity market data, Wind has everything:
- Project address: [vnpy_wind](https://github.com/vnpy/vnpy_wind)
- Data categories: Futures
- Data cycle: Minute bars (real-time updates)
- Registration: [Wind Financial Terminal](https://www.wind.com.cn/newsite/wft.html)

## iFinD
iFinD from Hexin Shunda is a financial data terminal launched by Hexin Shunda Company for professional institutional users, and its market share has been rapidly increasing in the past few years:
- Project address: [vnpy_ifind](https://github.com/vnpy/vnpy_ifind)
- Data categories: Futures
- Data cycle: Minute bars (real-time updates)
- Registration: [iFinD Financial Data Terminal](http://www.51ifind.com/)

## Tinysoft
As an old-brand financial data company in China, Tianrui's core product [Tianrui .NET Financial Analysis Platform] (referred to as TinySoft) has accumulated a large number of users in the securities research institute and proprietary trading fields. When flipping through securities financial engineering research reports, you will often find the source information note in the chart remarks saying "Data above comes from Tianrui":
- Project address: [vnpy_tinysoft](https://github.com/vnpy/vnpy_tinysoft)
- Data categories: Futures
- Data cycle: Minute bars (real-time updates)
- Registration: [Tianrui .NET Financial Analysis Platform](http://www.tinysoft.com.cn/TSDN/HomePage.tsl)

Please note that because Tinysoft currently does not support Python 3.10, VeighNa Studio 3.0.0 does not provide Tinysoft support.

## Script Usage
Before using the script, please configure the data service to be used according to the above instructions, and call the corresponding function interfaces when using (specific interface support refers to the data cycles supported in the above text).

### Script Loading

#### Load required packages and data structures in the script

```python3
from datetime import datetime
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.datafeed import get_datafeed
from vnpy.trader.object import HistoryRequest

# Get data service instance
datafeed = get_datafeed()
```

#### Get k-line level historical data

```python3
req = HistoryRequest(
    # Contract code (example cu888 is Ricequant continuous contract code, for demonstration only, please query specific contract code from data service provider according to your needs)
    symbol="cu888",
    # Exchange where the contract is located
    exchange=Exchange.SHFE,
    # Historical data start time
    start=datetime(2019, 1, 1),
    # Historical data end time
    end=datetime(2021, 1, 20),
    # Data time granularity, optionally minute, hour, and day levels by default, specific selection should be combined with the data service's permissions and needs
    interval=Interval.DAILY
)

# Get k-line historical data
data = datafeed.query_bar_history(req)
```

#### Get tick level historical data

Due to the large volume of tick data, please refer to the above text to confirm whether the data service provides tick data download services before downloading

```python3
req = HistoryRequest(
    # Contract code (example cu888 is Ricequant continuous contract code, for demonstration only, please query specific contract code from data service provider according to your needs)
    symbol="cu888",
    # Exchange where the contract is located
    exchange=Exchange.SHFE,
    # Historical data start time
    start=datetime(2019, 1, 1),
    # Historical data end time
    end=datetime(2021, 1, 20),
    # Data time granularity, tick level
    interval=Interval.TICK
)

# Get tick historical data
data = datafeed.query_tick_history(req)
```
