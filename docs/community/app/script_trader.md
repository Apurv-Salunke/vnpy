# ScriptTrader - Script Strategy Trading Module

## Function Overview

ScriptTrader is a functional module designed for **script strategy trading**. It provides interactive quantitative analysis and programmatic trading functions, as well as the script strategy function that runs the entire strategy continuously.

It can be seen as directly using Python to operate the trading client. The difference between it and the CTA strategy module is:

- It breaks the limitation of single exchange and single target;
- It can easily implement functions such as hedging strategies between stock index futures and a basket of stocks, cross-market arbitrage, and stock market scanning automated stock selection.

## Loading and Starting

### VeighNa Station Loading

After logging into VeighNa Station, click the 【Trading】 button, and in the configuration dialog box, check the 【ScriptTrader】 box under the 【Application Modules】 column.

### Script Loading

Add the following code to your script:

```python3
# At the top
from vnpy_scripttrader import ScriptTraderApp

# After creating the main_engine object
main_engine.add_app(ScriptTraderApp)
```

## Starting the Module

Before starting the module, please connect to the trading interface (the connection method is detailed in the basic usage section of the connection interface). After seeing the "Contract Information Query Successful" output in the VeighNa Trader main interface 【Log】 column, start the module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/1.png)

Please note that the IB interface cannot automatically obtain all contract information when logging in, and can only obtain it when the user manually subscribes to market data. Therefore, you need to manually subscribe to market data on the main interface before starting the module.

After successfully connecting to the trading interface, click on the 【Function】-> 【Script Strategy】 in the menu bar, or click on the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/0.png)

You can enter the UI interface of the script trading module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/1.png)

If you have configured the data service (the configuration method is detailed in the basic usage section of the global configuration), the data service login initialization will be automatically executed when the script trading module is opened. If the login is successful, the log will output "Data Service Initialization Successful", as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/20.png)

Users can use the following functions through the UI interface:

### Start

The script strategy needs to have the script strategy file written in advance, such as test_strategy.py (the script strategy template can refer to the [**Script Strategy**](#jump) section). Therefore, after clicking the 【Open】 button, the user needs to specify the path of the script strategy file, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/21.png)

After opening the script strategy, click the 【Start】 button to start the script strategy, and output the relevant information in the lower interface, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/8.png)

### Stop

If you want to stop the script strategy, just click the 【Stop】 button, and then the strategy will stop, and the notification will output "Script Trading Script Stopped" in the lower interface, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/11.png)

### Clear

If you think there is too much information displayed in the lower interface, or if you want to start a new script strategy, you can click the 【Clear】 button, and all the information in the lower interface will be cleared, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/10.png)


## Script Strategy Template

<span id="jump">

The script strategy file writing needs to follow a certain format. The template is provided below, and its function is:

- Subscribe to the market data of two varieties;
- Print contract information;
- Get the latest market data every 3 seconds.

```python3
from time import sleep
from vnpy_scripttrader import ScriptEngine

def run(engine: ScriptEngine):
    """"""
    vt_symbols = ["sc2209.INE", "sc2203.INE"]

    # Subscribe to market data
    engine.subscribe(vt_symbols)

    # Get contract information
    for vt_symbol in vt_symbols:
        contract = engine.get_contract(vt_symbol)
        msg = f"Contract Information, {contract}"
        engine.write_log(msg)

    # Continuous operation, use strategy_active to determine whether to exit the program
    while engine.strategy_active:
        # Polling to get market data
        for vt_symbol in vt_symbols:
            tick = engine.get_tick(vt_symbol)
            msg = f"Latest Market Data, {tick}"
            engine.write_log(msg)

        # Wait for 3 seconds to enter the next round
        sleep(3)
```

The engine.strategy_active is used to control the While loop, and can be viewed as the switch of the script strategy:

- Click the 【Start】 button to start the While loop and execute the script strategy;
- Click the 【Stop】 button to exit the While loop and stop the script strategy.


## Function Functions

The Jupyter mode is based on the script engine (ScriptEngine) driven. The various function functions of the ScriptEngine engine are explained below through the jupyter notebook.

First, open the Jupyter notebook, and then load the components and initialize the script engine:

```python3
from vnpy_scripttrader import init_cli_trading
from vnpy_ctp import CtpGateway
engine = init_cli_trading([CtpGateway])
```

