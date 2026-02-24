# SpreadTrading - Multi-Contract Spread Arbitrage Module

## Function Overview

SpreadTrading is a functional module for **multi-contract spread arbitrage**. Users can conveniently create flexible spread contracts, complete manual trading and automatic trading tasks through its UI interface.


## Loading and Launching

### Loading via VeighNa Station

After launching and logging into VeighNa Station, click the [Trading] button. In the configuration dialog, check [SpreadTrading] in the [Application Module] section.

### Loading via Script

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_spreadtrading import SpreadTradingApp

# Write after creating the main_engine object
main_engine.add_app(SpreadTradingApp)
```


## Starting the Module

<span id="jump">

For user-developed strategies, they need to be placed in the **strategies** directory under the VeighNa Trader runtime directory to be recognized and loaded. The specific runtime directory path can be viewed in the title bar at the top of the VeighNa Trader main interface.

For users with default installation on Windows, the strategies directory path for placing strategies is usually:

```bash
    C:\Users\Administrator\strategies
```

Where Administrator is the system username currently logged into Windows.

</span>

Before starting the module, please connect to the trading interface first (for connection methods, see the Interface Connection section in the Basic Usage chapter). After seeing "Contract information query successful" output in the [Log] section of the VeighNa Trader main interface, start the module (**if the module is opened before contract information query is successful, it may cause the spread's price tick value to be zero, thereby triggering underlying errors after order execution**), as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/1.png)

Please note that because the IB interface cannot automatically obtain all contract information upon login, it can only be obtained when the user manually subscribes to market data. Therefore, you need to manually subscribe to contract market data on the main interface before starting the module.

After successfully connecting to the trading interface, click [Function] -> [Spread Trading] in the menu bar, or click the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/1.png)

You can then enter the UI interface of the spread trading module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/2.png)


## Creating Spread Contracts

### Querying Contracts

Before creating spread contracts, users can use the [Query Contract] function to find contracts that can form spreads (**exchange arbitrage contracts are not supported**):

- Click [Help] -> [Query Contract] in the VeighNa Trader menu bar, and the contract query interface will pop up, as shown in the figure below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/3.png)
- Find contracts that can be used for spread trading in the interface;
- This document demonstrates with soybean futures calendar spread arbitrage, i.e., trading y2205.DCE (soybean futures May 2022 expiry contract) and y2209.DCE (soybean futures September 2022 expiry contract).

### Building Spread Contracts

On the left side of the spread trading interface, click the [Create Spread] button to pop up the create spread interface, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/4.png)

The spread trading module supports flexible spread calculation formulas (such as A/B, A-B*C, etc.), and also allows introducing pricing legs that do not participate in trading to meet the needs of complex domestic and foreign arbitrage spreads that need to consider exchange rates and tax rates and other factors. When creating spread contracts, you need to configure relevant parameters. The parameter requirements are as follows:

- Spread Name
  - User-defined spread contract name;
  - Spread names cannot be duplicated;
- Active Leg Code
  - The local code of the leg that is sent first when the spread order book price meets conditions.
  - Format is vt_symbol (contract code + exchange name);
  - Must be one of the leg options below;
- Minimum Trading Volume
  - Minimum trading lots;
- Price Formula
  - Spread contract calculation formula;
  - Supports any Python built-in mathematical functions;
  - Note that variables can only be A, B, C, D, E (not all need to be used);
- [A, B, C, D, E]
  - Includes active and passive legs that build the spread contract, and can also introduce pricing legs that do not participate in trading, consisting of contract code, trading direction, and trading multiplier:
    - Contract code is the contract local code (vt_symbol) corresponding to the variable in the formula;
    - Generally speaking, spread trading principle is to use the passive leg to hedge immediately after the active leg completes trading, so the active leg generally chooses less active contracts, with both price multiplier and trading multiplier being positive; the passive leg generally chooses more active contracts, with both price multiplier and trading multiplier being negative;
    - Leave unused variables blank;

After setting the spread contract parameters, click the [Create Spread] button below to successfully create the spread contract.

In the soybean futures calendar spread arbitrage example, its price multiplier and trading multiplier are both 1:1, i.e., spread = y2205 - y2209; buying 1 lot of spread equals buying 1 lot of y2205 and simultaneously selling 1 lot of y2209 to complete hedging.

Please note that when there are multiple legs and futures contract sizes are unequal, building spread contracts will be relatively difficult. For example, when building spread contracts used in virtual steel mill arbitrage, the calculation formula is as follows:

- Rebar production technology is 16 tons of iron ore plus 5 tons of coke to make 10 tons of rebar.
- Spread based on price multiplier: spread = 1* RB - 1.6* I - 0.5* J.
- However, rebar is 10 tons/lot, iron ore and coke are both 100 tons/lot, so their trading multipliers are 1:10:10;
- Therefore, based on the greatest common divisor rule, the actual trading lot relationship is for every 100 lots of rebar bought (1000 tons), 16 lots of iron ore (1600 tons) and 5 lots of coke (500 tons) need to be sold to complete hedging.

### Monitoring Spread Contracts

After the spread contract is created, the [Log] section in the monitoring interface will output "Spread created successfully"; the [Spread] section will also display the spread contract's real-time market data, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/6.png)

In the soybean futures spread trading example, the meaning of each field in the [Spread] component is as follows:

- Bid Price
  - y2205 bid 1 price - y2209 ask 1 price
- Bid Quantity
  - min(y2205 bid 1 quantity, y2209 ask 1 quantity)
  - Take the minimum value to ensure all contracts can be executed
- Ask Price
  - y2205 ask 1 price - y2209 bid 1 price
- Ask Quantity
  - min(y2205 ask 1 quantity, y2209 bid 1 quantity)

### Removing Spread Contracts

On the left side of the spread trading interface, click the [Remove Spread] button to pop up the remove spread interface, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/35.png)

After selecting the spread contract to remove, click the [Remove] button to successfully remove the spread contract. The [Log] component outputs "Spread removed successfully", as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/36.png)


## Manual Trading

Assuming the current soybean futures spread contract bid price is 408, ask price is 420, and on a large cycle, the spread fluctuates around 0.

The profit of spread trading lies in selling high and buying low, i.e., buying the soybean futures spread contract at a low position, such as -300, and selling the spread contract at a high position, such as +800, to close positions and profit. Since it cannot be executed immediately, its default execution algorithm SpreadTaker (active price matching algorithm) will perform order operations at regular intervals, generally in the form of limit orders with price improvement.

The following introduces the manual trading operation situation through 2 examples: sending orders for immediate execution and sending orders waiting for execution:

### Sending Orders for Immediate Execution

Assuming the target spread contract price is 420, we send a buy limit order at 430 in the form of 5 ticks price improvement, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/2-7.png)

Since the limit order (430) price is higher than the current ask price (410), the order is executed immediately, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/8.png)

At this time, the status of each monitoring component is as follows:

- Log Component
  - The order of buying y_05_09 spread contract is: send y2205 long order -> y2205 order executed -> send y2209 short order -> y2209 order executed. Spread trading must follow the logic that after the active leg is executed, the passive leg is used to hedge positions, and hedging must be as timely as possible. This is also why the passive leg generally chooses more active contracts.
- Spread Component
  - After buying 1 lot of soybean futures spread contract, [Net Position] changes from 0 to 1. In fact, the VeighNa Trader [Position] component shows y2205 contract long position 1 lot, y2209 contract short position 1 lot.
- Algorithm Component
  - This order's SpreadTaker algorithm execution situation: trade quantity 1 lot, order status is [All Filled].

### Sending Orders Waiting for Execution

Send a limit buy order at 400 price. Since the current bid and ask prices are located at 412 and 426 respectively, the order status displays [Not Filled], as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/9.png)

At this time, the status of each monitoring component is as follows:

- Log Component
  - This algorithm, SpreadTaker_000002, has been started, but because the price has not triggered the target price, the algorithm is in a waiting state during countdown reading;
- Algorithm Component
  - Order status is [Not Filled]. To end the algorithm, just double-click the [SpreadTaker_000002] cell with the mouse.

Only when the ask price is lower than -300 will this limit order be triggered, with 5 ticks price improvement, i.e., -290 to actively execute.

### Cancelling Orders

Double-click the [SpreadTaker_000002] cell with the mouse to end the algorithm. At this time, the [Log] component outputs "Algorithm stopped", and the [Algorithm] component displays the order status changing from [Not Filled] to [Cancelled], as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/10.png)


## Automatic Trading

### Adding Strategies

Users can create different strategy instances (objects) based on written spread strategy templates (classes).

Select the strategy name to trade from the dropdown box on the left (such as BasicSpreadStrategy), as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/19.png)

Please note that the displayed strategy name is the name of the **strategy class** (camelCase naming), not the strategy file (underscore naming).

After selecting the strategy class, click [Add Strategy] to pop up the add strategy dialog, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/11.png)

When creating a strategy instance, you need to configure relevant parameters. The parameter requirements are as follows:

- Instance Name
  - User-defined strategy instance name, here is test;
  - Strategy instance names cannot be duplicated;
- Spread Name
  - Spread contract used for trading, here is y_05_09;
  - Must be a spread contract that can be queried in the spread component;
- Parameter Settings
  - The displayed parameter names are the parameter names written in the parameters list in the strategy;
  - Default values are the default values of parameters in the strategy;
  - As observed in the figure above, the data type of the parameter is displayed in the <> brackets after the parameter name. When filling in parameters, you should follow the corresponding data type. Among them, <class 'str'> is string, <class 'int'> is integer, <class 'float'> is float;
  - Please note that if a parameter may be adjusted to a value with decimal places, and the default parameter value is an integer (such as 1). When writing the strategy, set the default parameter value to a float (such as 1.0). Otherwise, the strategy will default that parameter to an integer, and when subsequently [Editing] the strategy instance parameters, only integers will be allowed.

  - Taking BasicSpreadStrategy as an example, the strategy's parameter settings are as follows:
    - buy_price
      - Buy open threshold, in the figure is -300, i.e., when the price falls below -300, execute orders;
    - sell_price
      - Sell close threshold, in the figure is 400, i.e., when the price rises to 400, execute orders;
    - short_price
      - Sell open threshold, in the figure is 800, i.e., when the price rises to 800, execute orders;
    - cover_price
      - Buy close threshold, in the figure is 600, i.e., when the price falls to 600, execute orders;
    - max_pos
      - Active leg order quantity;
    - payup
      - Number of ticks for price improvement;
    - interval
      - Time interval, i.e., orders will be sent at regular intervals.

After parameter configuration is completed, click the [Add] button to start creating the strategy instance. After successful creation, you can see the strategy instance in the strategy monitoring component in the lower right corner, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/12.png)

The top of the strategy monitoring component displays the strategy instance name, spread name, strategy class name, and strategy author name (author defined in the strategy). The top buttons are used to control and manage the strategy instance. The first row of the table displays the parameter information inside the strategy (parameter names need to be written in the strategy's parameters list to be displayed in the GUI). The second row of the table displays the variable information during strategy operation (variable names need to be written in the strategy's variables list to be displayed in the GUI). The [inited] field indicates the current initialization status of the strategy (whether historical data playback has been completed), and the [trading] field indicates whether the strategy can currently start trading.

As observed in the figure above, at this time the strategy instance's [inited] and [trading] status are both [False]. This indicates that the strategy instance has not been initialized yet and cannot send trading signals.

After the strategy instance is successfully created, the strategy instance configuration information will be saved to the spread_trading_strategy.json file under the .vntrader folder.

### Managing Strategies

#### Initialization

After the strategy instance is successfully created, you can initialize the instance. Click the [Initialize] button under the strategy instance. If initialization is successful, it is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/23.png)

You can observe that at this time the strategy instance's [inited] status is already [True]. This indicates that the strategy instance has called the load_bar function to load historical data and completed initialization. The [trading] status is still [False], indicating that the strategy instance cannot start automatic trading yet.

#### Start

Only when the strategy instance is initialized successfully and the [inited] status is [True] can the strategy's automatic trading function be started. Click the [Start] button under the strategy instance to start the strategy instance. After successful start, the [Log] component will output corresponding information (please note that strategy start does not mean algorithm start; algorithm start status depends on strategy logic), as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/13.png)

At this time, the [Algorithm] component shows that the test strategy calls the SpreadTaker algorithm to place buy and sell orders at -300 and 800 positions respectively; since the actual price has not reached these 2 thresholds, the orders are always hanging, and the order status is [Not Filled].

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/14.png)

The [trading] field in the [Strategy] component changes from [False] to [True], as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/24.png)

#### Stop

If you want to stop the strategy, click the [Stop] button under the strategy instance to stop the strategy instance's automatic trading. The [Log] component outputs "Algorithm stopped", as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/15.png)

The algorithm status in the [Algorithm] component becomes [Cancelled], as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/16.png)

The [trading] field in the [Strategy] component changes from [True] to [False], as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/29.png)

#### Edit

If after creating a strategy instance, you want to edit the parameters of a certain strategy instance (if the strategy has been started, you need to click the [Stop] button under the strategy instance first to stop the strategy), you can click the [Edit] button under the strategy instance, and a parameter editing dialog will pop up for modifying strategy parameters, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/18.png)

After editing the strategy parameters, click the [OK] button below, and the corresponding modifications will be immediately updated in the parameter table, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/30.png)

However, the strategy instance's trading contract code cannot be modified, and no re-initialization operation will be executed after modification. Also note that at this time only the parameter values of the strategy instance in the spread_trading_strategy.json file under the .vntrader folder are modified, not the parameters in the original strategy file.

Before modification, the json file is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/26-1.png)

After modification, the json file is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/27-1.png)

If you want to start the strategy again after editing during trading, click the [Start] button under the strategy instance to start the strategy instance again, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/28.png)

#### Remove

If after creating a strategy instance, you want to remove a certain strategy instance (if the strategy has been started, you need to click the [Stop] button under the strategy instance first to stop the strategy), you can click the [Remove] button under the strategy instance. After successful removal, the strategy monitoring component in the lower right corner of the GUI will no longer display the strategy instance information. As shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/34.png)

At this time, the spread_trading_strategy.json file under the .vntrader folder has also removed the configuration information of the strategy instance.

### Batch Operations

When the strategy has been fully tested, runs stably in live trading, and does not need frequent adjustments, if there are multiple spread strategy instances to run, you can use the [Initialize All], [Start All], and [Stop All] functions in the lower left corner of the interface to execute pre-market batch initialization, start strategy instances, and post-market batch stop strategy instances operations.

#### Initialize All

After all strategy instances are successfully created, click the [Initialize All] button in the lower left corner to batch initialize strategy instances, as shown in the figure below:

After clicking [Initialize All], as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/31.png)

#### Start All

After all strategy instances are successfully initialized, click the [Start All] button in the lower left corner to batch start strategy instances, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/32.png)

#### Stop All

After all strategy instances are successfully started, click the [Stop All] button in the lower left corner to batch stop strategy instances, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/spread_trading/33.png)


## Spread Trading Strategy Template (SpreadStrategyTemplate)

The spread trading strategy template provides signal generation and order management functions. Users can develop strategies based on this template (located in vnpy_spreadtrading.template).

User-developed strategies can be placed in the [strategies](#jump) folder under the user's running folder.

Please note:

1. Strategy file naming uses underscore mode, such as statistical_arbitrage_strategy.py, while strategy class naming uses camelCase, such as StatisticalArbitrageStrategy.

2. The class name of self-built strategies should not coincide with the class names of example strategies. If they coincide, only one strategy class name will be displayed on the GUI.

Currently, VeighNa officially provides two spread strategies: BasicSpreadStrategy and StatisticalArbitrageStrategy. The following uses the StatisticalArbitrageStrategy example to demonstrate the specific steps of strategy development:

Before writing strategy logic based on the spread trading strategy template, you need to load the internal components needed at the top of the strategy file, as shown in the code below:

```python3
from vnpy.trader.utility import BarGenerator, ArrayManager
from vnpy_spreadtrading import (
    SpreadStrategyTemplate,
    SpreadAlgoTemplate,
    SpreadData,
    OrderData,
    TradeData,
    TickData,
    BarData
)
```

Among them, SpreadStrategyTemplate and SpreadAlgoTemplate are spread trading strategy template and spread algorithm template, SpreadData, OrderData, TickData, TradeData, and BarData are data containers storing corresponding information, BarGenerator is the K-line generation module, and ArrayManager is the K-line time series management module.

### Strategy Parameters and Variables

Below the strategy class, you can set the strategy author (author), parameters (parameters), and variables (variables), as shown in the code below:

```python3
    author = "Python Trader"

    boll_window = 20
    boll_dev = 2
    max_pos = 10
    payup = 10
    interval = 5

    spread_pos = 0.0
    boll_up = 0.0
    boll_down = 0.0
    boll_mid = 0.0

    parameters = [
        "boll_window",
        "boll_dev",
        "max_pos",
        "payup",
        "interval"
    ]
    variables = [
        "spread_pos",
        "boll_up",
        "boll_down",
        "boll_mid"
    ]
