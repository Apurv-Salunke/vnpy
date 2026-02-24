# PortfolioStrategy - Multi-Contract Portfolio Strategy Module

## Function Overview

PortfolioStrategy is a functional module for **multi-contract portfolio strategy live trading**. Users can conveniently complete tasks such as strategy initialization, strategy start, strategy stop, strategy parameter editing, and strategy removal through its UI interface.

## Loading and Launching

### Loading via VeighNa Station

After launching and logging into VeighNa Station, click the [Trading] button. In the configuration dialog, check [PortfolioStrategy] in the [Application Module] section.

### Loading via Script

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_portfoliostrategy import PortfolioStrategyApp

# Write after creating the main_engine object
main_engine.add_app(PortfolioStrategyApp)
```


## Starting the Module

<span id="jump">

For user-developed strategies, they need to be placed in the **strategies** directory under the VeighNa Trader runtime directory to be recognized and loaded. The specific runtime directory path can be viewed in the title bar at the top of the VeighNa Trader main interface.

For users with default installation on Windows, the strategies directory path for placing strategies is usually:

```
    C:\Users\Administrator\strategies
```

Where Administrator is the system username currently logged into Windows.

</span>

Before starting the module, please connect to the trading interface first (for connection methods, see the Interface Connection section in the Basic Usage chapter). After seeing "Contract information query successful" output in the [Log] section of the VeighNa Trader main interface, start the module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/1.png)

Please note that because the IB interface cannot automatically obtain all contract information upon login, it can only be obtained when the user manually subscribes to market data. Therefore, you need to manually subscribe to contract market data on the main interface before starting the module.

After successfully connecting to the trading interface, click [Function] -> [Portfolio Strategy] in the menu bar, or click the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/0.png)

You can then enter the UI interface of the multi-contract portfolio strategy module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/1.png)

If a data service is configured (for configuration methods, see the Global Configuration section in the Basic Usage chapter), data service login initialization is automatically executed when opening the multi-contract portfolio strategy module. If login is successful, "Data service initialization successful" log will be output, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/2.png)


## Adding Strategies

Users can create different strategy instances (objects) based on written portfolio strategy templates (classes).

Select the strategy name to trade from the dropdown box in the upper left corner, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/3.png)

Please note that the displayed strategy name is the name of the **strategy class** (camelCase naming), not the strategy file (underscore naming).

After selecting the strategy class, click [Add Strategy] to pop up the add strategy dialog, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/4.png)

When creating a strategy instance, you need to configure relevant parameters. The parameter requirements are as follows:

- Instance Name
  - Instance names cannot be duplicated;
- Contract Variety
  - Format is vt_symbol (contract code + exchange name);
  - Must be a contract name that can be found in the live trading system;
  - Contract names are separated by ",", without spaces in between;
- Parameter Settings
  - The displayed parameter names are the parameter names written in the parameters list in the strategy;
  - Default values are the default values of parameters in the strategy;
  - As observed in the figure above, the data type of the parameter is displayed in the <> brackets after the parameter name. When filling in parameters, you should follow the corresponding data type. Among them, <class 'str'> is string, <class 'int'> is integer, <class 'float'> is float;
  - Please note that if a parameter may be adjusted to a value with decimal places, and the default parameter value is an integer (such as 1). When writing the strategy, set the default parameter value to a float (such as 1.0). Otherwise, the strategy will default that parameter to an integer, and when subsequently [Editing] the strategy instance parameters, only integers will be allowed.

After parameter configuration is completed, click the [Add] button to start creating the strategy instance. After successful creation, you can see the strategy instance in the strategy monitoring component on the left side, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/5.png)

The top of the strategy monitoring component displays the strategy instance name, strategy class name, and strategy author name (author defined in the strategy). The top buttons are used to control and manage the strategy instance. The first row of the table displays the parameter information inside the strategy (parameter names need to be written in the strategy's parameters list to be displayed in the GUI). The second row of the table displays the variable information during strategy operation (variable names need to be written in the strategy's variables list to be displayed in the GUI). The [inited] field indicates the current initialization status of the strategy (whether historical data playback has been completed), and the [trading] field indicates whether the strategy can currently start trading.

As observed in the figure above, at this time the strategy instance's [inited] and [trading] status are both [False]. This indicates that the strategy instance has not been initialized yet and cannot send trading signals.

After the strategy instance is successfully created, the strategy instance configuration information will be saved to the portfolio_strategy_setting.json file under the .vntrader folder.

Please note that if a strategy instance with the same name is added, creation will fail, and the GUI will output "Strategy creation failed, duplicate name exists" log information, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/8.png)


## Managing Strategies

### Initialization

After the strategy instance is successfully created, you can initialize the instance. Click the [Initialize] button under the strategy instance. If initialization is successful, it is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/6.png)

After initialization is completed, you can observe that the strategy instance's [inited] status is already [True]. This indicates that the strategy instance has loaded historical data and completed initialization. The [trading] status is still [False], indicating that the strategy instance cannot start automatic trading yet.

Please note that, unlike CTA strategies, if incorrect vt_symbol is entered when creating an instance, the multi-contract portfolio strategy module will report an error during initialization, not when creating the strategy instance, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/7.png)

### Start

Only when the strategy instance is initialized successfully and the [inited] status is [True] can the strategy's automatic trading function be started. Click the [Start] button under the strategy instance to start the strategy instance. After success, it is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/10.png)

You can observe that at this time the strategy instance's [inited] and [trading] status are both [True]. This indicates that the strategy instance has completed historical data playback, and at this time the trading request functions inside the strategy (buy/sell/short/cover/cancel_order, etc.) and information output functions (send_email/put_event, etc.) will truly execute and send corresponding request commands to the underlying interface (truly executing trading).

In the previous strategy initialization process, although the strategy was also receiving (historical) data and calling corresponding function functions, because the [trading] status was [False], there were no real order placement operations or trading-related log information output.

If the strategy sends orders after starting, you can view order details in the [Order] bar on the VeighNa Trader main interface, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/9.png)

Please note that, unlike the CTA strategy module, the multi-contract portfolio strategy **does not provide local stop order functionality**, so there will be no stop order display area on the UI interface.


### Stop

If after starting the strategy, due to certain situations (such as market closing time, or encountering emergency situations during trading) you want to stop, edit, or remove the strategy, you can click the [Stop] button under the strategy instance to stop the strategy instance's automatic trading. After success, it is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/11.png)

The portfolio strategy engine will automatically cancel all active orders sent by the strategy before, to ensure that there are no out-of-control orders after the strategy stops. At the same time, the latest variable information of the strategy instance will be saved to the portfolio_strategy_data.json file under the .vntrader folder.

At this time, you can observe that the strategy instance's [trading] status has become [False], indicating that the strategy instance has stopped automatic trading.

During multi-contract portfolio strategy live trading, under normal circumstances, the strategy should run automatically throughout the entire trading period, and extra pause/restart operations should be avoided as much as possible. For the domestic futures market, automatic trading should be started before the trading period begins, and then closed after the market closes. Because now CTP also closes the system after night trading closes and restarts before morning open, so you also need to stop the strategy and close VeighNa Trader after night trading closes.

### Edit

If after creating a strategy instance, you want to edit the parameters of a certain strategy instance (if the strategy has been started, you need to click the [Stop] button under the strategy instance first to stop the strategy), you can click the [Edit] button under the strategy instance, and a parameter editing dialog will pop up for modifying strategy parameters. As shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/12.png)

After editing the strategy parameters, click the [OK] button below, and the corresponding modifications will be immediately updated in the parameter table.

However, the strategy instance's trading contract code cannot be modified, and no re-initialization operation will be executed after modification. Also note that at this time only the parameter values of the strategy instance in the portfolio_strategy_setting.json file under the .vntrader folder are modified, not the parameters in the original strategy file.

Before modification, the json file is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/18.png)


After modification, the json file is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/17.png)

If you want to start the strategy again after editing during trading, click the [Start] button under the strategy instance to start the strategy instance again.

### Remove

If after creating a strategy instance, you want to remove a certain strategy instance (if the strategy has been started, you need to click the [Stop] button under the strategy instance first to stop the strategy), you can click the [Remove] button under the strategy instance. After successful removal, the strategy monitoring component on the left side of the GUI will no longer display the strategy instance information. As shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/13.png)

At this time, the portfolio_strategy_setting.json file under the .vntrader folder has also removed the configuration information of the strategy instance.

### Status Tracking

If you want to track the strategy status through the GUI, there are two ways:

1. Call the put_event function

   All variable information in the strategy instance needs to have the variable name written in the strategy's variables list to be displayed in the GUI. If you want to track variable status changes, you need to call the put_event function in the strategy, and the interface will refresh the data.

   Sometimes users find that no matter how long their strategy runs, the variable information does not change. In this case, please check whether the call to the put_event function is missing in the strategy.

2. Call the write_log function

   If you not only want to observe variable information status changes but also want to output personalized logs based on your own needs according to the strategy status, you can call the write_log function in the strategy for log output.

## Running Logs

### Log Content

There are two sources of logs output on the multi-contract portfolio strategy module UI interface: the strategy engine and strategy instances.

**Engine Logs**

The strategy engine generally outputs global information. In the figure below, except for content with strategy instance name followed by a colon, all are logs output by the strategy engine.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/15.png)

**Strategy Logs**

If the write_log function is called in the strategy, the log content will be output through strategy logs. The content in the red box in the figure below is the strategy log output by the strategy instance. Before the colon is the strategy instance name, and after the colon is what the write_log function outputs.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/16.png)

### Clear Operation

If you want to clear the log output on the multi-contract portfolio strategy UI interface, you can click the [Clear Logs] button in the upper right corner to clear all output logs on the interface with one click.

After clicking [Clear Logs], as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/14.png)

## Batch Operations

When the strategy has been fully tested, runs stably in live trading, and does not need frequent adjustments, if there are multiple portfolio strategy instances to run, you can use the [Initialize All], [Start All], and [Stop All] functions in the upper right corner of the interface to execute pre-market batch initialization, start strategy instances, and post-market batch stop strategy instances operations.

### Initialize All

After all strategy instances are successfully created, click the [Initialize All] button in the upper right corner to batch initialize strategy instances, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/19.png)

### Start All

After all strategy instances are successfully initialized, click the [Start All] button in the upper right corner to batch start strategy instances, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/20.png)

### Stop All

After all strategy instances are successfully started, click the [Stop All] button in the upper right corner to batch stop strategy instances, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/21.png)

## Multi-Contract Portfolio Strategy Template (StrategyTemplate) -- Basic

The multi-contract portfolio strategy template provides signal generation and order management functions. Users can develop multi-contract portfolio strategies based on this template (located in site-packages\vnpy_portfoliostrategy\template).

User-developed strategies can be placed in the [strategies](#jump) folder under the user's running folder.

Please note:

1. Strategy file naming uses underscore mode, such as portfolio_boll_channel_strategy.py, while strategy class naming uses camelCase, such as PortfolioBollChannelStrategy.

2. The class name of self-built strategies should not coincide with the class names of example strategies. If they coincide, only one strategy class name will be displayed on the GUI.

The following uses the PortfolioBollChannelStrategy strategy example to demonstrate the specific steps of strategy development:

Before writing strategy logic based on the strategy template, you need to load the internal components needed at the top of the strategy file, as shown in the code below:

```python3
from typing import List, Dict
from datetime import datetime