Where:

- The script engine can support multiple interfaces connected at the same time;
- init_cli_trading(gateways: Sequence[BaseGateway]) can pass multiple interface classes to init_cli_trading in the form of a list;
- init_cli_trading can be viewed as a well-encapsulated initialization and startup function of vnpy, which has encapsulated various objects such as the main engine, script engine, etc.

### Connect Interface

**connect_gateway**

* Input: setting: dict, gateway_name: str

* Output: None

Different interfaces require different configuration parameters. The configuration of SimNow is as follows:
```json
setting = {
    "Username": "xxxx",
    "Password": "xxxx",
    "Broker ID": "9999",
    "Trade Server":"180.168.146.187:10202",
    "Market Server":"180.168.146.187:10212",
    "Product Name":"simnow_client_test",
    "Authorization Code":"0000000000000000"
}
engine.connect_gateway(setting,"CTP")
```

Other interface configurations can refer to the default_setting in the different interface module classes under the site-packages directory (such as vnpy_ctp.gateway.ctp_gateway).

### Subscribe to Market Data

**subscribe**

* Input: vt_symbols: Sequence[str]

* Output: None

The subscribe() function is used to subscribe to market data. If you need to subscribe to the market data of a basket of contracts, you can use the list format.
```python3
engine.subscribe(vt_symbols = ["rb2209.SHFE","rb2210.SHFE"])
```

### Query Data
Here we introduce the data storage after successfully connecting to the trading interface:

- The underlying interface keeps pushing new data to the main engine;
- The main engine maintains a ticks dictionary for caching the latest tick data of different targets (only the latest data can be cached);
- The use_df is used to convert to DataFrame format, which is convenient for data analysis.

#### Single Query

**get_tick**

* Input: vt_symbol: str, use_df: bool = False

* Output: TickData

Query the latest tick of a single target. use_df is an optional parameter, used to convert the returned class object to DataFrame format, which is convenient for data analysis.

```python3
tick = engine.get_tick(vt_symbol="rb2210.SHFE",use_df=False)
```

Where:

- vt_symbol: is the local contract code, in the format of contract variety + exchange, such as rb2210.SHFE;
- use_df: is a bool variable, default is False, return TickData class object, otherwise return the corresponding DataFrame, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/13.png)

**get_order**

* Input: vt_orderid: str, use_df: bool = False

* Output: OrderData

Query the detailed information of an order based on the vt_orderid.

```python3
order = engine.get_order(vt_orderid="CTP.3_-1795780178_1",use_df=False)
```

Where, vt_orderid is the local order number (when placing an order, the vt_orderid of the order will be automatically returned).
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/14.png)

**get_contract**

* Input: vt_symbol, use_df: bool = False

* Output: ContractData

Query the detailed information of the corresponding contract object based on the local vt_symbol.

```python3
contract = engine.get_contract(vt_symbol="rb2210.SHFE",use_df=False)
```
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/15.png)

**get_account**

* Input: vt_accountid: str, use_df: bool = False

* Output: AccountData

Query the corresponding fund information based on the local vt_accountid.

```python3
account = engine.get_account(vt_accountid="CTP.189672",use_df=False)
```
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/16.png)

**get_position**

* Input: vt_positionid: str, use_df: bool = False

* Output: PositionData

Query the position based on the vt_positionid, and the returned object contains the interface name, exchange, contract code, quantity, frozen quantity, etc.

```python3
position = engine.get_position(vt_positionid='CTP.hc2305.SHFE.多')
```
Note that, vt_positionid is the unique position number for a specific position in vnpy, in the format of "gateway_name.vt_symbol.Direction.value", where the position direction can be "long", "short" and "net", as shown in the figure below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/17.png)

#### Multiple Query

**get_ticks**

* Input: vt_symbols: Sequence[str], use_df: bool = False

* Output: Sequence[TickData]

Query the latest tick of multiple contracts.

```python3
ticks = engine.get_ticks(vt_symbols=['rb2209.SHFE','rb2210.SHFE'],use_df=True)
```

vt_symbols is in list format, containing multiple vt_symbols, as shown in the figure below.
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/18.png)


**get_orders**

* Input: vt_orderids: Sequence[str], use_df: bool = False

* Output: Sequence[OrderData]

Query the detailed information of multiple vt_orderids. vt_orderids is a list, containing multiple vt_orderids.