```

Although strategy parameters and variables both belong to the strategy class, strategy parameters are fixed (specified by the trader externally), while strategy variables change with the strategy status during trading, so strategy variables only need to be initialized to corresponding basic types at the beginning. For example: integers set to 0, floats set to 0.0, and strings set to "".

If you need the spread trading module engine to display strategy parameters and variables on the UI interface during operation, and save their values during data refresh and strategy stop, you need to add the names of parameters and variables (as string data type) to the parameters and variables lists.

Please note that this list only accepts parameters and variables with str, int, float, and bool four data types. If the strategy needs to use parameters and variables of other data types, please put the definition of that parameter or variable under the __init__ function.

### Class Initialization

Input parameters: strategy_engine, strategy_name: str, spread: SpreadData, setting: dict

Output: None

The __init__ function is the constructor of the strategy class and needs to be consistent with the inherited SpreadStrategyTemplate.

In this inherited strategy class, initialization is generally divided into three steps, as shown in the code below:

```python3
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(
            strategy_engine, strategy_name, spread, setting
        )

        self.bg = BarGenerator(self.on_spread_bar)
        self.am = ArrayManager()
```

1. Inherit SpreadStrategyTemplate through the super( ) method, and pass in the strategy engine, strategy name, spread, and parameter settings in the __init__( ) function (the above parameters are automatically passed in by the strategy engine when creating strategy instances using the strategy class, and users do not need to set them);

2. Call the K-line generation module (BarGenerator): Synthesize Tick data into 1-minute K-line data through time slicing. If needed, you can also synthesize longer time period data.

3. Call the K-line time series management module (ArrayManager): Convert K-line data into a time series data structure convenient for vectorized calculation, and internally support using the talib library to calculate corresponding technical indicators.

The default length of ArrayManager is 100. If you need to adjust the length of ArrayManager, you can pass in the size parameter for adjustment (size cannot be smaller than the cycle length for calculating indicators).

### Functions Called by Spread Strategy Engine

The update_setting function in SpreadStrategyTemplate, the four functions starting with get after this function, and the two functions starting with update after that are all functions that the spread strategy engine is responsible for calling. Generally, they do not need to be called during strategy writing.

### Strategy Callback Functions

Functions starting with on in SpreadStrategyTemplate are called callback functions and can be used to receive spread market data or receive status updates during strategy writing. The role of callback functions is that when a certain event occurs, this type of function in the strategy will be automatically called by the spread trading strategy engine (no need to actively operate in the strategy). Callback functions can be classified into the following three categories according to their functions:

#### Strategy Instance Status Control (All strategies need)

**on_init**

* Input: None

* Output: None

The on_init function is called when initializing the strategy. The default writing method is to call the write_log function to output "Strategy initialized" log, and then call the load_bar function to load historical data, as shown in the code below:

```python3
    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("Strategy initialized")
        self.load_bar(10)