from vnpy.trader.utility import ArrayManager, Interval
from vnpy.trader.object import TickData, BarData
from vnpy_portfoliostrategy import StrategyTemplate, StrategyEngine
from vnpy_portfoliostrategy.utility import PortfolioBarGenerator
```

Among them, StrategyTemplate is the strategy template, StrategyEngine is the strategy engine, Interval is data frequency, TickData and BarData are data containers storing corresponding information, PortfolioBarGenerator is the portfolio strategy K-line generation module, and ArrayManager is the K-line time series management module.

### Strategy Parameters and Variables

Below the strategy class, you can set the strategy author (author), parameters (parameters), and variables (variables), as shown in the code below:

```python3

    author = "Python Trader"

    boll_window = 18
    boll_dev = 3.4
    cci_window = 10
    atr_window = 30
    sl_multiplier = 5.2
    fixed_size = 1
    price_add = 5

    parameters = [
        "boll_window",
        "boll_dev",
        "cci_window",
        "atr_window",
        "sl_multiplier",
        "fixed_size",
        "price_add"
    ]
    variables = []

```

Although strategy parameters and variables both belong to the strategy class, strategy parameters are fixed (specified by the trader externally), while strategy variables change with the strategy status during trading, so strategy variables only need to be initialized to corresponding basic types at the beginning. For example: integers set to 0, floats set to 0.0, and strings set to "".

If you need the strategy engine to display strategy parameters and variables on the UI interface during operation, and save their values during data refresh and strategy stop, you need to add the names of parameters and variables (as string data type) to the parameters and variables lists.

Please note that this list only accepts parameters or variables with str, int, float, and bool four data types. If the strategy needs to use parameters and variables of other data types, please put the definition of that parameter or variable under the __init__ function.

### Class Initialization

Input parameters: strategy_engine: StrategyEngine, strategy_name: str, vt_symbols: List[str], setting: dict

Output: None

The __init__ function is the constructor of the strategy class and needs to be consistent with the inherited StrategyTemplate.

In this inherited strategy class, initialization is generally divided into four steps, as shown in the code below:

```python3
    def __init__(
        self,
        strategy_engine: StrategyEngine,
        strategy_name: str,
        vt_symbols: List[str],
        setting: dict
    ):
        """"""
        super().__init__(strategy_engine, strategy_name, vt_symbols, setting)

        self.boll_up: Dict[str, float] = {}
        self.boll_down: Dict[str, float] = {}
        self.cci_value: Dict[str, float] = {}
        self.atr_value: Dict[str, float] = {}
        self.intra_trade_high: Dict[str, float] = {}
        self.intra_trade_low: Dict[str, float] = {}

        self.targets: Dict[str, int] = {}
        self.last_tick_time: datetime = None

        self.ams: Dict[str, ArrayManager] = {}
        for vt_symbol in self.vt_symbols:
            self.ams[vt_symbol] = ArrayManager()
            self.targets[vt_symbol] = 0

        self.pbg = PortfolioBarGenerator(self.on_bars, 2, self.on_2hour_bars, Interval.HOUR)
