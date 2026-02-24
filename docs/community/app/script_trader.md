# ScriptTrader - Script Strategy Trading Module

## Function Overview

ScriptTrader is a functional module for **script strategy trading**, providing interactive quantitative analysis and programmatic trading functions, as well as script strategy functions that run continuously as a whole strategy.

Therefore, it can be regarded as directly using Python to operate the trading client. Its difference from the CTA strategy module lies in:

- Breaking through the limitations of single exchange and single underlying;
- Can more easily implement hedging strategies between stock index futures and a basket of stocks, cross-variety arbitrage, stock market scanning automated stock selection, and other functions.

## Loading and Launching

### Loading via VeighNa Station

After launching and logging into VeighNa Station, click the [Trading] button. In the configuration dialog, check [ScriptTrader] in the [Application Module] section.

### Loading via Script

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_scripttrader import ScriptTraderApp

# Write after creating the main_engine object
main_engine.add_app(ScriptTraderApp)
```

## Starting the Module

Before starting the module, please connect to the trading interface first (for connection methods, see the Interface Connection section in the Basic Usage chapter). After seeing "Contract information query successful" output in the [Log] section of the VeighNa Trader main interface, start the module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/1.png)

Please note that because the IB interface cannot automatically obtain all contract information upon login, it can only be obtained when the user manually subscribes to market data. Therefore, you need to manually subscribe to contract market data on the main interface before starting the module.

After successfully connecting to the trading interface, click [Function] -> [Script Strategy] in the menu bar, or click the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/0.png)

You can then enter the UI interface of the script trading module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/1.png)

If a data service is configured (for configuration methods, see the Global Configuration section in the Basic Usage chapter), data service login initialization is automatically executed when opening the script trading module. If login is successful, "Data service initialization successful" log will be output, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/20.png)

Users can use the following functions through the UI interface:

### Start

Script strategies need to be written in advance, such as test_strategy.py (for script strategy templates, please refer to the [**Script Strategy**](#jump) section). Therefore, after clicking the [Open] button, users need to specify the path of the script strategy file, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/21.png)

After opening the script strategy, click the [Start] button to start the script strategy, and relevant information will be output in the interface below, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/8.png)

### Stop

If you want to stop the script strategy, directly click the [Stop] button. After that, the strategy will stop, and a notification will output "Strategy trading script stopped" log in the interface below, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/11.png)

### Clear

If you feel there is too much information displayed in the interface below, or want to start a new script strategy, you can click the [Clear] button. At this time, all information below will be cleared, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/10.png)


## Script Strategy Template

<span id="jump">

Script strategy files need to be written following a certain format. The following provides a usage template, which functions as:

- Subscribe to market data for two varieties;
- Print contract information;
- Get latest market data every 3 seconds.

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
        msg = f"Contract information, {contract}"
        engine.write_log(msg)

    # Continue running, use strategy_active to judge whether to exit the program
    while engine.strategy_active:
        # Poll to get market data
        for vt_symbol in vt_symbols:
            tick = engine.get_tick(vt_symbol)
            msg = f"Latest market data, {tick}"
            engine.write_log(msg)

        # Wait 3 seconds to enter the next round
        sleep(3)
```

Among them, engine.strategy_active is used to control the While loop, which can be regarded as the switch of the script strategy:

- Click the [Start] button to start the While loop and execute the script strategy;
- Click the [Stop] button to exit the While loop and stop the script strategy.


## Function Functions

Jupyter mode is driven by the script engine (ScriptEngine). The following explains the function functions of the ScriptEngine engine through jupyter notebook.

First, open Jupyter notebook, then load components and initialize the script engine:

```python3
from vnpy_scripttrader import init_cli_trading
from vnpy_ctp import CtpGateway
engine = init_cli_trading([CtpGateway])
```

Among them:

- The script engine can support connecting multiple interfaces simultaneously;
- init_cli_trading(gateways: Sequence[BaseGateway]) can pass multiple interface classes to init_cli_trading in the form of a list;
- init_cli_trading can be regarded as a wrapped initialization startup function by vnpy, encapsulating various objects such as main engine and script engine.