```

Please note that if backtesting based on Tick data, please call the load_tick function here.

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

The on_stop function is called when stopping the strategy. The default writing method is to call the write_log function to output "Strategy stopped" log, and restore strategy variables at the same time, as shown in the code below:

```python3
    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("Strategy stopped")
        self.put_event()
```
After calling the strategy's on_stop function to stop the strategy, the strategy's trading status becomes [False], and at this time the strategy will not send trading signals.

#### Receive Data, Calculate Indicators, Send Trading Signals

**on_spread_data**

* Input: None

* Output: None

The on_spread_data function is called when spread data is updated (because the example strategy class StatisticalArbitrageStrategy in this demonstration does not trade based on on_spread_data, no example explanation is given. For example code trading based on on_spread_data, please refer to the example strategy BasicSpreadStrategy). The StatisticalArbitrageStrategy writing method is to first call get_spread_tick to obtain spread Tick data, and then push it into the on_spread_tick function, as shown in the code below:

```python3
    def on_spread_data(self):
        """
        Callback when spread price is updated.
        """
        tick = self.get_spread_tick()
        self.on_spread_tick(tick)
```

**on_spread_tick**

* Input: tick: TickData

* Output: None

When the strategy receives the latest spread Tick data market data, the on_spread_tick function is called. The default writing method is to push the received Tick data into the previously created bg instance through the BarGenerator's update_tick function to synthesize 1-minute K-lines, as shown in the code below:

```python3
    def on_spread_tick(self, tick: TickData):
        """
        Callback when new spread tick data is generated.
        """
        self.bg.update_tick(tick)