```

1. Inherit the strategy template through the super( ) method, and pass in the strategy engine, strategy name, vt_symbols, and parameter settings in the __init__( ) function (the above parameters are automatically passed in by the strategy engine when creating strategy instances using the strategy class, and users do not need to set them).

2. Create dictionaries for storing different contract K-line time series management instances (ArrayManager) and strategy variables required by the strategy.

3. Create ArrayManager and target position variables for different contracts traded by the strategy and put them in the dictionary.

The default length of ArrayManager is 100. If you need to adjust the length of ArrayManager, you can pass in the size parameter for adjustment (size cannot be smaller than the cycle length for calculating indicators).

4. Call the portfolio strategy K-line generation module (PortfolioBarGenerator): Synthesize Tick data into 1-minute K-line data through time slicing. If needed, you can also synthesize longer time period data, such as 15-minute K-lines.

If you only trade based on on_bar, the code here can be written as:

```python3
        self.pbg = PortfolioBarGenerator(self.on_bars)
```

And you don't need to pass in the longer K-line period to be synthesized based on the on_bars period, and the function name to receive longer K-line periods to the pbg instance.

Please note:

 - When synthesizing X-minute lines, X must be set to a number divisible by 60 (except 60). There is no such limit for synthesizing hour lines.

 - The default data frequency for PortfolioBarGenerator to synthesize long-period K-lines based on the on_bar function is minute level. If you need to trade based on synthesized hour lines or longer period K-lines, please import Interval at the top of the strategy file and pass in the corresponding data frequency to the bg instance.

 - **The self.on_hour_bars function name has been used internally in the program**. If you need to synthesize 1-hour K-lines, please use self.on_1_hour_bars or other naming.

### Functions Called by Strategy Engine

The update_setting function in StrategyTemplate and the four functions starting with get after this function, as well as the update_trade and update_order functions, are all functions that the strategy engine is responsible for calling. Generally, they do not need to be called during strategy writing.

### Strategy Callback Functions

Functions starting with on in StrategyTemplate are called callback functions and can be used to receive data or receive status updates during strategy writing. The role of callback functions is that when a certain event occurs, this type of function in the strategy will be automatically called by the strategy engine (no need to actively operate in the strategy). Callback functions can be classified into the following two categories according to their functions:

#### Strategy Instance Status Control (All strategies need)

**on_init**

* Input: None

* Output: None

The on_init function is called when initializing the strategy. The default writing method is to first call the write_log function to output "Strategy initialized" log, and then call the load_bars function to load historical data. As shown in the code below:

```python3
    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("Strategy initialized")
        self.load_bars(10)