### Connecting Interfaces

**connect_gateway**

* Input: setting: dict, gateway_name: str

* Output: None

Different interfaces require different configuration parameters. SimNow configuration is as follows:
```json
setting = {
    "Username": "xxxx",
    "Password": "xxxx",
    "Broker ID": "9999",
    "Trading Server": "180.168.146.187:10202",
    "Market Data Server": "180.168.146.187:10212",
    "Product Name": "simnow_client_test",
    "Auth Code": "0000000000000000"
}
engine.connect_gateway(setting, "CTP")
```

Other interface configurations can be filled in according to default_setting in different interface module classes (such as vnpy_ctp.gateway.ctp_gateway) under the site-packages directory.

### Subscribing to Market Data

**subscribe**

* Input: vt_symbols: Sequence[str]

* Output: None

The subscribe() function is used to subscribe to market data information. If you need to subscribe to market data for a basket of contracts, you can use list format.
```python3
engine.subscribe(vt_symbols = ["rb2209.SHFE", "rb2210.SHFE"])
```

### Querying Data
Here describes data storage after connecting to the trading interface and successfully subscribing to data:

- The underlying interface continuously pushes new data to the main engine;
- The main engine maintains a ticks dictionary to cache the latest tick data for different underlyings (only the latest data can be cached);
- The function of use_df is to convert to DataFrame format for data analysis.

#### Single Query

**get_tick**

* Input: vt_symbol: str, use_df: bool = False

* Output: TickData

Query the latest tick for a single underlying. use_df is an optional parameter used to convert the returned class object to DataFrame format for data analysis.

```python3
tick = engine.get_tick(vt_symbol="rb2210.SHFE", use_df=False)
```

Among them:

- vt_symbol: is the local contract code, format is contract variety + exchange, such as rb2210.SHFE;
- use_df: is a bool variable, default is False, returns TickData class object, otherwise returns corresponding DataFrame, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/13.png)

**get_order**

* Input: vt_orderid: str, use_df: bool = False

* Output: OrderData

Query detailed information of orders according to vt_orderid.

```python3
order = engine.get_order(vt_orderid="CTP.3_-1795780178_1", use_df=False)
```

Among them, vt_orderid is the local order number (when placing orders, the vt_orderid of the order will be automatically returned).
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/14.png)

**get_contract**

* Input: vt_symbol, use_df: bool = False

* Output: ContractData

Query detailed information of corresponding contract objects according to local vt_symbol.

```python3
contract = engine.get_contract(vt_symbol="rb2210.SHFE", use_df=False)
```
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/15.png)

**get_account**

* Input: vt_accountid: str, use_df: bool = False

* Output: AccountData

Query corresponding capital information according to local vt_accountid.

```python3
account = engine.get_account(vt_accountid="CTP.189672", use_df=False)
```
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/16.png)

**get_position**

* Input: vt_positionid: str, use_df: bool = False

* Output: PositionData

Query position status according to vt_positionid. The returned object contains interface name, exchange, contract code, quantity, frozen quantity, etc.

```python3
position = engine.get_position(vt_positionid='CTP.hc2305.SHFE.Long')
```
Note that vt_positionid is vnpy's internal unique position number for a specific position. The format is "gateway_name.vt_symbol.Direction.value", where position direction can be "Long", "Short", or "Net", as shown in the figure below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/17.png)

#### Multiple Queries

**get_ticks**

* Input: vt_symbols: Sequence[str], use_df: bool = False

* Output: Sequence[TickData]

Query the latest ticks for multiple contracts.

```python3
ticks = engine.get_ticks(vt_symbols=['rb2209.SHFE', 'rb2210.SHFE'], use_df=True)
```

vt_symbols is in list format, containing multiple vt_symbols, as shown in the figure.
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/18.png)


**get_orders**

* Input: vt_orderids: Sequence[str], use_df: bool = False

* Output: Sequence[OrderData]