```

**on_spread_bar**

* Input: bar: BarData

* Output: None

When the strategy receives the latest spread K-line data (during live trading, the default pushed in is 1-minute K-lines synthesized based on Tick data, and during backtesting, it depends on the K-line data frequency filled in when selecting parameters), the on_spread_bar function is called.

If the strategy trades based on K-lines pushed by on_spread_bar, then please write all trading request functions under the on_spread_bar function. The example strategy class StatisticalArbitrageStrategy generates CTA signals through 1-minute K-line data returns. There are three parts in total, as shown in the code below:

```python3
    def on_spread_bar(self, bar: BarData):
        """
        Callback when spread bar data is generated.
        """
        self.stop_all_algos()

        self.am.update_bar(bar)
        if not self.am.inited:
            return

        self.boll_mid = self.am.sma(self.boll_window)
        self.boll_up, self.boll_down = self.am.boll(
            self.boll_window, self.boll_dev)

        if not self.spread_pos:
            if bar.close_price >= self.boll_up:
                self.start_short_algo(
                    bar.close_price - 10,
                    self.max_pos,
                    payup=self.payup,
                    interval=self.interval
                )
            elif bar.close_price <= self.boll_down:
                self.start_long_algo(
                    bar.close_price + 10,
                    self.max_pos,
                    payup=self.payup,
                    interval=self.interval
                )
        elif self.spread_pos < 0:
            if bar.close_price <= self.boll_mid:
                self.start_long_algo(
                    bar.close_price + 10,
                    abs(self.spread_pos),
                    payup=self.payup,
                    interval=self.interval
                )
        else:
            if bar.close_price >= self.boll_mid:
                self.start_short_algo(
                    bar.close_price - 10,
                    abs(self.spread_pos),
                    payup=self.payup,
                    interval=self.interval
                )

        self.put_event()