```

Unlike CTA strategies, multi-contract portfolio strategies only support K-line backtesting, so the multi-contract strategy template does not have a load_ticks function.

During strategy initialization, the strategy's inited and trading status are both [False]. At this time, only ArrayManager is called to calculate and cache related calculation indicators, and trading signals cannot be sent. Only after calling the on_init function does the strategy's inited status become [True], and strategy initialization is completed.

**on_start**

* Input: None

* Output: None

The on_start function is called when starting the strategy. The default writing method is to call the write_log function to output "Strategy started" log, as shown in the code below:

```python3
    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("Strategy started")
```

After calling the strategy's on_start function to start the strategy, the strategy's trading status becomes [True], and only at this time can the strategy send trading signals.

**on_stop**

* Input: None

* Output: None

The on_stop function is called when stopping the strategy. The default writing method is to call the write_log function to output "Strategy stopped" log, as shown in the code below:

```python3
    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("Strategy stopped")
```

After calling the strategy's on_stop function to stop the strategy, the strategy's trading status becomes [False], and at this time the strategy will not send trading signals.

#### Receive Data, Calculate Indicators, Send Trading Signals

**on_tick**

* Input: tick: TickData

* Output: None

Most trading systems only provide Tick data push. Even if some platforms can provide K-line data push, the speed at which these data arrive at the local computer will also be slower than Tick data push, because they also need to be synthesized by the platform before being pushed. Therefore, during live trading, all strategy K-lines in VeighNa are synthesized from received Tick data.

When the strategy receives the latest Tick data market push in live trading, the on_tick function is called. The default writing method is to push the received Tick data into the previously created pbg instance through the PortfolioBarGenerator's update_tick function to synthesize 1-minute K-lines, as shown in the code below:

```python3
    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.pbg.update_tick(tick)
