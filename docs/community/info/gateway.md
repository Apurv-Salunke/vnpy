# Trading Interface

## Loading and Starting

### VeighNa Station Loading

After starting and logging into VeighNa Station, click the [Trading] button, and check the trading interfaces you want to trade in the [Trading Interface] column of the configuration dialog box.

### Script Loading

Taking the CTP interface as an example, add the following code to the startup script:

```python3
# Write at the top
from vnpy_ctp import CtpGateway

# Write after creating the main_engine object
main_engine.add_gateway(CtpGateway)
```


## Connecting Interface

In the graphical operation interface VeighNa Trader, click [System] -> [Connect CTP] in the menu bar, and the account configuration window will pop up, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/gateway/1.png)

Enter account, password, and other relevant information to connect to the interface and immediately perform query work: such as querying account information, querying positions, querying order information, querying transaction information, etc. After successful query, you can see the output log in the main interface components, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/gateway/5.png)

### Modifying json Configuration Files

Interface configuration-related information is saved in json files, placed in the .vntrader folder under the user directory, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/gateway/3.png)

If you need to modify the interface configuration file, users can either modify it within the VeighNa Trader graphical interface or directly modify the corresponding json file under the .vntrader folder.

Additionally, separating the json configuration file from vnpy has the benefit of avoiding the need to reconfigure the json file every time you upgrade.

### Viewing Tradable Contracts

First log in to the interface, then click [Help] -> [Query Contracts] in the menu bar to pop up a blank [Query Contracts] window. Click the [Query] button to display the query results. Leave blank to query all contracts, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/gateway/4.png)


## Interface Classification

| Interface                 |                    Type                         |
| ---------------------| :--------------------------------------------: |
| CTP                  |           Futures, Futures Options (Live 6.5.1)            |
| CTP Test              |           Futures, Futures Options (Test 6.5.1)            |
| CTP Mini            |            Futures, Futures Options (Live 1.4)             |
| Femas                 |                    Futures                         |
| CTP Option              |             ETF Options (Live 20190802)              |
| Vertex Feichuang             |                    ETF Options                       |
| Vertex HTS              |                    ETF Options                       |
| Hundsun UFT              |                Futures, ETF Options                     |
| Esunny                 |                Futures, Gold TD                      |
| Zhongtai XTP              |              A-shares, Margin Trading, ETF Options                  |
| Guotai Junan Unified Trading Gateway   |                    A-shares                          |
| Huaxin Qidian Stock          |                    A-shares                          |
| Huaxin Qidian Option          |                  ETF Options                        |
| Comstar       |                Interbank Market                       |
| Oriental Securities OST           |                    A-shares                          |
| Interactive Brokers              |                 Overseas Multi-variety                      |
| Esunny 9.0 Foreign              |                  Foreign Futures                       |
| Direct Futures              |                  Foreign Futures                       |
| Ronghang                 |                  Futures Asset Management                        |
| TTS                  |                    Futures                         |
| Feishu                  |                  Gold TD                         |
| Kingstar Gold            |                  Gold TD                         |


## Interface Details

### CTP

#### Interface Support

- Operating System
  - Windows
  - Ubuntu

- Trading Varieties
  - Futures
  - Futures Options

- Position Direction
  - Only supports two-way positions

- Historical Data
  - Not provided

#### Related Fields

- Username:
- Password:
- Broker Code:
- Trading Server:
- Market Data Server:
- Product Name:
- Authorization Code:
#### Getting Account

- Simulation Account: Obtain from SimNow website. Just enter the mobile phone number and SMS verification (SMS verification can sometimes only be received during normal working hours on weekdays). SimNow username (InvestorID) is a 6-digit number, broker number is 9999, and provides two sets of environments for intraday simulation trading and after-hours testing. You need to change the password once before using. Please note that the applicable time periods for each simulation environment are different.

- Live Account: Open an account with a futures company, and it can be activated by contacting the account manager. The username is a pure number, and the broker number is also a 4-digit number (each futures company has a different broker number). Additionally, live accounts can also activate simulation trading functions, also by contacting the account manager.

