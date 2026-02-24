# CtaStrategy - CTA Automatic Trading Module

## Function Overview

CtaStrategy is a functional module for **CTA automatic trading**. Users can conveniently complete tasks such as strategy initialization, strategy start, strategy stop, strategy parameter editing, and strategy removal through its UI interface.

## Loading and Launching

### Loading via VeighNa Station

After launching and logging into VeighNa Station, click the [Trading] button. In the configuration dialog, check [CtaStrategy] in the [Application Module] section.

### Loading via Script

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_ctastrategy import CtaStrategyApp

# Write after creating the main_engine object
main_engine.add_app(CtaStrategyApp)
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

After successfully connecting to the trading interface, click [Function] -> [CTA Strategy] in the menu bar, or click the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/00.png)

You can then enter the UI interface of the CTA strategy module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/2.png)

If a data service is configured (for configuration methods, see the Global Configuration section in the Basic Usage chapter), data service login initialization is automatically executed when opening the CTA strategy module. If login is successful, "Data service initialization successful" log will be output, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/ctas.png)


## Adding Strategies

Users can create different strategy instances (objects) based on written CTA strategy templates (classes). The benefit of strategy instances is that the same strategy can trade multiple variety contracts simultaneously, and each instance's parameters can be different.

Select the strategy name to trade from the dropdown box in the upper left corner, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/28.png)

Please note that the displayed strategy name is the name of the **strategy class** (camelCase naming), not the strategy file (underscore naming).

After selecting the strategy class, click [Add Strategy] to pop up the add strategy dialog, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/5.png)

When creating a strategy instance, you need to configure relevant parameters. The parameter requirements are as follows:

- Instance Name
  - Instance names cannot be duplicated;
- Contract Variety
  - Format is vt_symbol (contract code + exchange name);
  - Must be a contract name that can be found in the live trading system;
  - Generally choose the month with the best liquidity for the futures variety;
- Parameter Settings
  - The displayed parameter names are the parameter names written in the parameters list in the strategy;
  - Default values are the default values of parameters in the strategy;
  - As observed in the figure above, the data type of the parameter is displayed in the <> brackets after the parameter name. When filling in parameters, you should follow the corresponding data type. Among them, <class 'str'> is string, <class 'int'> is integer, <class 'float'> is float;
  - Please note that if a parameter may be adjusted to a value with decimal places, and the default parameter value is an integer (such as 1). When writing the strategy, set the default parameter value to a float (such as 1.0). Otherwise, the strategy will default that parameter to an integer, and when subsequently [Editing] the strategy instance parameters, only integers will be allowed.

After parameter configuration is completed, click the [Add] button to start creating the strategy instance. After successful creation, you can see the strategy instance in the strategy monitoring component on the left side, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/47.png)

The top of the strategy monitoring component displays the strategy instance name, contract variety name, strategy class name, and strategy author name (author defined in the strategy). The top buttons are used to control and manage the strategy instance. The first row of the table displays the parameter information inside the strategy (parameter names need to be written in the strategy's parameters list to be displayed in the GUI). The second row of the table displays the variable information during strategy operation (variable names need to be written in the strategy's variables list to be displayed in the GUI). The [inited] field indicates the current initialization status of the strategy (whether historical data playback has been completed), and the [trading] field indicates whether the strategy can currently start trading.

As observed in the figure above, at this time the strategy instance's [inited] and [trading] status are both [False]. This indicates that the strategy instance has not been initialized yet and cannot send trading signals.

After the strategy instance is successfully created, the strategy instance configuration information will be saved to the cta_strategy_setting.json file under the .vntrader folder.

### Creation Failure

The following are several possible situations where strategy instance creation fails:

- If a strategy instance with the same name is added, creation will fail, and the GUI will output "Strategy creation failed, duplicate name exists" log information, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/48.png)

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/49.png)

- If the exchange name is not filled in for the contract variety, creation will fail, and the GUI will output "Strategy creation failed, local code missing exchange suffix" log information, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/50.png)

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/51.png)

- If the exchange name for the contract variety is filled incorrectly, creation will fail, and the GUI will output "Strategy creation failed, local code exchange suffix is incorrect" information, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/52.png)

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/53.png)