```

Please note that the on_tick function is only called in live trading and is not supported in backtesting.

**on_bars**

* Input: bars: Dict[str, BarData]

* Output: None

When the strategy receives the latest K-line data (during live trading, the default pushed in is 1-minute K-lines synthesized based on Tick data, and during backtesting, it depends on the K-line data frequency filled in when selecting parameters), the on_bars function is called.

Unlike the CTA strategy module, the multi-contract portfolio strategy module receives K-line pushes through the on_bars callback function, receiving all contracts' K-line data at that time point at once, rather than receiving them one by one through the on_bar function (unable to judge whether the K-line of the current time point has all completed).

There are two writing methods that have appeared in example strategies:

1. If the strategy trades based on K-lines pushed by on_bars, then please write all trading request functions under the on_bars function (because the example strategy class PortfolioBollChannelStrategy in this demonstration does not trade based on on_bars, no example explanation is given. For example code trading based on on_bars, please refer to other example strategies);

2. If the strategy needs to synthesize longer time period K-lines through PortfolioBarGenerator based on K-line data pushed by on_bars to trade, then please call the PortfolioBarGenerator's update_bars function in on_bars to push the received bars into the previously created pbg instance, as shown in the code below:

```python3
    def on_bars(self, bars: Dict[str, BarData]):
        """
        Callback of new bars data update.
        """
        self.pbg.update_bars(bars)
```

The example strategy class PortfolioBollChannelStrategy generates signals through 2-hour K-line data returns. There are three parts in total, as shown in the code below:

```python3
    def on_2hour_bars(self, bars: Dict[str, BarData]):
        """"""
        self.cancel_all()

        for vt_symbol, bar in bars.items():
            am: ArrayManager = self.ams[vt_symbol]
            am.update_bar(bar)

        for vt_symbol, bar in bars.items():
            am: ArrayManager = self.ams[vt_symbol]
            if not am.inited:
                return

            self.boll_up[vt_symbol], self.boll_down[vt_symbol] = am.boll(self.boll_window, self.boll_dev)
            self.cci_value[vt_symbol] = am.cci(self.cci_window)
            self.atr_value[vt_symbol] = am.atr(self.atr_window)

            current_pos = self.get_pos(vt_symbol)
            if current_pos == 0:
                self.intra_trade_high[vt_symbol] = bar.high_price
                self.intra_trade_low[vt_symbol] = bar.low_price

                if self.cci_value[vt_symbol] > 0:
                    self.targets[vt_symbol] = self.fixed_size
                elif self.cci_value[vt_symbol] < 0:
                    self.targets[vt_symbol] = -self.fixed_size

            elif current_pos > 0:
                self.intra_trade_high[vt_symbol] = max(self.intra_trade_high[vt_symbol], bar.high_price)
                self.intra_trade_low[vt_symbol] = bar.low_price

                long_stop = self.intra_trade_high[vt_symbol] - self.atr_value[vt_symbol] * self.sl_multiplier

                if bar.close_price <= long_stop:
                    self.targets[vt_symbol] = 0

            elif current_pos < 0:
                self.intra_trade_low[vt_symbol] = min(self.intra_trade_low[vt_symbol], bar.low_price)
                self.intra_trade_high[vt_symbol] = bar.high_price

                short_stop = self.intra_trade_low[vt_symbol] + self.atr_value[vt_symbol] * self.sl_multiplier

                if bar.close_price >= short_stop:
                    self.targets[vt_symbol] = 0

        for vt_symbol in self.vt_symbols:
            target_pos = self.targets[vt_symbol]
            current_pos = self.get_pos(vt_symbol)

            pos_diff = target_pos - current_pos
            volume = abs(pos_diff)
            bar = bars[vt_symbol]
            boll_up = self.boll_up[vt_symbol]
            boll_down = self.boll_down[vt_symbol]

            if pos_diff > 0:
                price = bar.close_price + self.price_add

                if current_pos < 0:
                    self.cover(vt_symbol, price, volume)
                else:
                    self.buy(vt_symbol, boll_up, volume)
            elif pos_diff < 0:
                price = bar.close_price - self.price_add

                if current_pos > 0:
                    self.sell(vt_symbol, price, volume)
                else:
                    self.short(vt_symbol, boll_down, volume)

        self.put_event()