```

- Clear unfilled orders: To prevent previously placed orders from not being filled in the previous 1 minute but the price may have been adjusted in the next 1 minute, use the stop_all_algos() method to immediately cancel all previously unfilled orders, ensuring that the strategy's state at the beginning of the current 1 minute is clear and unique;

- Call the K-line time series management module: Calculate corresponding technical indicators based on the latest 1-minute spread K-line data, such as Bollinger Band upper and lower tracks, etc. First obtain the ArrayManager object, then push the received K-line into it, check the initialization status of ArrayManager. If it is not initialized successfully, return directly. There is no need to perform subsequent trading-related logic judgments. Because many technical indicator calculations have requirements for the minimum number of K-lines. If the number is not enough, the calculated indicators will be erroneous or meaningless. Conversely, if there is no return, you can start calculating technical indicators;

- Signal calculation: Through position judgment and combined with Bollinger Band channel, place orders at channel breakout points, and set exit points.

   Please note that if you need to refresh indicator values on the GUI, please do not forget to call the put_event() function.

#### Order Status Update

The following functions can generally be directly passed in the strategy, and their specific logic applications are left to the backtesting/live engine to be responsible for.

**on_spread_pos**

* Input: None

* Output: None

The on_spread_pos function is called when receiving position updates. Unlike the CTA strategy module accessing strategy logical positions, the spread trading module accesses the underlying account positions. So the default writing method is to call the get_spread_pos function to obtain spread positions for the strategy to perform logic judgment, as shown in the code below:

```python3
    def on_spread_pos(self):
        """
        Callback when spread position is updated.
        """
        self.spread_pos = self.get_spread_pos()
        self.put_event()