## Managing Strategies

### Initialization

After the strategy instance is successfully created, you can initialize the instance. Click the [Initialize] button under the strategy instance. If initialization is successful, it is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/54.png)

During the initialization process, the following three steps are mainly completed in sequence:

1. Obtain Historical Data

   To ensure the accuracy of indicator values within the strategy, each strategy instance needs a certain amount of historical data for strategy initialization.

   Therefore, during strategy initialization, the load_bar function inside the strategy instance will first obtain the latest historical data from the interface. If the interface does not provide historical data, it will be obtained through the configured data service (taking RQData as an example, [RQData](https://www.ricequant.com/welcome/purchase?utm_source=vnpy) provides historical data for domestic futures, stocks, and options. RQData's data service provides intraday K-line updates. Even if the strategy is launched at 9:45, it can still obtain K-line data from 9:30 to 9:45 for strategy initialization calculation, without worrying about data missing issues). If no data service is configured, it will query by accessing the local database. In this case, users need to ensure data integrity in the database (meeting initialization requirements), which can be recorded through DataRecorder or imported from CSV files using DataManager.

   The specific length of loaded data depends on the parameter control of the load_bar function (strategy template default is 10 days). After data loading, it will be pushed to the strategy in the form of K-line by K-line (or Tick by Tick) to achieve internal variable initialization calculation, such as caching K-line sequences and calculating technical indicators.

2. Load Cached Variables

   During daily live operation, some variables in quantitative strategies are only related to historical market data. Such variables can obtain correct values by loading historical data playback. Another type of variable may be related to trading status, such as strategy positions, moving stop-loss highest price tracking, etc. Such variables need to be cached on the hard disk (when exiting the program) and read and restored after replaying historical data the next day to ensure consistency with previous trading status.

   Each time the strategy is stopped, the variables corresponding to the strategy's variables list and strategy positions are automatically cached into the cta_strategy_data.json file under the .vntrader directory, so as to be automatically loaded during the next strategy initialization.

   Please note that in some situations (such as manual position closing), cached data may have deviations (because the strategy position maintains the logical position of the running strategy instance, not the position of a specific variety). In such cases, you can adjust by manually modifying the json file.

3. Subscribe to Market Data Push

   Finally, obtain the information of the contract traded by the strategy based on the vt_symbol parameter, and subscribe to the contract's real-time market data push. If the live trading system cannot find the contract information, such as not connecting to the login interface or vt_symbol filled incorrectly, corresponding error information will be output in the log module.

After the above three steps are completed, you can observe that the strategy instance's [inited] status is already [True], and variables also display corresponding values (no longer 0). This indicates that the strategy instance has called the load_bar function to load historical data and completed initialization. The [trading] status is still [False], indicating that the strategy instance cannot start automatic trading yet.

### Initialization Failure

The following are several possible situations where strategy instance creation fails:
- Even if the exchange filled is a VeighNa-supported exchange name and the strategy instance is successfully created, if the contract name is entered incorrectly (such as case errors, contract doesn't match exchange, or has been delisted), causing the live trading system to not find the contract, initialization will fail. At this time, the GUI outputs "Market subscription failed, contract not found" log. As shown in the figure below:

  ![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/55.png)

- Even if the contract code is filled correctly and the strategy instance is successfully created, if the interface has not been connected yet, or the interface contract information query operation has not been completed, causing the live trading system to not find the contract, initialization will also fail. At this time, the GUI outputs "Market subscription failed, contract not found" log. As shown in the figure below:

  ![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/56.png)

  If problems like "Market subscription failed, contract not found" occur, you can query by clicking [Help] - [Query Contract] on the VeighNa Trader main interface to find the correct contract information. As shown in the figure below:

  ![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/57.png)

- If the strategy uses the K-line time series management module (ArrayManager) to calculate variable indicator values, please ensure the historical data length is sufficient for ArrayManager initialization (the default ArrayManager needs 100 data points to initialize successfully). If the historical data length is not enough for ArrayManager initialization, even if the GUI outputs the log "Initialization completed", the strategy instance initialization is still a failure.

  - If the strategy logic is based on the example strategy, returning immediately once ArrayManager is not initialized successfully (if not am.inited), then as observed in the figure below, the values of strategy indicators calculated based on ArrayManager in the strategy instance on the left side of the GUI are all 0. This indicates that although the strategy instance can start automatic trading after startup, because ArrayManager is not initialized successfully, the strategy logic returns every time it reaches the ArrayManager initialization status judgment, and cannot reach the logic of calculating indicators and sending trading signals. Therefore, the strategy instance needs to wait until the data pushed into the strategy instance is enough for ArrayManager initialization, satisfying the ArrayManager initialization judgment condition, before it can truly send trading signals.
  ![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/58.png)

  - If the strategy logic is not based on returning immediately once ArrayManager is not initialized successfully (if not am.inited) in the example strategy, then although the strategy indicators in the strategy instance on the left side of the GUI have specific values, and trading signals can be sent at this time without waiting for ArrayManager initialization to complete, because ArrayManager is not initialized successfully, the variable indicator values calculated by the strategy instance are inaccurate, which may send trading signals that do not meet strategy expectations.

### Start

Only when the strategy instance is initialized successfully and the [inited] status is [True] can the automatic trading function be started. Click the [Start] button under the strategy instance to start the strategy instance. After success, it is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/59.png)

You can observe that at this time the strategy instance's [inited] and [trading] status are both [True]. This indicates that the strategy instance has called the load_bar function, completed historical data playback, and at this time the trading request functions inside the strategy (buy/sell/short/cover/cancel_order, etc.) and information output functions (send_email/put_event, etc.) will truly execute and send corresponding request commands to the underlying interface (truly executing trading).

In the previous strategy initialization process, although the strategy was also receiving (historical) data and calling corresponding function functions, because the [trading] status was [False], there were no real order placement operations or trading-related log information output.

If the strategy sends limit orders after starting, you can view order details in the [Order] bar on the VeighNa Trader main interface. If the strategy sends local stop orders, you can view order details in the stop order monitoring component in the upper right area of the CTA strategy UI interface.

### Stop

If after starting the strategy, due to certain situations (such as market closing time, or encountering emergency situations during trading) you want to stop, edit, or remove the strategy, you can click the [Stop] button under the strategy instance to stop the strategy instance's automatic trading. After success, it is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/60.png)

The CTA strategy engine will automatically cancel all active orders sent by the strategy before, to ensure that there are no out-of-control orders after the strategy stops. At the same time, the latest variable information of the strategy instance will be saved to the cta_strategy_data.json file under the .vntrader folder.

At this time, you can observe that the strategy instance's [trading] status has become [False], indicating that the strategy instance has stopped automatic trading.

During CTA strategy live trading, under normal circumstances, the strategy should run automatically throughout the entire trading period, and extra pause/restart operations should be avoided as much as possible. For the domestic futures market, automatic trading should be started before the trading period begins, and then closed after the market closes. Because now CTP also closes the system after night trading closes and restarts before morning open, so you also need to stop the strategy and close VeighNa Trader after night trading closes.

### Edit

If after creating a strategy instance, you want to edit the parameters of a certain strategy instance (if the strategy has been started, you need to click the [Stop] button under the strategy instance first to stop the strategy), you can click the [Edit] button under the strategy instance, and a parameter editing dialog will pop up for modifying strategy parameters. As shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/61.png)

After editing the strategy parameters, click the [OK] button below, and the corresponding modifications will be immediately updated in the parameter table, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/62.png)