```

- Clear unfilled orders: To prevent previously placed orders from not being filled in the previous 2 hours but the price may have been adjusted in the next 2 hours, use the cancel_all() method to immediately cancel all previously unfilled orders, ensuring that the strategy's state at the beginning of the current 2 hours is clear and unique;

- Call the K-line time series management module: Calculate corresponding technical indicators based on the latest 2-hour K-line data, such as Bollinger Band upper and lower tracks, CCI indicator, ATR indicator, etc. First obtain the ArrayManager object, then push the received K-line into it, check the initialization status of ArrayManager. If it is not initialized successfully, return directly. There is no need to perform subsequent trading-related logic judgments. Because many technical indicator calculations have requirements for the minimum number of K-lines. If the number is not enough, the calculated indicators will be erroneous or meaningless. Conversely, if there is no return, you can start calculating technical indicators;

- Signal calculation: Through position judgment and combined with CCI indicator and ATR indicator, place **limit orders** (buy/sell) at channel breakout points, and set exit points (short/cover).

    Please note:
    1. In the CTA strategy module, position judgment is usually done by accessing the strategy's variable pos. However, in the multi-contract portfolio strategy module, the get_pos function is called to obtain the current position of a certain contract for logic judgment, then the target position of that contract is set, and finally logic judgment is performed through the difference between target position and actual position to send trading signals;

    2. If you need to refresh indicator values on the GUI, please do not forget to call the put_event() function.

#### Order Status Update

Because the portfolio strategy needs to place orders for multiple contracts simultaneously, and the sequence of order execution for each contract within a certain K-line segment cannot be judged during backtesting, on_order and on_trade functions cannot be provided to obtain order/trade pushes. Instead, related status queries can only be performed through get_pos and get_order during each on_bars callback.

### Active Functions

**buy**: Buy to open (Direction: LONG, Offset: OPEN)

**sell**: Sell to close (Direction: SHORT, Offset: CLOSE)

**short**: Sell to open (Direction: SHORT, Offset: OPEN)

**cover**: Buy to close (Direction: LONG, Offset: CLOSE)

* Input: vt_symbol: str, price: float, volume: float, lock: bool = False, net: bool = False

* Output: vt_orderids: List[str] / None

buy/sell/short/cover are all trading request functions inside the strategy responsible for sending orders. The strategy can send trading signals to the strategy engine through these functions to achieve the purpose of placing orders.

Taking the buy function code below as an example, you can see that **the code of the specific contract to trade**, price, and quantity are required parameters, while lock position conversion and net position conversion default to False. You can also see that after receiving the passed-in parameters, the function internally calls the send_order function in StrategyTemplate to send orders (because it is a buy instruction, it automatically fills in LONG for direction and OPEN for offset).

Unlike the CTA strategy module, the portfolio strategy module does not provide local stop order functionality, so the stop parameter has been removed from the order functions.

If lock is set to True, the order will perform lock position order conversion (in the case of existing positions, if you want to close positions, it will first close all yesterday positions, and then the remaining part will perform reverse opening to replace closing today positions, to avoid today's closing fee penalty).

If net is set to True, the order will perform net position order conversion (based on all positions of the overall account, convert the opening and closing direction of the strategy order according to the net position holding method). However, the net position trading mode and lock position trading mode are mutually exclusive, so when net is set to True, lock must be set to False.

Please note that if sending a closing order to the Shanghai Futures Exchange, because the exchange must specify closing today or closing yesterday, the underlying layer will automatically convert its closing instructions. Because some varieties of the Shanghai Futures Exchange have today's closing fee discounts, by default, orders are sent with today's closing priority (if the trading target has yesterday's closing fee discount on the Shanghai Futures Exchange, you can make appropriate modifications in the convert_order_request_shfe function of vnpy.trader.converter).

```python3
    def buy(self, vt_symbol: str, price: float, volume: float, lock: bool = False, net: bool = False) -> List[str]:
        """
        Send buy order to open a long position.
        """
        return self.send_order(vt_symbol, Direction.LONG, Offset.OPEN, price, volume, lock, net)
