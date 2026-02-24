# VeighNa Trader

## Starting the Program

### Graphical Mode

After starting and logging into VeighNa Station, users can click the [Trading] button, check the required trading interfaces and application modules, and click the [Start] button to enter VeighNa Trader, as shown below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/quick_start/22.png)

### Script Mode

Find the run.py file in the examples/veighna_trader folder (not under veighna_studio, you need to download the source code from github). Run run.py to enter VeighNa Trader.

- Taking the Win10 system as an example, users can hold down [Shift] in the folder where run.py is located, and click the right mouse button at the same time, select [Open powershell window here], in the pop-up window, enter the following command to start VeighNa Trader.
   ```bash
        python run.py
   ```
   ![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/quick_start/3.png)

The successfully started VeighNa Trader is shown below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/quick_start/23.png)

## Connecting Interface

### SimNow Simulation

Taking the use of SimNow simulation trading account to log in to the **CTP** interface as an example, click [System] -> [Connect CTP] in the menu bar on VeighNa Trader, and the account configuration window will pop up, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/gateway/1.png)

Among them, the field filling requirements are as follows:
- Username: xxxxxx (6-digit pure number account)
- Password: xxxxxx (need to change the password once for after-hours testing)
- Broker Code: 9999 (SimNow default broker number)
- Trading Server: 182.254.243.31:30001 (intraday testing)
- Market Data Server: 182.254.243.31:30011 (intraday testing)
- Product Name: simnow_client_test
- Authorization Code: 0000000000000000 (16 zeros)

Please note:
 - The username needs to be filled with InvestorID (6-digit pure number), not the account (mobile phone number) registered on the Simnow website. In addition, the account registered on Simnow needs to change the password once before logging in.
 - If after clicking to connect to the interface, there is no output in the [Log] component of the VeighNa Trader main interface, you can use the telnet tool to test whether the trading server/market data server ports are enabled.

After successful connection, the [Log] component of the VeighNa Trader main interface will immediately output login-related information, and users can also see account information, position information, contract query, and other relevant information. As shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/1.png)


## Contract Query

After successfully connecting to the trading interface, users can query contract information through the contract query function:
Click [Help] -> [Query Contracts] in the menu bar, and directly click the [Query] button in the upper right corner of the dialog box that pops up to query contract information (leave blank to query all contract price information), as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/3.png)

Please note that because the IB interface cannot automatically obtain all contract information when logging in, it can only be obtained when the user manually subscribes to market data. Therefore, you need to manually subscribe to contract market data on the main interface before you can query contract information.


## Subscribing to Market Data

Enter the exchange and contract code in the trading component, and press the Enter key to subscribe to market data. For example, when subscribing to stock index futures market data, fill in CFFEX for the exchange and fill in the corresponding contract code IF2206 for the code.

After successful subscription, the trading component will display the contract name, and display the depth market data quote below, such as the latest price, bid one price, and ask one price. The market data component will display the latest market data information, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/quick_start/24.png)

Please note that **the input contract code needs to be consistent with what is queried in the menu bar [Help] -> [Query Contracts] function**.


## Order Trading

The trading component is used to manually initiate order trading. In addition to filling in the exchange and contract code, you also need to fill in the five fields in the figure below (direction, open/close, type, price, and quantity):

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/quick_start/5.png)

Please note that if the order type is a market order, the order price does not need to be filled; if the trading interface only supports one-way positions (see trading interface section for interface position direction support), the open/close direction does not need to be filled.

After sending the order, the local will cache the order-related information and display it in the [Order] component and [Active] component. At this time, the order status is [Submitting].

After the exchange receives the order sent by the user, it will insert it into the central order book for matching and push the order report to the user:
- If the order has not been executed, the [Order] component and [Active] component will only update the time and order status fields, and the order status becomes [Not Executed];
- If the order is executed immediately, the order-related information will be removed from the [Active] component and added to the [Transaction] component, and the order status becomes [Fully Executed].


## Data Monitoring

Data monitoring consists of the following components and comes with two auxiliary functions:

Select any of the following components, right-click to select [Adjust Column Width] (especially suitable for low screen resolution situations) or select [Save Data] (CSV format), as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/quick_start/12.png)

### Market Data Component

The market data component is used to monitor subscribed market data in real-time, as shown below:

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/subcribe_contract_module.png)

The market data component monitoring content includes the following parts:

- Contract information: contract code, exchange, contract name;
- Market data information: latest price, trading volume, opening price, highest price, lowest price, closing price, bid 1 price, bid 1 volume, ask 1 price, ask 1 volume;
- Other information: data push time, interface.

### Active Component

The active component is used to store orders that have not been executed yet, such as limit orders or market orders that were not executed immediately. In this component, double-click any order to complete the cancellation operation, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/quick_start/15.png)

### Transaction Component

The transaction component is used to store executed orders. In this component, price, quantity, and time are all transaction information pushed by the exchange, not order information, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/quick_start/14.png)

### Order Component

The order component is used to store all order information sent by users. Its order status can be submitting, cancelled, partially executed, fully executed, rejected, etc., as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/quick_start/13.png)

### Position Component

The position component is used to record historical positions. You need to pay attention to the following field information.