However, the strategy instance's trading contract code cannot be modified, and no re-initialization operation will be executed after modification. Also note that at this time only the parameter values of the strategy instance in the cta_strategy_setting.json file under the .vntrader folder are modified, not the parameters in the original strategy file.

Before modification, the json file is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/63.png)

After modification, the json file is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/64.png)

If you want to start the strategy again after editing during trading, click the [Start] button under the strategy instance to start the strategy instance again, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/65.png)

### Remove

If after creating a strategy instance, you want to remove a certain strategy instance (if the strategy has been started, you need to click the [Stop] button under the strategy instance first to stop the strategy), you can click the [Remove] button under the strategy instance. After successful removal, the strategy monitoring component on the left side of the GUI will no longer display the strategy instance information. As shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/66.png)

At this time, the cta_strategy_setting.json file under the .vntrader folder has also removed the configuration information of the strategy instance.

### Status Tracking

If you want to track the strategy status through the GUI, there are two ways:

1. Call the put_event function

   All variable information in the strategy instance needs to have the variable name written in the strategy's variables list to be displayed in the GUI. If you want to track variable status changes, you need to call the put_event function in the strategy, and the interface will refresh the data.

   Sometimes users find that no matter how long their strategy runs, the variable information does not change. In this case, please check whether the call to the put_event function is missing in the strategy.