```

**on_spread_algo**

* Input: algo: SpreadAlgoTemplate

* Output: None

The on_spread_algo function is called when receiving algorithm status updates.

**on_order**

* Input: order: OrderData

* Output: None

The on_order function is called when receiving strategy order reports.

**on_trade**

* Input: trade: TradeData

* Output: None

The on_trade function is called when receiving strategy trade reports.

### Active Functions

**start_long_algo**

* Input: price: float, volume: float, payup: int, interval: int, lock: bool = False, extra: dict = None

* Output: algoid: str

**start_short_algo**

* Input: price: float, volume: float, payup: int, interval: int, lock: bool = False, extra: dict = None

* Output: algoid: str

Unlike the CTA strategy module, example spread trading strategies call the start_long_algo/start_short_algo functions (for spreads) instead of buy/sell/short/cover functions (for specific contracts) to send orders. In the spread trading module, algorithms are responsible for spread trading execution, and strategies are responsible for spread algorithm scheduling. Spread algorithms simplify spread trading to ordinary orders, encapsulating all active leg order placement and passive leg hedging details.

Taking the start_long_algo function code below as an example, you can see that price, quantity, price improvement value, and time interval are required parameters, while lock position conversion and open/close direction default to False and Offset.NONE respectively. You can also see that after receiving the passed-in parameters, the function internally calls the start_algo function in SpreadStrategyTemplate to send orders (because it is a long instruction, it automatically fills in LONG for direction)

```python3
     def start_long_algo(
        self,
        price: float,
        volume: float,
        payup: int,
        interval: int,
        lock: bool = False,
        extra: dict = None
    ) -> str:
        """"""
        if not extra:
            extra = None

        return self.start_algo(
            Direction.SHORT, price, volume,
            payup, interval, lock, extra
        )