```

Please note that domestic futures have the concept of opening and closing positions, for example, buy operations need to be distinguished into buy to open and buy to close; but for stocks and foreign futures, they are all net position mode, without the concept of opening and closing positions, so you only need to use the buy and sell instructions.

**send_order**

* Input: vt_symbol: str, direction: Direction, offset: Offset, price: float, volume: float, lock: bool = False, net: bool = False

* Output: vt_orderids: List[str] / None

The send_order function is a function for sending orders called by the strategy engine. Generally, you do not need to call it separately when writing strategies. You can send limit orders through buy/sell/short/cover functions.

During live trading, after receiving the passed-in parameters, the round_to function is called to process the order price and quantity based on the contract's pricetick and min_volume.

Please note that trading orders can only be sent after the strategy is started, that is, after the strategy's trading status becomes [True]. If this function is called when the strategy's Trading status is [False], it will only return [].

**cancel_order**

* Input: vt_orderid: str

* Output: None

**cancel_all**

* Input: None

* Output: None

cancel_order and cancel_all are both trading request functions responsible for cancelling orders. cancel_order cancels specified active orders in the strategy, and cancel_all cancels all active orders in the strategy.

Please note that orders can only be cancelled after the strategy is started, that is, after the strategy's trading status becomes [True].

### Function Functions

The following are function functions other than strategies:

**get_pos**

* Input: vt_symbol: str

* Output: int / 0

Calling the get_pos function in the strategy can obtain position data for a specific contract.

**get_order**

* Input: vt_orderid

* Output: OrderData / None

Calling the get_order function in the strategy can obtain order data for a specific contract.

**get_all_active_orderids**

* Input: None

* Output: List[OrderData] / None

Calling the get_all_active_orderids function in the strategy can obtain all current active order numbers.

**get_pricetick**

* Input: vt_symbol

* Output: pricetick: float / None

Calling the get_price function in the strategy can obtain the minimum price movement for a specific contract.

**write_log**

* Input: msg: str

* Output: None

Calling the write_log function in the strategy can output logs with specified content.

**load_bars**

* Input: days: int, interval: Interval = Interval.MINUTE

* Output: None

Calling the load_bars function in the strategy can load K-line data during strategy initialization.

As shown in the code below, when the load_bars function is called, the default loaded days is 10, the frequency is one minute, which corresponds to loading 10 days of 1-minute K-line data. During backtesting, 10 days refers to 10 trading days, while during live trading, 10 days refers to natural days, so it is recommended that the loaded days be more rather than less. When loading, it will first try to obtain historical data through the trading interface, data service, and database in sequence until historical data is obtained or empty is returned.

```python3
    def load_bars(self, days: int, interval: Interval = Interval.MINUTE) -> None:
        """
        Load historical bar data for initializing strategy.
        """
        self.strategy_engine.load_bars(self, days, interval)
```

**put_event**

* Input: None

* Output: None

Calling the put_event function in the strategy can notify the GUI to refresh the strategy status related display.

Please note that the interface can only be refreshed after strategy initialization is completed and the inited status becomes [True].

**send_email**

* Input: msg: str

* Output: None

After configuring email related information (for configuration methods, see the Global Configuration section in the Basic Usage chapter), calling the send_email function in the strategy can send emails with specified content to your email address.

Please note that emails can only be sent after strategy initialization is completed and the inited status becomes [True].

**sync_data**

* Input: None

* Output: None

Calling the sync_data function in the strategy can synchronize strategy variables to json files for local caching every time the strategy stops or trades during live trading, convenient for reading and restoring the next day during initialization (the strategy engine will call it, and there is no need to actively call it in the strategy).

Please note that strategy information can only be synchronized after the strategy is started, that is, after the strategy's trading status becomes [True].

## Multi-Contract Portfolio Strategy Template (StrategyTemplate) -- Advanced

The PortfolioStrategy module is aimed at multi-underlying portfolio quantitative strategies. Such strategies pursue adjusting the strategy portfolio position to the target state at the execution level, without paying too much attention to the underlying order trading details.

First, introduce the function functions for position target rebalancing trading to demonstrate the function support for position target rebalancing trading:

### Function Functions for Position Target Rebalancing Trading

The following are function functions called by strategies in position target rebalancing trading mode:

**set_target**

* Input: vt_symbol: str, target: int

* Output: None

Calling the set_target function in the strategy can set the target position for a specific contract.

Please note: Target position is a continuous state, so after setting it will continue to be maintained until it is set again.

**get_target**

* Input: vt_symbol: str

* Output: int

Calling the get_target function in the strategy can obtain the set target position for a specific contract.

Please note: The strategy's target position state will be automatically persisted to hard disk files during sync_data (trades, stops, etc.) and restored after strategy restart.

**rebalance_portfolio**

* Input: bars: Dict[str, BarData]

* Output: None

Calling the rebalance_portfolio function in the strategy can execute rebalancing trading based on the set target positions for specific contracts.

Please note: Only contracts with K-line slices in the current bars dictionary will participate in the execution of this rebalancing trading, thereby ensuring that contracts in non-trading periods (no market push) will not incorrectly send orders.

**calculate_price**

* Input: vt_symbol: str, direction: Direction, reference: float

* Output: pricetick: float

Overriding the calculate_price function in the strategy can set the target price for specific contracts on demand (such as fixed price improvement, fixed pricetick improvement, percentage improvement, etc.).

If not passed, it defaults to returning the reference price (if not overridden in the strategy, the K-line closing price will be used as the order price in the rebalance_portfolio function).

### Usage Example of Position Target Rebalancing Trading Function Functions

The biggest difference between position target rebalancing trading function and the basic usage of StrategyTemplate lies in the processing differences in the strategy on_bars function. The following uses the TrendFollowingStrategy strategy example to demonstrate the specific steps of position target rebalancing trading:

**on_bars**

* Input: bars: Dict[str, BarData]

* Output: None

When the strategy receives the latest K-line data (during live trading, the default pushed in is 1-minute K-lines synthesized based on Tick data, and during backtesting, it depends on the K-line data frequency filled in when selecting parameters), the on_bars function is called.

The example strategy class TrendFollowingStrategy generates signals through 1-minute K-line data returns. There are three parts in total, as shown in the code below:

```python3
    def on_bars(self, bars: Dict[str, BarData]) -> None:
        """K-line slice callback"""
        # Update K-line to calculate RSI values
        for vt_symbol, bar in bars.items():
            am: ArrayManager = self.ams[vt_symbol]
            am.update_bar(bar)

        for vt_symbol, bar in bars.items():
            am: ArrayManager = self.ams[vt_symbol]
            if not am.inited:
                return

            atr_array = am.atr(self.atr_window, array=True)
            self.atr_data[vt_symbol] = atr_array[-1]
            self.atr_ma[vt_symbol] = atr_array[-self.atr_ma_window:].mean()
            self.rsi_data[vt_symbol] = am.rsi(self.rsi_window)

            current_pos = self.get_pos(vt_symbol)
            if current_pos == 0:
                self.intra_trade_high[vt_symbol] = bar.high_price
                self.intra_trade_low[vt_symbol] = bar.low_price

                if self.atr_data[vt_symbol] > self.atr_ma[vt_symbol]:
                    if self.rsi_data[vt_symbol] > self.rsi_buy:
                        self.set_target(vt_symbol, self.fixed_size)
                    elif self.rsi_data[vt_symbol] < self.rsi_sell:
                        self.set_target(vt_symbol, -self.fixed_size)
                    else:
                        self.set_target(vt_symbol, 0)

            elif current_pos > 0:
                self.intra_trade_high[vt_symbol] = max(self.intra_trade_high[vt_symbol], bar.high_price)
                self.intra_trade_low[vt_symbol] = bar.low_price

                long_stop = self.intra_trade_high[vt_symbol] * (1 - self.trailing_percent / 100)

                if bar.close_price <= long_stop:
                    self.set_target(vt_symbol, 0)

            elif current_pos < 0:
                self.intra_trade_low[vt_symbol] = min(self.intra_trade_low[vt_symbol], bar.low_price)
                self.intra_trade_high[vt_symbol] = bar.high_price

                short_stop = self.intra_trade_low[vt_symbol] * (1 + self.trailing_percent / 100)

                if bar.close_price >= short_stop:
                    self.set_target(vt_symbol, 0)

        self.rebalance_portfolio(bars)

        self.put_event()