2. Call the write_log function

   If you not only want to observe variable information status changes but also want to output personalized logs based on your own needs according to the strategy status, you can call the write_log function in the strategy for log output.

## Running Logs

### Log Content

There are two sources of logs output on the CTA strategy module UI interface: the CTA strategy engine and strategy instances.

**Engine Logs**

The CTA strategy engine generally outputs global information. In the figure below, except for content starting with the strategy instance name in square brackets, all are logs output by the CTA strategy engine.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/67.png)

**Strategy Logs**

If the write_log function is called in the strategy, the log content will be output through strategy logs. The content in the red boxes in the figure below are strategy logs output by two different strategy instances. The content in square brackets is the strategy instance name, and the content after the square brackets is what the write_log function outputs.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/68.png)

### Clear Operation

If you want to clear the log output on the CTA strategy UI interface, you can click the [Clear Logs] button in the upper right corner to clear all output logs on the interface with one click.

Before clicking [Clear Logs], as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/66.png)

After clicking [Clear Logs], as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/70.png)


## Stop Orders

The stop order monitoring component in the upper right area of the GUI is used to track the status changes of all local stop orders in the CTA engine.

Because not all interfaces support stop orders, VeighNa provides the local stop order function. When the trading interface does not support exchange stop orders, users can still enable the local stop order function by setting the stop parameter to True through the strategy's order function (buy/sell/short/cover).

VeighNa's local stop orders have three characteristics:

1. Saved on the local computer, invalid after shutdown;
2. Only visible to the trader, no need to worry about leaking your hand;
3. Stop order triggering has delays, causing certain slippage.

**Stop Order Information**

After sending a local stop order, the monitoring component in the upper right of the GUI will display the order details of the stop order.

Local stop orders have three states: [Waiting], [Triggered], and [Cancelled], as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/71.png)

When the stop order is first sent, it is in the [Waiting] state. Because the stop order information is recorded locally and not sent to the exchange, there will be no changes in the [Order] bar on the main interface at this time.

Once the stop order's order price is triggered, in order to achieve immediate execution, the CTA strategy engine will immediately send **limit** orders at **limit up/down prices** or **five-level order book** prices (so it is recommended to use local stop orders only for contracts with good liquidity). After the limit order is sent, the [Order] bar on the VeighNa Trader main interface will update the order status. At this time, the stop order status will become [Triggered], and the [Limit Order Number] column will also be filled with the order's limit order number.

Please note that **the price displayed in the stop order interface is the trigger price of the local stop order, not the price of the sent limit order**.

If the stop order is cancelled by the strategy before being triggered, the order status will become [Cancelled].


## Batch Operations

When the strategy has been fully tested, runs stably in live trading, and does not need frequent adjustments, if there are multiple CTA strategy instances to run, you can use the [Initialize All], [Start All], and [Stop All] functions in the upper right corner of the interface to execute pre-market batch initialization, start strategy instances, and post-market batch stop strategy instances operations.

### Initialize All

After all strategy instances are successfully created, click the [Initialize All] button in the upper right corner to batch initialize strategy instances.

Before clicking [Initialize All], as shown in the figure below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/72.png)

After clicking [Initialize All], as shown in the figure below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/73.png)

### Start All

After all strategy instances are successfully initialized, click the [Start All] button in the upper right corner to batch start strategy instances, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/74.png)

### Stop All

After all strategy instances are successfully started, click the [Stop All] button in the upper right corner to batch stop strategy instances, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/75.png)


## Position Transfer Assistant

If you need to use the automatic position transfer assistant, please complete strategy initialization first, then click the [Position Transfer Assistant] button for the strategy to execute position transfer. The position transfer assistant dialog will pop up, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/76.png)