```

**start_algo**

* Input: direction: Direction, price: float, volume: float, payup: int, interval: int, lock: bool, extra: dict

* Output: algoid: str

The start_algo function is a function for starting new spread trading algorithms called by the spread strategy engine. Generally, you do not need to call it separately when writing strategies. You can send orders through start_long_algo/start_short_algo functions.

Please note that trading orders can only be sent after the strategy is started, that is, after the strategy's trading status becomes [True]. If this function is called when the strategy's Trading status is [False], it will only return [].

**stop_algo**

* Input: algoid: str

* Output: None

**stop_all_algos**

* Input: None

* Output: None

stop_algo and stop_all_algos are both trading request functions responsible for stopping spread algorithms. stop_algo stops specified spread algorithms in the strategy, and stop_all_algos stops all active spread algorithms in the strategy.

Please note that orders can only be cancelled after the strategy is started, that is, after the strategy's trading status becomes [True].

**buy**: Buy to open (Direction: LONG, Offset: OPEN)

**sell**: Sell to close (Direction: SHORT, Offset: CLOSE)

**short**: Sell to open (Direction: SHORT, Offset: OPEN)

**cover**: Buy to close (Direction: LONG, Offset: CLOSE)

* Input: vt_symbol: str, price: float, volume: float, lock: bool = False

* Output: vt_orderids: List[vt_orderid] / None

buy/sell/short/cover are all trading request functions inside the strategy responsible for sending underlying trading orders for specific contracts. The strategy can send trading signals to the spread strategy engine through these functions to achieve the purpose of placing orders.

Taking the buy function code below as an example, you can see that local code, price, and quantity are required parameters, while lock position conversion defaults to False. You can also see that after receiving the passed-in parameters, the function internally calls the send_order function in SpreadStrategyTemplate to send orders (because it is a buy instruction, it automatically fills in LONG for direction and OPEN for offset)

If lock is set to True, the order will perform lock position order conversion (in the case of existing positions, if you want to close positions, it will first close all yesterday positions, and then the remaining part will perform reverse opening to replace closing today positions, to avoid today's closing fee penalty).

```python3
    def buy(self, vt_symbol: str, price: float, volume: float, lock: bool = False) -> List[str]:
        """"""
        return self.send_order(vt_symbol, price, volume, Direction.LONG, Offset.OPEN, lock)