```

- Call the K-line time series management module: Calculate corresponding technical indicators based on the latest minute K-line data, such as ATR indicator, RSI indicator, etc. First obtain the ArrayManager object, then push the received K-line into it, check the initialization status of ArrayManager. If it is not initialized successfully, return directly. There is no need to perform subsequent trading-related logic judgments. Because many technical indicator calculations have requirements for the minimum number of K-lines. If the number is not enough, the calculated indicators will be erroneous or meaningless. Conversely, if there is no return, you can start calculating technical indicators;

- Signal calculation: Through position judgment (get_pos) and combined with indicator calculation results, **set target positions** (set_target) at channel breakout points

- Execute rebalancing trading (rebalance_portfolio)

**calculate_price**

* Input: vt_symbol: str, direction: Direction, reference: float

* Output: price: float

When the rebalance_portfolio function detects a difference between target position and actual position, it will call the calculate_price function to calculate the rebalancing order price.

The default writing method in the strategy is to calculate the order price based on the set price_add for the order direction. You can also refer to the example strategy PairTradingStrategy for calculating the order price based on the set tick_add.

```python3
    def calculate_price(self, vt_symbol: str, direction: Direction, reference: float) -> float:
        """Calculate rebalancing order price (supports overriding on demand)"""
        if direction == Direction.LONG:
            price: float = reference + self.price_add
        else:
            price: float = reference - self.price_add

        return price
```

### Differences from Basic Usage of StrategyTemplate

**on_bars**

1. No need to clear unfilled orders: rebalance_portfolio already has logic to call the cancel_all function, so there is no need to call the cancel_all function to cancel unfilled orders when receiving on_bars function pushes.

2. No need to use the self.targets dictionary to cache contract target positions: Directly call the set_target function passing in the contract and target position (positive numbers represent long, negative numbers represent short) for setting.

3. No need to manually write order logic in the strategy based on cached target positions: The rebalance_portfolio function has automatically taken over rebalancing trading and will place orders based on target positions.

**calculate_price**

Position target rebalancing trading needs to call the calculate_price function to calculate the rebalancing order price.