First, configure the position transfer tasks to be executed in the left area, where:

- Transfer Contract: This dropdown box displays the local codes of all contracts traded by all strategy instances under the current CTA strategy module. Select the old contract to be closed;
- Target Contract: The local code (vt_symbol) of the contract to transfer the old positions and strategies to. Enter the new contract to open;
- Order Price Improvement: The pricetick that the order price exceeds the opposite side of the order book when executing position transfer trading.

After completing the configuration and confirming it is correct, click the [Transfer] button to start execution. During the position transfer process, logs will be output as shown in the figure below. After completion, the dialog will be locked (turned gray and cannot be clicked again):

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/77.png)

You can see that the position transfer operations for all positions and strategies corresponding to the transfer contract were completed in almost 1 second, and at the same time, the strategy trading code on the CTA strategy module interface has become the target contract.

The specific task steps executed during the position transfer process are as follows:

- Position Transfer:

  - Close [all positions] of the transfer contract in the current account (note that this does not distinguish between strategy positions and manual trading positions), and record the corresponding positions (recorded separately for long and short);
  - Execute opening trades for the target contract. The opening price is the opposite side of the order book at that time plus the price improvement pricetick, and the quantity is the original transfer contract position recorded in the previous step.

- Strategy Transfer:

  - Record the [logical positions] of all strategies whose trading object is the transfer contract in the current CTA strategy module (note that the logical positions here may not fully correspond to the actual account positions);
  - Delete the old strategy instances whose trading object is the transfer contract, and create new strategy instances with the same name using the target contract as the trading target;
  - Initialize the new strategy instances, and update the [logical positions] of the old strategy instances recorded previously to the new strategy status.

Return to the VeighNa Trader main interface, where you can also view detailed position transfer order and trade records. As shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/78.png)


## CTA Strategy Template (CtaTemplate)

The CTA strategy template provides signal generation and order management functions. Users can develop CTA strategies based on this template (located in site-packages\vnpy_ctastrategy\template).