### CTPTEST (CTP Test)

#### Interface Support

- Operating System
  - Windows
  - Ubuntu

- Trading Varieties
  - Futures
  - Futures Options

- Position Direction
  - Only supports two-way positions

- Historical Data
  - Not provided

#### Related Fields

- Username:
- Password:
- Broker Code:
- Trading Server:
- Market Data Server:
- Product Name:
- Authorization Code:

#### Getting Account

Open an account with a futures company, and apply for penetration testing through the account manager.

### MINI (CTP Mini)

#### Interface Support

- Operating System
  - Windows
  - Ubuntu

- Trading Varieties
  - Futures
  - Futures Options

- Position Direction
  - Only supports two-way positions

- Historical Data
  - Not provided

#### Related Fields

- Username:
- Password:
- Broker Code:
- Trading Server:
- Market Data Server:
- Product Name:
- Authorization Code:

#### Getting Account

Open an account with a futures company, and it can be activated by contacting the account manager. The username is a pure number, and the broker number is also a 4-digit number (each futures company has a different broker number). Additionally, live accounts can also activate simulation trading functions, also by contacting the account manager.

### FEMAS

#### Interface Support

- Operating System
  - Windows

- Trading Varieties
  - Futures

- Position Direction
  - Only supports two-way positions

- Historical Data
  - Not provided

#### Related Fields

- Username:
- Password:
- Broker Code:
- Trading Server:
- Market Data Server:
- Product Name:
- Authorization Code:

#### Getting Account

Open an account with a futures company, and it can be activated by contacting the account manager. The username is a pure number, and the broker code is also a 4-digit number (each futures company has a different broker number). Additionally, live accounts can also activate simulation trading functions, also by contacting the account manager.

### SOPT (CTP Option)

#### Interface Support

- Operating System
  - Windows
  - Ubuntu

- Trading Varieties
  - ETF Options

- Position Direction
  - Only supports two-way positions

- Historical Data
  - Not provided

#### Related Fields

- Username:
- Password:
- Broker Code:
- Trading Server:
- Market Data Server:
- Product Name:
- Authorization Code:

#### Getting Account

Open an account with a futures company, and it can be activated by contacting the account manager. The username is a pure number, and the broker code is also a 4-digit number (each futures company has a different broker code). Additionally, live accounts can also activate simulation trading functions, also by contacting the account manager.

### SEC (Vertex Feichuang)

#### Interface Support

- Operating System
  - Windows

- Trading Varieties
  - ETF Options

- Position Direction
  - Stocks only support one-way positions
  - Stock options only support two-way positions

- Historical Data
  - Not provided

#### Related Fields

- Account:
- Password:
- Market Data Address:
- Trading Address:
- Market Data Protocol: TCP, UDP
- Authorization Code:
- Product Number:
- Collection Type: Vertex, Hundsun, Kingstar, Kingstar
- Market Data Compression: N, Y

#### Getting Account

Open an account with a futures company, and it can be activated by contacting the account manager.

### HTS (Vertex HTS)

#### Interface Support

- Operating System
  - Windows

- Trading Varieties
  - ETF Options

- Position Direction
  - Two-way positions

- Historical Data
  - Not provided

#### Related Fields

- Account:
- Password:
- Market Data Address:
- Trading Address:
- Market Data Protocol: TCP, UDP
- Authorization Code:
- Product Number:
- Collection Type: Vertex, Hundsun, Kingstar, Kingstar
- Market Data Compression: N, Y

#### Getting Account

Open an account with a futures company, and it can be activated by contacting the account manager.

### UFT (Hundsun UFT)

#### Interface Support

- Operating System
  - Windows
  - Ubuntu

- Trading Varieties
  - Futures
  - ETF Options

- Position Direction
  - Only supports two-way positions

- Historical Data
  - Not provided

#### Related Fields