- Direction: Futures varieties have long/short directions, while stock variety direction is [Net] position;
- Quantity: Total position, i.e., today's position + yesterday's position;
- Yesterday's Position: Its appearance derives from the need for the SHFE's unique flat today/flat yesterday mode;
- Average Price: Average price of historical transactions (for some huge orders, multiple partial executions may occur, requiring average price calculation);
- Profit/Loss: Position profit/loss. In long position, profit = current price - average price, short position is vice versa.

If you close the position and leave the market, the position quantity clears to zero, and floating profit/loss becomes actual profit/loss affecting account balance changes. Therefore, the following fields: quantity, yesterday's position, frozen, average price, profit/loss are all 0, as shown below:

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/query_position.png)


### Capital Component

The capital component displays the basic information of the account, as shown below:

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/quick_start/query_account.png)

You need to pay attention to the following three field information:

- Available Capital: Cash that can be used for orders
- Frozen: Amount frozen by order operations (not the same concept as margin)
- Balance: Total capital, i.e., available capital + margin + floating profit/loss

If all positions are closed, floating profit/loss becomes actual profit/loss, margin and floating profit/loss clear to zero, and total capital equals available capital.

### Log Component

The log component is used to display interface login information and order error information, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/1.png)


## Application Modules

VeighNa officially provides ready-to-use quantitative trading application modules. Check the required functional modules when starting VeighNa Trader. After successful startup, click the [Function] button in the menu bar to display the checked functional modules, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/quick_start/25.png)


## Global Configuration

Click the [Configuration] button on the VeighNa Trader menu bar to pop up the [Global Configuration] window, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/quick_start/20.png)

### GUI Interface

The font.family and font.size parameters are used to configure the GUI interface. The meanings of each parameter are as follows:

- font.family: Sets the font type of the VeighNa Trader graphical interface. In addition to the default Arial font, it also supports Courier New and System fonts;

- font.size: Sets the font size of the VeighNa Trader graphical interface. Users can modify the font size according to the actual resolution of their display.

### Log Output

log.active, log.level, log.console, and log.file are used to configure log output. The meanings of each parameter are as follows:

- log.active: Controls whether to start LogEngine, default is True. If this item is modified to False, the subsequent parameters will become invalid, and VeighNa Trader will no longer output logs or generate log files during operation (can reduce some system latency);

- log.level: Controls the log output level. Logs can be divided into five levels from light to severe: DEBUG, INFO, WARNING, ERROR, CRITICAL, corresponding to integer values 10, 20, 30, 40, 50 respectively. If the log level is lower than the set value of this item, it will be ignored. If you want to record more detailed system operation information, it is recommended to lower the integer value of this item;

- log.console: console refers to the terminal, such as cmd and Powershell on Windows systems, and Terminal on Linux. When set to True, run the script through the terminal (requires registering log event listener) to start VeighNa Trader, and log information will be output in the terminal; if VeighNa Trader is started directly through VeighNa Station, there is no console output;

- log.file: This parameter is used to control whether to output logs to a file. It is recommended to set it to True, otherwise generated logs cannot be recorded.

VeighNa Trader log files are located in the .vntrader\log directory under the run directory by default, with the full path:
```
C:\users\administrator\.vntrader\log
```

Where administrator is the login username of the current Windows system.

### Email Notification

Parameters prefixed with email are used to configure the mailbox. Emails can be sent to notify in real-time when specific events occur (such as order execution, data anomalies, etc.). The meanings of each parameter are as follows:

- email.server: SMTP mail server address, default filled with QQ email server address, can be used directly. If you need to use other email boxes, you need to find other server addresses yourself;
- email.port: SMTP mail server port number, default filled with QQ email server port, can be used directly;
- email.username: Fill in the email address, such as xxxx@qq.com;
- email.password: For QQ email, this is not the email password, but an authorization code generated by the system after enabling SMTP;
- email.sender: Sending email name, consistent with email.username;
- email.receiver: Receiving email address.


### datafeed Data Service

Similar to database adapters, there is a standardized interface BaseDatafeed for data services (located in vnpy.trader.datafeed), implementing more flexible data service support. The specific field meanings are as follows:

- datafeed.name: The name of the data service interface, lowercase English letters in full;
- datafeed.username: The username for the data service;
- datafeed.password: The password for the data service.

The fields are shown in the figure:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/quick_start/17.png)

Currently supports seven datafeeds:
- [XT]
- [RQData]
- [Udata]
- [TuShare]
- [TQSDK]
- [Wind]
- [iFinD]
- [Tinysoft]

[XT]:https://github.com/vnpy/vnpy_xt
[RQData]:https://github.com/vnpy/vnpy_rqdata
[Udata]: https://github.com/vnpy/vnpy_udata
[TuShare]: https://github.com/vnpy/vnpy_tushare
[TQSDK]: https://github.com/vnpy/vnpy_tqsdk
[Wind]:https://github.com/vnpy/vnpy_wind
[iFinD]: https://github.com/vnpy/vnpy_ifind
[Tinysoft]: https://github.com/vnpy/vnpy_tinysoft


### Database

Parameters prefixed with database are used to configure database services. Currently, VeighNa supports eight databases: SQLite, MySQL, PostgreSQL, MongoDB, InfluxDB, DolphinDB, Arctic, and LevelDB. For specific configuration methods, please refer to the database configuration section of the project documentation.