User-developed strategies can be placed in the [strategies](#jump) folder under the user's running folder.

Please note:

1. Strategy file naming uses underscore mode, such as boll_channel_strategy.py, while strategy class naming uses camelCase, such as BollChannelStrategy.

2. The class name of self-built strategies should not coincide with the class names of example strategies. If they coincide, only one strategy class name will be displayed on the GUI.

The following uses the BollChannelStrategy strategy example to demonstrate the specific steps of strategy development:

Before writing strategy logic based on the CTA strategy template, you need to load the internal components needed at the top of the strategy file, as shown in the code below:

```python3
from vnpy_ctastrategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
    ArrayManager
)
```

Among them, CtaTemplate is the CTA strategy template, StopOrder, TickData, BarData, TradeData, and OrderData are data containers storing corresponding information, BarGenerator is the K-line generation module, and ArrayManager is the K-line time series management module.

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

    boll_up = 0
    boll_down = 0
    cci_value = 0
    atr_value = 0

    intra_trade_high = 0
    intra_trade_low = 0
    long_stop = 0
    short_stop = 0

    parameters = [
        "boll_window",
        "boll_dev",
        "cci_window",
        "atr_window",
        "sl_multiplier",
        "fixed_size"
    ]
    variables = [
        "boll_up",
        "boll_down",
        "cci_value",
        "atr_value",
        "intra_trade_high",
        "intra_trade_low",
        "long_stop",
        "short_stop"
    ]

```

Although strategy parameters and variables both belong to the strategy class, strategy parameters are fixed (specified by the trader externally), while strategy variables change with the strategy status during trading, so strategy variables only need to be initialized to corresponding basic types at the beginning. For example: integers set to 0, floats set to 0.0, and strings set to "".

If you need the CTA engine to display strategy parameters and variables on the UI interface during operation, and save their values during data refresh and strategy stop, you need to add the names of parameters and variables (as string data type) to the parameters and variables lists.

Please note that this list only accepts parameters or variables with str, int, float, and bool four data types. If the strategy needs to use parameters and variables of other data types, please put the definition of that parameter or variable under the __init__ function.

### Class Initialization

Input parameters: cta_engine: Any, strategy_name: str, vt_symbol: str, setting: dict

Output: None

The __init__ function is the constructor of the strategy class and needs to be consistent with the inherited CtaTemplate.

In this inherited strategy class, initialization is generally divided into three steps, as shown in the code below:

```python3
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        self.bg = BarGenerator(self.on_bar, 15, self.on_15min_bar)
        self.am = ArrayManager()
```

1. Inherit the CTA strategy template through the super( ) method, and pass in the CTA engine, strategy name, vt_symbol, and parameter settings in the __init__( ) function. Note that the CTA engine can be either a live engine or a backtesting engine, which can conveniently **achieve running backtesting and live with the same code** (the above parameters are automatically passed in by the strategy engine when creating strategy instances using the strategy class, and users do not need to set them).

2. Call the K-line generation module (BarGenerator): Synthesize Tick data into 1-minute K-line data through time slicing. If needed, you can also synthesize longer time period data, such as 15-minute K-lines.

If you only trade based on on_bar, the code here can be written as:

```python3
        self.bg = BarGenerator(self.on_bar)
```

And you don't need to pass in the longer K-line period to be synthesized based on the on_bar period, and the function name to receive longer K-line periods to the bg instance.

Please note that when synthesizing X-minute lines, X must be set to a number divisible by 60 (except 60). There is no such limit for synthesizing hour lines.

The default data frequency for BarGenerator to synthesize long-period K-lines based on the on_bar function is minute level. If you need to trade based on synthesized hour lines or longer period K-lines, please import Interval at the top of the strategy file and pass in the corresponding data frequency to the bg instance. As shown in the code below:

Import Interval at the top of the file:

```python3
from vnpy.trader.constant import Interval
```

Pass in data frequency when creating bg instance in __init__ function:

```python3
        self.bg = BarGenerator(self.on_bar, 2, self.on_2hour_bar, Interval.HOUR)
```

3. Call the K-line time series management module (ArrayManager): Based on K-line data, such as 1-minute, 15-minute, convert it into a time series data structure convenient for vectorized calculation, and internally support using the talib library to calculate corresponding technical indicators.

The default length of ArrayManager is 100. If you need to adjust the length of ArrayManager, you can pass in the size parameter for adjustment (size cannot be smaller than the cycle length for calculating indicators).

### Functions Called by CTA Strategy Engine

The update_setting function in CtaTemplate and the four functions starting with get after this function are all functions that the CTA strategy engine is responsible for calling. Generally, they do not need to be called during strategy writing.

### Strategy Callback Functions

Functions starting with on in CtaTemplate are called callback functions and can be used to receive data or receive status updates during strategy writing. The role of callback functions is that when a certain event occurs, this type of function in the strategy will be automatically called by the CTA strategy engine (no need to actively operate in the strategy). Callback functions can be classified into the following three categories according to their functions:

#### Strategy Instance Status Control (All strategies need)

**on_init**

* Input: None

* Output: None

The on_init function is called when initializing the strategy. The default writing method is to first call the write_log function to output "Strategy initialized" log, and then call the load_bar function to load historical data, as shown in the code below:

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

When the strategy receives the latest Tick data market push, the on_tick function is called. The default writing method is to push the received Tick data into the previously created bg instance through the BarGenerator's update_tick function to synthesize 1-minute K-lines, as shown in the code below:

```python3
    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)
```

**on_bar**

* Input: bar: BarData

* Output: None

When the strategy receives the latest K-line data (during live trading, the default pushed in is 1-minute K-lines synthesized based on Tick data, and during backtesting, it depends on the K-line data frequency filled in when selecting parameters), the on_bar function is called. There are two writing methods that have appeared in example strategies:

1. If the strategy trades based on K-lines pushed by on_bar, then please write all trading request functions under the on_bar function (because the example strategy class BollChannelStrategy in this demonstration does not trade based on on_bar, no example explanation is given. For example code trading based on on_bar, please refer to other example strategies);

2. If the strategy needs to synthesize longer time period K-lines through BarGenerator based on K-line data pushed by on_bar to trade, then please call the BarGenerator's update_bar function in on_bar to push the received bar into the previously created bg instance, as shown in the code below:

```python3
    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.bg.update_bar(bar)