```python3
orders = engine.get_orders([orderid_one,orderid_two],use_df=True)
```

**get_trades**

* Input: vt_orderid: str, use_df: bool = False

* Output: Sequence[TradeData]

Return all TradeData objects in this order process based on the given vt_orderid. vt_orderid is the local order number, each order OrderData, due to the relationship of partial transactions, can correspond to multiple transactions TradeData.

```python3
trades = engine.get_trades(vt_orderid=your_vt_orderid,use_df=True)
```

**get_bars**

* Input: vt_symbol: str, start_date: str, interval: Interval, use_df: bool = False

* Output: Sequence[BarData]

Query historical data through the configured data service.

```python3
bars = engine.get_bars(vt_symbol="rb2210.SHFE",start_date="20211201",
                        interval=Interval.MINUTE,use_df=False)
```

Where:

- vt_symbol: is the local contract code, in the format of contract code + exchange name;
- start_date: is the start date, in the format of "%Y%m%d";
- interval: is the K-line period, including: minute, hour, day, week;
- bars: is a list object containing a series of BarData data, and its BarData is defined as follows:
```python3
@dataclass
class BarData(BaseData):

    symbol: str
    exchange: Exchange
    datetime: datetime

    interval: Interval = None
    volume: float = 0
    turnover: float = 0
    open_interest: float = 0
    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    close_price: float = 0

    def __post_init__(self):
        self.vt_symbol = f"{self.symbol}.{self.exchange.value}"
```

#### Full Query

In the full query, the only parameter is use_df, which defaults to False. The returned is a List object containing the corresponding data, such as ContractData, AccountData and PositionData.

**get_all_contracts**

* Input: use_df: bool = False

* Output: Sequence[ContractData]

By default, it returns a list containing all ContractData in the market. If use_df=True, it will return the corresponding DataFrame.

**get_all_active_orders**

* Input: use_df: bool = False

* Output: Sequence[OrderData]

Active orders refer to orders that are waiting for complete execution, so their status includes "submitted, not executed, partially executed"; the function will return a list object containing a series of OrderData.

**get_all_accounts**

* Input: use_df: bool = False

* Output: Sequence[AccountData]

By default, it returns a list object containing AccountData.

**get_all_positions**

* Input: use_df: bool = False

* Output: Sequence[PositionData]

By default, it returns a list object containing PositionData, as shown in the figure below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/19.png)

### Trading Order

**buy**: Buy to open (Direction: LONG, Offset: OPEN)

**sell**: Sell to close (Direction: SHORT, Offset: CLOSE)

**short**: Sell to open (Direction: SHORT, Offset: OPEN)

**cover**: Buy to close (Direction: LONG, Offset: CLOSE)

* Input: vt_symbol: str, price: float, volume: float, order_type: OrderType = OrderType.LIMIT

* Output: str

Taking the buy order as an example, the engine.buy() function input includes:

- vt_symbol: local contract code (string format);
- price: order price (float type);
- volume: order quantity (float type);
- order_type: OrderType enumeration constant, default is limit order (OrderType.LIMIT), and also supports stop order (OrderType.STOP), FAK (OrderType.FAK), FOK (OrderType.FOK), market order (OrderType.MARKET), different exchanges support different order methods.
```python3
engine.buy(vt_symbol="rb2210.SHFE", price=4200, volume=1, order_type=OrderType.LIMIT)
```

After executing the trading order, the local order number vt_orderid will be returned.

**send_order**

* Input: vt_symbol: str, price: float, volume: float, direction: Direction, offset: Offset, order_type: OrderType

* Output: str

The send_order function is the function of sending an order called by the script trading strategy engine. Generally, it is not necessary to call it separately when writing a strategy. You can send an order through the buy/sell/short/cover function.

**cancel_order**

* Input: vt_orderid: str

* Output: None 

Cancel the order based on the local order number.

```python3
engine.cancel_order(vt_orderid='CTP.3_-1795780178_1')
```

### Information Output

**write_log**

* Input: msg: str

* Output: None

By calling the write_log function in the strategy, you can output the specified content of the log.

**send_email**

* Input: msg: str

* Output: None

After configuring the email related information (the configuration method is detailed in the global configuration section of the basic usage), calling the send_email function can send an email titled "Script Strategy Engine Notification" to your email.