```

**send_order**

* Input: vt_symbol: str, price: float, volume: float, direction: Direction, offset: Offset, lock: bool = False

* Output: vt_orderids / None

The send_order function is a function for sending orders for specific contracts (**not spreads**) called by the spread strategy engine. Generally, you do not need to call it separately when writing strategies. You can send orders through buy/sell/short/cover functions.

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

**put_event**

* Input: None

* Output: None

Calling the put_event function in the strategy can notify the GUI to refresh the strategy status related display.

Please note that the interface can only be refreshed after strategy initialization is completed and the inited status becomes [True].

**write_log**

* Input: msg: str

* Output: None

Calling the write_log function in the strategy can output logs with specified content.

**get_spread_tick**

* Input: None

* Output: tick: TickData

Calling the get_spread_tick function in the strategy can obtain spread Tick data.

**get_spread_pos**

* Input: None

* Output: spread_pos: float

Calling the get_spread_pos function in the strategy can obtain spread net position data.

**get_leg_tick**

* Input: vt_symbol: str

* Output: leg.tick: TickData / None

Calling the get_leg_tick function in the strategy can obtain Tick data for a specific contract.

**get_leg_pos**

* Input: vt_symbol: str, direction: Direction = Direction.NET

* Output: leg.net_pos: float / leg.long_pos: float / leg.short_pos: float / None

Calling the get_leg_pos function in the strategy can obtain position data for a specific contract, used for fine-grained adjustment after leg imbalance.

**send_email**

* Input: msg: str

* Output: None

After configuring email related information (for configuration methods, see the Global Configuration section in the Basic Usage chapter), calling the send_email function in the strategy can send emails with specified content to your email address.

Please note that emails can only be sent after strategy initialization is completed and the inited status becomes [True].

**load_bar**

* Input: days: int, interval: Interval = Interval.MINUTE, callback: Callable = None

* Output: None

Calling the load_bar function in the strategy can load spread K-line data during strategy initialization.

As shown in the code below, when the load_bar function is called, the default loaded days is 10, the frequency is one minute, which corresponds to loading 10 days of 1-minute K-line data. During backtesting, 10 days refers to 10 trading days, while during live trading, 10 days refers to natural days, so it is recommended that the loaded days be more rather than less. When loading, it will first try to obtain historical data through the trading interface, data service, and database in sequence until historical data is obtained or empty is returned.

Please note that during the backtesting period, if any leg's K-line data (1 minute is best) is missing for a certain segment, then all legs' segments will be discarded.

```python3
    def load_bar(
        self,
        days: int,
        interval: Interval = Interval.MINUTE,
        callback: Callable = None,
    ):
        """
        Load historical bar data for initializing strategy.
        """
        if not callback:
            callback = self.on_spread_bar

        self.strategy_engine.load_bar(self.spread, days, interval, callback)
```

**load_tick**

* Input: days: int

* Output: None

Spread Tick data source:
First, you need to create and configure the spread in the SpreadTrading module, and then use the DataRecorder module to record Ticks. The local code should be filled as xx-spread.LOCAL, where xx-spread is the user-defined spread name, and LOCAL is a fixed exchange suffix (representing locally generated).

Calling the load_tick function in the strategy can load recorded spread Tick order book data from the database during strategy initialization.