```

The example strategy class BollChannelStrategy generates CTA signals through 15-minute K-line data returns. There are three parts in total, as shown in the code below:

```python3
    def on_15min_bar(self, bar: BarData):
        """"""
        self.cancel_all()

        am = self.am
        am.update_bar(bar)
        if not am.inited:
            return

        self.boll_up, self.boll_down = am.boll(self.boll_window, self.boll_dev)
        self.cci_value = am.cci(self.cci_window)
        self.atr_value = am.atr(self.atr_window)

        if self.pos == 0:
            self.intra_trade_high = bar.high_price
            self.intra_trade_low = bar.low_price

            if self.cci_value > 0:
                self.buy(self.boll_up, self.fixed_size, True)
            elif self.cci_value < 0:
                self.short(self.boll_down, self.fixed_size, True)

        elif self.pos > 0:
            self.intra_trade_high = max(self.intra_trade_high, bar.high_price)
            self.intra_trade_low = bar.low_price

            self.long_stop = self.intra_trade_high - self.atr_value * self.sl_multiplier
            self.sell(self.long_stop, abs(self.pos), True)

        elif self.pos < 0:
            self.intra_trade_high = bar.high_price
            self.intra_trade_low = min(self.intra_trade_low, bar.low_price)

            self.short_stop = self.intra_trade_low + self.atr_value * self.sl_multiplier
            self.cover(self.short_stop, abs(self.pos), True)

        self.put_event()
```

- Clear unfilled orders: To prevent previously placed orders from not being filled in the previous 15 minutes but the price may have been adjusted in the next 15 minutes, use the cancel_all() method to immediately cancel all previously unfilled orders, ensuring that the strategy's state at the beginning of the current 15 minutes is clear and unique;

- Call the K-line time series management module: Calculate corresponding technical indicators based on the latest 15-minute K-line data, such as Bollinger Band upper and lower tracks, CCI indicator, ATR indicator, etc. First obtain the ArrayManager object, then push the received K-line into it, check the initialization status of ArrayManager. If it is not initialized successfully, return directly. There is no need to perform subsequent trading-related logic judgments. Because many technical indicator calculations have requirements for the minimum number of K-lines. If the number is not enough, the calculated indicators will be erroneous or meaningless. Conversely, if there is no return, you can start calculating technical indicators;

- Signal calculation: Through position judgment and combined with CCI indicator, Bollinger Band channel, and ATR indicator, place stop orders (buy/sell) at channel breakout points, and set exit points (short/cover).

    Please note that if you need to refresh indicator values on the GUI, please do not forget to call the put_event() function.

#### Order Status Update

The following functions can be directly passed in the strategy, and their specific logic applications are left to the backtesting/live engine to be responsible for.

**on_trade**

* Input: trade: TradeData

* Output: None

The on_trade function is called when receiving strategy trade reports.

**on_order**

* Input: order: OrderData

* Output: None

The on_order function is called when receiving strategy order reports.

**on_stop_order**

* Input: stop_order: StopOrder

* Output: None

The on_stop_order function is called when receiving strategy stop order reports.

### Active Functions

**buy**: Buy to open (Direction: LONG, Offset: OPEN)

**sell**: Sell to close (Direction: SHORT, Offset: CLOSE)

**short**: Sell to open (Direction: SHORT, Offset: OPEN)

**cover**: Buy to close (Direction: LONG, Offset: CLOSE)

* Input: price: float, volume: float, stop: bool = False, lock: bool = False, net: bool = False

* Output: vt_orderids: List[vt_orderid] / None

buy/sell/short/cover are all trading request functions inside the strategy responsible for sending orders. The strategy can send trading signals to the CTA strategy engine through these functions to achieve the purpose of placing orders.

Taking the buy function code below as an example, you can see that price and quantity are required parameters, while stop order conversion, lock position conversion, and net position conversion default to False. You can also see that after receiving the passed-in parameters, the function internally calls the send_order function in CtaTemplate to send orders (because it is a buy instruction, it automatically fills in LONG for direction and OPEN for offset)

If stop is set to True, the order will be automatically converted to a stop order. If the interface supports exchange stop orders, it will be converted to an exchange stop order. If the interface does not support exchange stop orders, it will be converted to VeighNa's local stop order.

If lock is set to True, the order will perform lock position order conversion (in the case of existing positions, and the exchange being traded is not an exchange that specifies closing today or yesterday, it will directly open in the opposite direction. In the case of existing yesterday positions, if you want to close positions, it will first close all yesterday positions, and then the remaining part will perform reverse opening to replace closing today positions, to avoid today's closing fee penalty).

If net is set to True, the order will perform net position order conversion (based on all positions of the overall account, convert the opening and closing direction of the strategy order according to the net position holding method). However, the net position trading mode and lock position trading mode are mutually exclusive, so when net is set to True, lock must be set to False.

Please note that if sending a closing order to the Shanghai Futures Exchange, because the exchange must specify closing today or closing yesterday, the underlying layer will automatically convert its closing instructions. Because some varieties of the Shanghai Futures Exchange have today's closing fee discounts, by default, orders are sent with today's closing priority (if the trading target has yesterday's closing fee discount on the Shanghai Futures Exchange, you can make appropriate modifications in the convert_order_request_shfe function of vnpy.trader.converter).

```python3
    def buy(self, price: float, volume: float, stop: bool = False, lock: bool = False, net: bool = False):
        """
        Send buy order to open a long position.
        """
        return self.send_order(Direction.LONG, Offset.OPEN, price, volume, stop, lock, net)