- Username:
- Password:
- Market Data Server:
- Trading Server:
- Server Type: Futures, ETF Options
- Product Name:
- Authorization Code:
- Order Type: q

#### Getting Account

Please apply for test accounts through Hundsun Electronics.

### ESUNNY (Esunny)

#### Interface Support

- Operating System
  - Windows
  - Ubuntu

- Trading Varieties
  - Futures
  - Gold TD

- Position Direction
  - Supports two-way positions

- Historical Data
  - Not supported

#### Related Fields

- Market Data Account:
- Market Data Password:
- Market Data Server:
- Market Data Port: 0
- Market Data Authorization Code:
- Trading Account:
- Trading Password:
- Trading Server:
- Trading Port: 0
- Trading Product Name:
- Trading Authorization Code:
- Trading System: Domestic, Foreign

#### Getting Account

Please apply for test accounts through the Esunny official website.

### XTP (Zhongtai Counter)

#### Interface Support

- Operating System
  - Windows
  - Ubuntu

- Trading Varieties
  - A-shares
  - Margin Trading
  - ETF Options

- Position Direction
  - Stocks only support one-way positions
  - Other instruments support two-way positions

- Historical Data
  - Not provided

#### Related Fields

- Account:
- Password:
- Client Number: 1
- Market Data Address:
- Market Data Port: 0
- Trading Address:
- Trading Port: 0
- Market Data Protocol: TCP, UDP
- Log Level: FATAL, ERROR, WARNING, INFO, DEBUG, TRACE
- Authorization Code:

#### Getting Account

Please apply for test accounts through Zhongtai Securities.

#### Other Features

XTP is the first to provide margin trading for ultra-fast counters.

### HFT (Guotai Junan Unified Trading Gateway)

#### Interface Support

- Operating System
  - Windows

- Trading Varieties
  - A-shares

- Position Direction
  - Only supports one-way positions

- Historical Data
  - Not provided

#### Related Fields

- Trading Username:
- Trading Password:
- Trading Server:
- Trading Port:
- Institution Code:
- Branch Code:
- Gateway:
- Market Data Username:
- Market Data Password:
- Market Data Server:
- Market Data Port:

#### Getting Account

Please apply for test accounts through Guotai Junan.

### TORASTOCK (Huaxin Qidian Stock)

#### Interface Support

- Operating System
  - Windows

- Trading Varieties
  - A-shares

- Position Direction
  - Only supports one-way positions

- Historical Data
  - Not provided

#### Related Fields

- Account:
- Password:
- Market Data Server:
- Trading Server:
- Account Type: User Code, Fund Account
- Address Type: Front Address, FENS Address

#### Getting Account

Please apply for test accounts through Huaxin Securities.

### TORAOPTION (Huaxin Qidian Option)

#### Interface Support

- Operating System
  - Windows

- Trading Varieties
  - ETF Options

- Position Direction
  - Only supports two-way positions

- Historical Data
  - Not provided

#### Related Fields

- Account:
- Password:
- Market Data Server:
- Trading Server:
- Account Type: User Code, Fund Account
- Address Type: Front Address, FENS Address

#### Getting Account

Please apply for test accounts through Huaxin Securities.

### COMSTAR

#### Interface Support

- Operating System
  - Windows

- Trading Varieties
  - Interbank Market

- Position Direction
  - None

- Historical Data
  - Not provided

#### Related Fields

- Trading Server:
- Username:
- Password:
- Key:
- routing_type: 5
- valid_until_time: 18:30:00.000

#### Getting Account

Only various large financial institutions can use it (securities proprietary trading departments, bank financial market departments, etc.), private equity or individuals cannot use it. You need to purchase ComStar's trading interface service before using it.

### OST (Oriental Securities)

#### Interface Support

- Operating System
  - Windows

- Trading Varieties
  - A-shares

- Position Direction
  - One-way positions

- Historical Data
  - Not provided

#### Related Fields

- Username:
- Password:
- Trading Server:
- SSE Snapshot Address:
- SSE Snapshot Port: 0
- SZSE Snapshot Address:
- SZSE Snapshot Port: 0
- Local IP Address:

#### Getting Account

Open an account with a securities company, and it can be activated by contacting the account manager.

### IB (Interactive Brokers)

#### Interface Support

- Operating System
  - Windows
  - Ubuntu
  - Mac

- Trading Varieties
  - Overseas Multi-variety

- Position Direction
  - Only supports one-way positions

- Historical Data
  - Provided

#### Related Fields

- TWS Address: 127.0.0.1
- TWS Port: 7497
- Client Number: 1
- Trading Account:

#### Getting Account

Open an account with Interactive Brokers and deposit funds to obtain API access permissions.

#### Other Features

Tradable varieties cover stocks, options, and futures in many overseas markets; commission fees are relatively low.

Please note that the IB interface contract code is more special, please go to the product query section of the official website to query. VeighNa Trader uses Interactive Brokers' unique identifier ConId for each contract on a certain exchange as the contract code, rather than Symbol or LocalName.

### TAP (Esunny 9.0 Foreign)

#### Interface Support

- Operating System
  - Windows

- Trading Varieties
  - Foreign Futures

- Position Direction
  - Only supports one-way positions

- Historical Data
  - Not provided

#### Related Fields

- Market Data Account:
- Market Data Password:
- Market Data Server:
- Market Data Port: 0
- Trading Account:
- Trading Password:
- Trading Server:
- Trading Port: 0
- Authorization Code:

#### Getting Account

Please apply for test accounts through the Esunny official website.

### DA (Direct Futures)

#### Interface Support

- Operating System
  - Windows

- Trading Varieties
  - Foreign Futures

- Position Direction
  - Only supports two-way positions

- Historical Data
  - Not provided

#### Related Fields

- Username:
- Password:
- Trading Server:
- Market Data Server:
- Authorization Code:

#### Getting Account

Open an account with Direct Futures and deposit funds to obtain API access permissions.

### ROHON (Ronghang)

#### Interface Support

- Operating System
  - Windows
  - Ubuntu

- Trading Varieties
  - Futures Asset Management

- Position Direction
  - Only supports two-way positions

- Historical Data
  - Not provided

#### Related Fields

- Username:
- Password:
- Broker Code:
- Trading Server:
- Market Data Server:
- Product Name:
- Authorization Code:

#### Getting Account

Please apply for test accounts through Ronghang.

Please note that the [Broker Code] for the Ronghang interface is no longer in pure numeric form, but can be a string containing English letters and numbers; VeighNa connecting to Ronghang for trading belongs to the [Relay] mode in penetration authentication, rather than the [Direct Connection] mode when connecting to counters (CTP, Hundsun, etc.) for trading, so do not make a mistake when filling out the form for penetration authentication testing.

### TTS

#### Interface Support

- Operating System
  - Windows
  - Ubuntu

- Trading Varieties
  - Futures
  - Futures Options

- Position Direction
  - Only supports two-way positions

- Historical Data
  - Not provided

#### Related Fields

- Username:
- Password:
- Broker Code:
- Trading Server:
- Market Data Server:
- Product Name:
- Authorization Code:

#### Getting Account

Please obtain through the OpenCTP platform.

### SGIT (Feishu)

#### Interface Support

- Operating System
  - Ubuntu

- Trading Varieties
  - Gold TD

- Position Direction
  - Only supports two-way positions

- Historical Data
  - Not provided

#### Related Fields

- Username:
- Password:
- Trading Server:
- Market Data Server:
- Product Name:
- Authorization Code:

#### Getting Account

Please obtain through gold spot brokers.

### KSGOLD (Kingstar Gold)

#### Interface Support

- Operating System
  - Ubuntu

- Trading Varieties
  - Gold TD

- Position Direction
  - Only supports two-way positions

- Historical Data
  - Not provided

#### Related Fields

- Username:
- Password:
- Trading Server:
- Market Data Server:
- Account Type: Bank Account, Gold Account

#### Getting Account

Please obtain through gold spot brokers.