Query detailed information according to multiple vt_orderids. vt_orderids is a list containing multiple vt_orderids.

```python3
orders = engine.get_orders([orderid_one, orderid_two], use_df=True)
```

**get_trades**

* Input: vt_orderid: str, use_df: bool = False

* Output: Sequence[TradeData]

Return all TradeData objects in this order process according to a given vt_orderid. vt_orderid is the local order number. Each order OrderData can correspond to multiple trade TradeData due to partial execution relationships.

```python3
trades = engine.get_trades(vt_orderid=your_vt_orderid, use_df=True)
```

**get_bars**

* Input: vt_symbol: str, start_date: str, interval: Interval, use_df: bool = False

* Output: Sequence[BarData]

Query historical data through configured data services.

```python3
bars = engine.get_bars(vt_symbol="rb2210.SHFE", start_date="20211201",
                        interval=Interval.MINUTE, use_df=False)
```

Among them:

- vt_symbol: local contract code, format is contract code + exchange name;
- start_date: start date, format is "%Y%m%d";
- interval: K-line period, including: minute, hour, day, week;
- bars: list object containing a series of BarData data. Its BarData definition is as follows:
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

In full query, the only parameter is use_df, defaulting to False. Returns a List object containing corresponding data, such as ContractData, AccountData, and PositionData.

**get_all_contracts**

* Input: use_df: bool = False

* Output: Sequence[ContractData]

By default, returns a list containing ContractData of the entire market. If use_df=True, returns the corresponding DataFrame.

**get_all_active_orders**

* Input: use_df: bool = False

* Output: Sequence[OrderData]

Active orders refer to orders waiting to be fully executed, so their status includes "submitted, not filled, partially filled"; the function will return a list object containing a series of OrderData.

**get_all_accounts**

* Input: use_df: bool = False

* Output: Sequence[AccountData]

By default, returns a list object containing AccountData.

**get_all_positions**

* Input: use_df: bool = False

* Output: Sequence[PositionData]

By default, returns a list object containing PositionData, as shown in the figure below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/script_trader/19.png)

### Trading Orders

**buy**: Buy to open (Direction: LONG, Offset: OPEN)

**sell**: Sell to close (Direction: SHORT, Offset: CLOSE)

**short**: Sell to open (Direction: SHORT, Offset: OPEN)

**cover**: Buy to close (Direction: LONG, Offset: CLOSE)

* Input: vt_symbol: str, price: float, volume: float, order_type: OrderType = OrderType.LIMIT

* Output: str

Taking order buy as an example, the engine.buy() function input parameters include:

- vt_symbol: local contract code (string format);
- price: order price (float type);
- volume: order quantity (float type);
- order_type: OrderType enumeration constant, defaults to limit order (OrderType.LIMIT), also supports stop orders (OrderType.STOP), FAK (OrderType.FAK), FOK (OrderType.FOK), market orders (OrderType.MARKET). Different exchanges support different order methods.
```python3
engine.buy(vt_symbol="rb2210.SHFE", price=4200, volume=1, order_type=OrderType.LIMIT)
```

After executing the trading order, the local order number vt_orderid will be returned.

**send_order**

* Input: vt_symbol: str, price: float, volume: float, direction: Direction, offset: Offset, order_type: OrderType

* Output: str

The send_order function is a function for sending orders called by the script trading strategy engine. Generally, you do not need to call it separately when writing strategies. You can send orders through buy/sell/short/cover functions.

**cancel_order**

* Input: vt_orderid: str

* Output: None

Cancel orders based on local order number.

```python3
engine.cancel_order(vt_orderid='CTP.3_-1795780178_1')
```

### Information Output

**write_log**

* Input: msg: str

* Output: None

Calling the write_log function in the strategy can output logs with specified content.

**send_email**

* Input: msg: str

* Output: None

After configuring email related information (for configuration methods, see the Global Configuration section in the Basic Usage chapter), calling the send_email function can send an email with the subject "Script Strategy Engine Notification" to your email address.