```

Please note that domestic futures have the concept of opening and closing positions, for example, buy operations need to be distinguished into buy to open and buy to close; but for stocks and foreign futures, they are all net position mode, without the concept of opening and closing positions, so you only need to use the buy and sell instructions.

**send_order**

* Input: direction: Direction, offset: Offset, price: float, volume: float, stop: bool = False, lock: bool = False, net: bool = False

* Output: vt_orderids / None

The send_order function is a function for sending orders called by the CTA strategy engine. Generally, you do not need to call it separately when writing strategies. You can send orders through buy/sell/short/cover functions.

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

**write_log**

* Input: msg: str

* Output: None

Calling the write_log function in the strategy can output logs with specified content.

**get_engine_type**

* Input: None

* Output: engine_type: EngineType

If the strategy has different logic processing during backtesting and live trading, you can call the get_engine_type function to obtain the current engine type for logic judgment.

Please note that if you want to call this function for logic judgment, please import "EngineType" at the top of the strategy file.

**get_pricetick**

* Input: None

* Output: pricetick: float / None

Calling the get_pricetick function in the strategy can obtain the minimum price movement of the trading contract.

**load_bar**

* Input: days: int, interval: Interval = Interval.MINUTE, callback: Callable = None, use_database: bool = False

* Output: None

Calling the load_bar function in the strategy can load K-line data during strategy initialization.

As shown in the code below, when calling the load_bar function, the default loaded days is 10, the frequency is one minute, which corresponds to loading 10 days of 1-minute K-line data. 10 days refers to 10 natural days. It is recommended that the loaded days be more rather than less. The use_database parameter defaults to False, and it will first try to obtain historical data through the trading interface, data service, and database in sequence until historical data is obtained or empty is returned. When use_database is set to True, it will skip obtaining historical data through the trading interface and data service, and directly query the database.

```python3
    def load_bar(
        self,
        days: int,
        interval: Interval = Interval.MINUTE,
        callback: Callable = None,
        use_database: bool = False
    ):
        """
        Load historical bar data for initializing strategy.
        """
        if not callback:
            callback = self.on_bar

        self.cta_engine.load_bar(
            self.vt_symbol,
            days,
            interval,
            callback,
            use_database
        )
```

**load_tick**

* Input: days: int

* Output: None

Calling the load_tick function in the strategy can load Tick data during strategy initialization.

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

Calling the sync_data function in the strategy can synchronize strategy variables to the corresponding json file for local caching every time the strategy stops or trades during live trading, convenient for reading and restoring the next day during initialization (the CTA strategy engine will call it, and there is no need to actively call it in the strategy).

Please note that strategy information can only be synchronized after the strategy is started, that is, after the strategy's trading status becomes [True].
