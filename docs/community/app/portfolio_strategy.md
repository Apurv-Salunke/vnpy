# PortfolioStrategy - Multi-Contract Portfolio Strategy Module

## Function Introduction

PortfolioStrategy is a functional module for **multi-contract portfolio strategy live trading**. Users can use its UI interface to easily complete tasks such as strategy initialization, strategy start, strategy stop, strategy parameter editing, and strategy removal.

## Loading and Starting

### VeighNa Station Loading

After starting and logging into VeighNa Station, click the 【Trading】 button, and check the 【PortfolioStrategy】 in the 【Application Module】 column in the configuration dialog.

### Script Loading

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_portfoliostrategy import PortfolioStrategyApp

# Write after creating the main_engine object
main_engine.add_app(PortfolioStrategyApp)
```


## Starting the Module

<span id="jump">

For strategies developed by users, they need to be placed in the **strategies** directory under the runtime directory of VeighNa Trader to be recognized and loaded. The specific runtime directory path can be viewed in the title bar at the top of the main interface of VeighNa Trader.

For users who are default installed on Windows, the path to the strategies directory is usually:

```
    C:\Users\Administrator\strategies
```

Where Administrator is the system username of the currently logged in Windows.

</span>

Before starting the module, please connect to the trading interface (the connection method is detailed in the basic usage section of the connection interface). After seeing the output of "Contract information query successful" in the VeighNa Trader main interface 【Log】 column, start the module as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/1.png)

Please note that the IB interface cannot automatically obtain all contract information when logging in, and can only obtain it when the user manually subscribes to market data. Therefore, you need to manually subscribe to market data on the main interface before starting the module.

After successfully connecting to the trading interface, click on the 【Function】-> 【Portfolio Strategy】 in the menu bar, or click on the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/0.png)

You can enter the UI interface of the multi-contract portfolio strategy module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/1.png)

If the data service is configured (the configuration method is detailed in the global configuration section of the basic usage section), the data service login initialization will be automatically executed when the multi-contract portfolio strategy module is opened. If the login is successful, the log will output "Data service initialization successful", as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/2.png)


## Adding a Strategy

Users can create different strategy instances (objects) based on the written combination strategy template (class).

Select the strategy name to be traded in the drop-down box in the upper left corner, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/3.png)

Please note that the displayed strategy name is the **strategy class** (camel case naming), not the strategy file (underscore mode naming) name.

After selecting the strategy class, click on the 【Add Strategy】 button, and the add strategy dialog will pop up, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/4.png)

When creating a strategy instance, you need to configure the relevant parameters. The requirements for each parameter are as follows:

- Instance name
  - The instance name cannot be duplicated;
- Contract variety
  - The format is vt_symbol (contract code + exchange name);
  - It must be a contract name that can be found in the live trading system;
  - The contract name is separated by "," without spaces in between;
- Parameter settings
  - The displayed parameter name is the parameter name written in the parameters list of the strategy;
  - The default value is the default value of the parameter in the strategy;
  - As can be observed from the figure above, the data type of the parameter is displayed in the <> brackets after the parameter name. When filling in the parameter, you should follow the corresponding data type. Among them, <class 'str'> is a string, <class 'int'> is an integer, <class 'float'> is a floating point number;
- Instance name
  - The instance name cannot be duplicated;
- Contract variety
  - The format is vt_symbol (contract code + exchange name);
  - It must be a contract name that can be found in the live trading system;
  - The contract name is separated by "," without spaces in between;
- Parameter settings
  - The displayed parameter name is the parameter name written in the parameters list of the strategy;
  - The default value is the default value of the parameter in the strategy;
  - As can be observed from the figure above, the data type of the parameter is displayed in the <> brackets after the parameter name. When filling in the parameter, you should follow the corresponding data type. Among them, <class 'str'> is a string, <class 'int'> is an integer, <class 'float'> is a floating point number;
  - Please note that if a parameter may be adjusted to a value with decimal places, and the default parameter value is an integer (such as 1). Please set the default parameter value to a floating point number (such as 1.0) when writing the strategy. Otherwise, the strategy will default this parameter to an integer, and when editing the strategy instance parameters in the subsequent [Edit], only integers will be allowed to be filled in.

After the parameter configuration is completed, click the 【Add】 button to start creating the strategy instance. After the creation is successful, you can see the strategy instance in the left strategy monitoring component, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/5.png)

The top of the strategy monitoring component displays the strategy instance name, strategy class name, and strategy author name (defined in the author of the strategy). The top button is used to control and manage the strategy instance, the first row of the table shows the parameter information inside the strategy (the parameter name needs to be written in the parameters list of the strategy for the graphical interface to display), and the second row of the table shows the variable information during the operation of the strategy (the variable name needs to be written in the variables list of the strategy for the graphical interface to display). The [inited] field indicates the initialization status of the current strategy (whether the historical data playback has been completed), and the [trading] field indicates whether the strategy can currently start trading.

As can be observed from the figure above, at this time, the [inited] and [trading] statuses of this strategy instance are both [False]. This indicates that the strategy instance has not been initialized and cannot yet send out trading signals.

After the successful creation of the strategy instance, the configuration information of this strategy instance will be saved to the portfolio_strategy_setting.json file under the .vntrader folder.

Please note that if a strategy instance with the same name is added, the creation will fail, and the graphical interface will output the log information "Failed to create strategy, duplicate name exists", as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/8.png)


## Managing Strategies

### Initialization

After the strategy instance is successfully created, you can initialize the instance. Click the [Initialize] button under the strategy instance, if the initialization is successful, it will be as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/6.png)

After the initialization is completed, it can be observed that the [inited] status of the strategy instance is already [True]. This indicates that the strategy instance has already loaded historical data and completed initialization. The [trading] status is still [False], indicating that the strategy instance cannot start automatic trading at this time.

Please note that unlike the CTA strategy, if an error vt_symbol is entered when creating an instance, the multi-contract combination strategy module will report an error during initialization, not when creating a strategy instance, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/7.png)

### Start

After the successful initialization of the strategy instance, when the [inited] status is [True], the automatic trading function of the strategy instance can be started. Click the [Start] button under the strategy instance, and the strategy instance can be started. If successful, it will be as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/10.png)

At this time, it can be observed that the [inited] and [trading] statuses of this strategy instance are both [True]. This indicates that the strategy instance has completed historical data playback and that the trading request class functions (buy/sell/short/cover/cancel_order, etc.) and information output class functions (send_email/put_event, etc.) inside the strategy will only be executed and send the corresponding request instructions to the underlying interface (actually execute the transaction) at this time.

During the initialization process of the strategy in the previous step, although the strategy is also receiving (historical) data and calling the corresponding functional functions, because the [trading] status is [False], there will be no real order placing operation or trading-related log information output.

If the strategy sends an order after starting, you can check the order details in the [Order] column of the main interface of VeighNa Trader, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/9.png)

Please note that unlike the CTA strategy module, the multi-contract combination strategy **does not provide local stop order function**, so there will be no stop order display area on the UI interface.

### Stop

If you want to stop, edit, or remove a strategy instance due to certain circumstances (such as the market closing time, or an emergency situation during the trading session), you can click the [Stop] button under the strategy instance to stop the automatic trading of this strategy instance. If successful, it will be as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/11.png)

The portfolio strategy engine will automatically cancel all active orders issued by the strategy before stopping the strategy to ensure that there are no uncontrolled orders after the strategy stops. At the same time, the latest variable information of this strategy instance will be saved to the portfolio_strategy_data.json file under the .vntrader folder.

At this time, it can be observed that the [trading] status of this strategy instance has been changed to [False], indicating that the automatic trading of this strategy instance has been stopped.

In the real trading process of the multi-contract combination strategy, the strategy should be run automatically throughout the entire trading session, and there should be as few additional pause and restart operations as possible. For the domestic futures market, the strategy should be started for automatic trading before the trading session starts, and then closed until the end of the trading session. Because the CTP night trading system will also be closed after the night trading session, and restarted before the morning trading session, the strategy needs to be stopped after the night trading session is closed and VeighNa Trader is closed.

### Edit

If you want to edit the parameters of a strategy instance after creating the strategy instance (if the strategy has been started, you need to click the [Stop] button under the strategy instance to stop the strategy first), you can click the [Edit] button under the strategy instance, and a parameter editing dialog box will pop up for you to modify the strategy parameters. As shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/12.png)

After editing the strategy parameters, click the [OK] button at the bottom, and the corresponding modifications will be immediately updated in the parameter table.

However, the trading contract code of the strategy instance cannot be modified, and the initialization operation will not be re-executed after the modification. Also, please note that at this time, only the parameter values of the strategy instance under the portfolio_strategy_setting.json file in the .vntrader folder have been modified, and the parameters under the original strategy file have not been modified.

Before the modification, the json file is as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/18.png)


After the modification, the json file is as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/17.png)

If you want to start the strategy again after editing during the trading session, you can click the [Start] button under the strategy instance to start the strategy instance again.

### Remove

If you want to remove a strategy instance after creating the strategy instance (if the strategy has been started, you need to click the [Stop] button under the strategy instance to stop the strategy first), you can click the [Remove] button under the strategy instance. After the removal is successful, the information of this strategy instance will no longer be displayed in the left strategy monitoring component of the graphical interface. As shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/13.png)

The configuration information of this strategy instance has also been removed from the portfolio_strategy_setting.json file under the .vntrader folder.

### Status Tracking

If you want to track the status of the strategy through the graphical interface, there are two ways:

1. Call the put_event function

   All variable information in the strategy instance needs to have the variable name written in the strategy's variables list in order to be displayed in the graphical interface. If you want to track the change of the variable state, you need to call the put_event function in the strategy, and the interface will refresh the data.

   Sometimes users may find that no matter how long their strategy runs, the variable information does not change. In this case, please check whether the put_event function is missing in the strategy.

2. Call the write_log function

   If you not only want to observe the change of the variable information, but also want to output personalized logs based on the status of the strategy, you can call the write_log function in the strategy to output logs.

## Running Log

### Log Content

There are two sources of logs output on the UI interface of the multi-contract combination strategy module, which are the strategy engine and the strategy instance.

**Engine Log**

The strategy engine generally outputs global information. In the figure below, except for the content after the strategy instance name followed by a colon, all are logs output by the strategy engine.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/15.png)

**Strategy Log**

If the write_log function is called in the strategy, the log content will be output through the strategy log. The content in the red box in the figure below is the strategy log output by the strategy instance. The content before the colon is the name of the strategy instance, and the content after the colon is the content output by the write_log function.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/16.png)

### Clear Operation

If you want to clear the log output on the UI interface of the multi-contract combination strategy, you can click the [Clear Log] button in the upper right corner, and the log output on the interface can be cleared with one click.

After clicking [Clear Log], as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/14.png)

## Batch Operation

In the case where the strategy has been thoroughly tested, the live trading is relatively stable, and there is no need to make frequent adjustments, if there are multiple combination strategy instances that need to be run, you can use the [All Initialize], [All Start], and [All Stop] functions in the upper right corner of the interface to execute pre-market batch initialization of strategy instances, start strategy instances, and post-market batch stop of strategy instances.

### All Initialize

After all strategy instances have been successfully created, click the [All Initialize] button in the upper right corner, and you can batch initialize the strategy instances, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/19.png)

### All Start

After all strategy instances have been successfully initialized, click the [All Start] button in the upper right corner, and you can batch start the strategy instances, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/20.png)

### All Stop

After all strategy instances have been successfully started, click the [All Stop] button in the upper right corner, and you can batch stop the strategy instances, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_strategy/21.png)

## Multi-Contract Combination Strategy Template (StrategyTemplate) -- Basic

The multi-contract combination strategy template provides signal generation and order management functions. Users can develop multi-contract combination strategies based on this template (located in site-packages\vnpy_portfoliostrategy\template).

The strategy developed by the user can be placed in the [strategies](#jump) folder under the user's running folder.

Please note:

1. The naming of the strategy file is in underscore mode, such as portfolio_boll_channel_strategy.py, and the naming of the strategy class is in camel case, such as PortfolioBollChannelStrategy.

2. The class name of the self-built strategy should not conflict with the class name of the example strategy. If there is a conflict, only one strategy class name will be displayed on the graphical interface.

The specific steps of strategy development are shown through the example strategy PortfolioBollChannelStrategy strategy.

Before writing the strategy logic based on the strategy template, you need to import the internal components that need to be used at the top of the strategy file, as shown in the code below:

```python3
from typing import List, Dict
from datetime import datetime

from vnpy.trader.utility import ArrayManager, Interval
from vnpy.trader.object import TickData, BarData
from vnpy_portfoliostrategy import StrategyTemplate, StrategyEngine
from vnpy_portfoliostrategy.utility import PortfolioBarGenerator
```

Where, StrategyTemplate is the strategy template, StrategyEngine is the strategy engine, Interval is the data frequency, TickData and BarData are the data containers that store the corresponding information, PortfolioBarGenerator is the combination strategy K-line generation module, ArrayManager is the K-line time series management module.

### Strategy Parameters and Variables

Below the strategy class, you can set the strategy's author (author), parameters (parameters), and variables (variables), as shown in the code below:

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

Although the strategy's parameters and variables both belong to the strategy class, the strategy parameters are fixed (specified from the outside by the trader), while the strategy variables change with the state of the strategy during the trading process, so the strategy variables only need to be initialized as the corresponding basic types. For example: set the integer to 0, the float to 0.0, and the string to "".

If the strategy engine needs to display the strategy parameters and variables on the UI interface during the running process, and save their values when the data is refreshed or the strategy is stopped, the names of the parameters and variables (as strings) need to be added to the parameters and variables lists.

Please note that this list can only accept parameters or variables of four data types: str, int, float, and bool. If the strategy needs to use parameters and variables of other data types, please put the definition of the parameter or variable under the __init__ function.

### Class Initialization

Input: strategy_engine: StrategyEngine, strategy_name: str, vt_symbols: List[str], setting: dict

Output: None

The __init__ function is the constructor of the strategy class, which needs to be consistent with the inherited StrategyTemplate.

In this inherited strategy class, the initialization generally consists of four steps, as shown in the code below:

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

1. Inherit the strategy template through the super() method, and pass the strategy engine, strategy name, vt_symbols, and parameter settings (all of which are automatically passed by the strategy engine when creating a strategy instance, and the user does not need to set them).

2. Create the ArrayManager instance and the dictionary of strategy variables that are needed for different contract K-line time series management (ArrayManager) and strategy variables.

3. Create ArrayManager and target position variables for different contracts and put them into the dictionary.

The default length of ArrayManager is 100. If you need to adjust the length of ArrayManager, you can pass the size parameter to adjust it (size cannot be less than the length of the calculated indicator).

4. Call the combination strategy K-line generation module (PortfolioBarGenerator): synthesize Tick data into 1-minute K-line data through time slicing. If necessary, longer time period data can also be synthesized, such as 15-minute K-line.

If the strategy is only based on on_bar trading, the code here can be written as:

```python3
        self.pbg = PortfolioBarGenerator(self.on_bars)
```

And there is no need to pass the longer K-line period that needs to be synthesized based on on_bars, and the function name that receives the longer K-line period.

Please note:

 - When synthesizing X-minute line, X must be set to a number that can be divided by 60 (except 60). There is no such restriction for synthesizing hourly line.

 - The default data frequency for synthesizing long period K-line data based on on_bar function in PortfolioBarGenerator is minute level. If you need to trade based on synthesized hourly line or longer period K-line, please import Interval at the top of the strategy file and pass the corresponding data frequency to the bg instance.

 - The function name self.on_hour_bars has been used internally in the program. If you need to synthesize 1-hour K-line, please use self.on_1_hour_bars or other naming.

### Functions called by the strategy engine

The update_setting function in StrategyTemplate and the four functions starting with get and update, as well as the update_trade and update_order functions, are functions called by the strategy engine. They are generally not needed to be called when writing the strategy.

### Callback functions of the strategy

The functions starting with on in StrategyTemplate are called callback functions. They can be used to receive data or receive status updates during the writing of the strategy. Callback functions can be divided into the following two categories according to their functions:

#### Strategy instance status control (required for all strategies)

**on_init**

* Input: None

* Output: None

When the strategy is initialized, the on_init function will be called. The default writing is to call the write_log function to output the "Strategy Initialization" log, and then call the load_bars function to load historical data. As shown in the code below:

```python3
    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("Strategy Initialization")
        self.load_bars(10)
```

Unlike CTA strategy, the multi-contract combination strategy only supports K-line backtesting, so the multi-contract strategy template does not have the load_ticks function.

When the strategy is initialized, the inited and trading states of the strategy are both [False]. At this time, only the ArrayManager is called to calculate and cache the relevant calculation indicators, and no trading signals can be sent. After calling the on_init function, the inited state of the strategy becomes [True], and the strategy initialization is completed.

**on_start**

* Input: None

* Output: None

When the strategy is started, the on_start function will be called. The default writing is to call the write_log function to output the "Strategy Start" log, as shown in the code below:

```python3
    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("Strategy Start")
```

After calling the on_start function of the strategy to start the strategy, the trading state of the strategy becomes [True], and the strategy can send trading signals.

**on_stop**

* Input: None

* Output: None

When the strategy is stopped, the on_stop function will be called. The default writing is to call the write_log function to output the "Strategy Stop" log, as shown in the code below:

```python3
    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("Strategy Stop")
```

After calling the on_stop function of the strategy to stop the strategy, the trading state of the strategy becomes [False], and the strategy will no longer send trading signals.

#### Receive data, calculate indicators, and send trading signals

**on_tick**

* Input: tick: TickData

* Output: None

Most trading systems only provide Tick data push. Even if some platforms can provide K-line data push, the speed of these data reaching the local computer is slower than the push of Tick data, because it also needs to be synthesized by the platform before it can be pushed over. Therefore, in live trading, all the strategies in VeighNa are based on K-line data synthesized from received Tick data.

When the strategy receives the latest market push of Tick data in live trading, the on_tick function will be called. The default writing is to push the received Tick data into the pbg instance created earlier through the update_tick function of the PortfolioBarGenerator, so that 1-minute K-line data can be synthesized, as shown in the code below:

```python3
    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.pbg.update_tick(tick)
```

Please note that the on_tick function is only called in live trading, and backtesting does not support it.

**on_bars**

* Input: bars: Dict[str, BarData]

* Output: None

When the strategy receives the latest K-line data (in live trading, the default is to push 1-minute K-line data synthesized from Tick data, and in backtesting, it depends on the K-line data frequency parameter filled in when selecting the parameter), the on_bars function will be called.

Unlike the CTA strategy module, the multi-contract combination strategy module receives K-line push through the on_bars callback function, and all the K-line data of all contracts at this time point are received at once, rather than one by one through the on_bar function (cannot judge whether the K-line at the current time point has all been completed). 

There are two ways of writing in the example strategy:

1. If the strategy is based on on_bars to push K-line trading, then please write all the trading request class functions under the on_bars function (because the example strategy class PortfolioBollChannelStrategy is not based on on_bars trading, it is not explained in the example. The example code of the strategy based on on_bars trading can be found in the example strategy).

2. If the strategy needs to use the K-line data pushed by on_bars to synthesize longer time period K-line data through the PortfolioBarGenerator for trading, then please call the update_bars function of the PortfolioBarGenerator to push the received bars into the pbg instance created earlier, as shown in the code below:

```python3
    def on_bars(self, bars: Dict[str, BarData]):
        """
        Callback of new bars data update.
        """
        self.pbg.update_bars(bars)
```

The example strategy class PortfolioBollChannelStrategy generates signals through 2-hour K-line data. There are three parts in total, as shown in the code below:

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

- Clear Unfilled Orders: To prevent orders placed earlier from not being executed in the last 2 hours, but the price may have been adjusted in the next 2 hours, use the cancel_all() method to immediately cancel all unfilled orders placed earlier, ensuring that the strategy is clear and unique at the beginning of the current 2 hours;

- Call K-line Time Series Management Module: Calculate the corresponding technical indicators, such as Bollinger Bands, CCI Index, ATR Index, etc., based on the latest 2-hour K-line data. First, get the ArrayManager object, then push the received K-line into it, check the initialization status of ArrayManager, if it has not been initialized successfully, return directly, there is no need to go through the subsequent trading-related logical judgment. Because many technical indicator calculations have requirements for the minimum number of K-lines, if the quantity is not enough, the calculated indicators will be incorrect or meaningless. On the contrary, if there is no return, you can start calculating technical indicators;

- Signal Calculation: Hang out **limit order** (buy/sell) based on the judgment of the position and combined with the CCI Index, ATR Index at the channel breakthrough point, and set the exit point (short/cover).

    Please note:
    1. In the CTA strategy module, it is usually through accessing the strategy variable pos to get the strategy position judgment. However, in the multi-contract combination strategy module, it is through calling the get_pos function to get the current position of a certain contract for logical judgment, then set the target position of the contract, and finally use the difference between the target position and the actual position for logical judgment to send out the trading signal;

    2. If you need to refresh the indicator values in the graphical interface, please do not forget to call the put_event() function.

#### Order Status Update

Because the multi-contract combination strategy needs to place orders for multiple contracts at the same time, it is impossible to judge the order execution order of each contract within a certain K-line segment during backtesting, so it is impossible to provide the on_order and on_trade functions to obtain the order execution push, and can only be queried through get_pos and get_order in each on_bars callback.

### Active Functions

**buy**: Buy to open (Direction: LONG, Offset: OPEN)

**sell**: Sell to close (Direction: SHORT, Offset: CLOSE)

**short**: Sell to open (Direction: SHORT, Offset: OPEN)

**cover**: Buy to close (Direction: LONG, Offset: CLOSE)

* Input: vt_symbol: str, price: float, volume: float, lock: bool = False, net: bool = False

* Output: vt_orderids: List[str] / None

buy/sell/short/cover are all trading request class functions responsible for placing orders within the strategy. The strategy can send trading signals to the strategy engine through these functions to achieve the purpose of placing orders.

The following is an example of the buy function. As you can see, the **specific code of the contract to be traded**, the price and volume are required parameters, and the lock and net conversion are set to False by default. You can also see that after receiving the parameters passed in, the function calls the send_order function in StrategyTemplate to place an order (because it is a buy command, the direction is automatically filled in as LONG, and the offset is filled in as OPEN).

Unlike the CTA strategy module, the multi-contract combination strategy module does not provide local stop order function, so the stop parameter is removed from the order function.

If lock is set to True, then the order will be converted to a lock order (in the case of today's position, if you want to close the position, all yesterday's position will be closed first, and then the remaining part will be converted to reverse opening to replace the closing today's position, in order to avoid the penalty of today's position fee).

If net is set to True, then the order will be converted to a net order (based on the overall account's total position, the direction of the strategy's order will be converted according to the net position holding method). However, the net trading mode is mutually exclusive with the lock trading mode, so when net is set to True, lock must be set to False.

Please note that if a closing order is sent to the Shanghai Futures Exchange, because the exchange must specify today's or yesterday's closing, the bottom layer will automatically convert its closing order. Because some varieties on the Shanghai Futures Exchange have today's closing preference, it is default to send the order in today's closing preference manner (if the target of the transaction is more favorable in yesterday's closing of the Shanghai Futures Exchange, you can make appropriate modifications in the convert_order_request_shfe function in vnpy.trader.converter).

```python3
    def buy(self, vt_symbol: str, price: float, volume: float, lock: bool = False, net: bool = False) -> List[str]:
        """
        Send buy order to open a long position.
        """
        return self.send_order(vt_symbol, Direction.LONG, Offset.OPEN, price, volume, lock, net)
```

Please note that domestic futures have the concept of opening and closing positions, for example, the buy operation needs to be distinguished as buy to open and buy to close; but for stocks and foreign futures, it is a net position mode, without the concept of opening and closing, so only the buy (buy) and sell (sell) commands are needed.

**send_order**

* Input: vt_symbol: str, direction: Direction, offset: Offset, price: float, volume: float, lock: bool = False, net: bool = False

* Output: vt_orderids: List[str] / None

The send_order function is the function used by the strategy engine to send orders. Generally, it is not necessary to call it separately when writing the strategy. You can send a limit order by using the buy/sell/short/cover functions.

In real trading, after receiving the parameters, the round_to function will be called to process the order price and quantity based on the contract's pricetick and min_volume.

Please note that the send_order function can only be called after the strategy is started, that is, after the trading status of the strategy becomes [True]. If the function is called when the trading status of the strategy is [False], it will only return [].

**cancel_order**

* Input: vt_orderid: str

* Output: None

**cancel_all**

* Input: None

* Output: None

The cancel_order and cancel_all functions are trading request class functions responsible for canceling orders. cancel_order cancels the specified active order within the strategy, and cancel_all cancels all active orders within the strategy.

Please note that the order can only be canceled after the strategy is started, that is, after the trading status of the strategy becomes [True].

### Functional Functions

The following are functional functions outside the strategy:

**get_pos**

* Input: vt_symbol: str

* Output: int / 0

When the get_pos function is called in the strategy, the specific contract's position data can be obtained.

**get_order**

* Input: vt_orderid

* Output: OrderData / None

When the get_order function is called in the strategy, the specific contract's order data can be obtained.

**get_all_active_orderids**

* Input: None

* Output: List[OrderData] / None

When the get_all_active_orderids function is called in the strategy, all current active order numbers can be obtained.

**get_pricetick**

* Input: vt_symbol

* Output: pricetick: float / None

When the get_price function is called in the strategy, the minimum price movement of a specific contract can be obtained.

**write_log**

* Input: msg: str

* Output: None

When the write_log function is called in the strategy, the specified content can be logged.

**load_bars**

* Input: days: int, interval: Interval = Interval.MINUTE

* Output: None

When the load_bars function is called in the strategy, K-line data can be loaded during the initialization of the strategy.

As shown in the following code, when the load_bars function is called, the default number of days to load is 10, and the frequency is one minute, which corresponds to loading 10 days of one-minute K-line data. In backtesting, 10 days refers to 10 trading days, while in real trading, 10 days refers to natural days, so it is recommended to load more days rather than too few. When loading, it will first try to obtain historical data through the trading interface, data service, and database in turn, until historical data is obtained or returned empty.

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

When the put_event function is called in the strategy, the graphical interface can be notified to refresh the display related to the strategy status.

Please note that the interface can only be refreshed after the strategy is initialized, that is, after the inited status of the strategy becomes [True].

**send_email**

* Input: msg: str

* Output: None

After configuring the email-related information (the configuration method is detailed in the global configuration part of the basic usage section), the send_email function can be called in the strategy to send an email with the specified content to your email.

Please note that the email can only be sent after the strategy is initialized, that is, after the inited status of the strategy becomes [True].

**sync_data**

* Input: None

* Output: None

When the sync_data function is called in the strategy, the strategy variables are synchronized into the json file for local caching every time the strategy stops or is executed in real trading, making it easy to read and restore when initializing the next day (the strategy engine will call it, no need to call it actively in the strategy).

Please note that the strategy information can only be synchronized after the strategy is started, that is, after the trading status of the strategy becomes [True].

## Advanced Multi-Contract Combination Strategy Template (StrategyTemplate)

The PortfolioStrategy module is aimed at quantitative strategies of multi-underlying investment portfolios. This type of strategy pursues the adjustment of the position of the strategy investment portfolio to the target state at the execution level, rather than paying too much attention to the underlying order trading details.

First, introduce the functional functions of the position target rebalancing trading, to show the support of the position target rebalancing trading:

### Introduction to the Functional Functions of Position Target Rebalancing Trading

The following are the functional functions called by the strategy in the position target rebalancing trading mode:

**set_target**

* Input: vt_symbol: str, target: int

* Output: None

When the set_target function is called in the strategy, the target position of a specific contract can be set.

Please note: The target position is a persistent state, so after it is set, it will be maintained in the subsequent time until it is set and modified again.

**get_target**

* Input: vt_symbol: str

* Output: int

When the get_target function is called in the strategy, the target position of a specific contract can be obtained.

Please note: The target position state of the strategy will be automatically persisted to the hard disk file during the sync_data operation (execution, stop, etc.), and will be restored after the strategy is restarted.

**rebalance_portfolio**

* Input: bars: Dict[str, BarData]

* Output: None

When the rebalance_portfolio function is called in the strategy, the rebalancing trading can be executed based on the target position of a specific contract.

Please note: Only the contracts with K-line slices in the current bars dictionary will participate in the execution of this rebalancing trading, so as to ensure that contracts without market data push during non-trading hours (no market data push) will not mistakenly place orders.

**calculate_price**

* Input: vt_symbol: str, direction: Direction, reference: float

* Output: pricetick: float

When the rebalance_portfolio function detects a difference between the target position and the actual position, the calculate_price function will be called to calculate the price of the rebalancing order.

The default writing in the strategy is to calculate the order price based on the price_add set for the order direction, and you can also refer to the example strategy PairTradingStrategy to calculate the order price based on the tick_add set for the order direction.

```python3
    def calculate_price(self, vt_symbol: str, direction: Direction, reference: float) -> float:
        """Calculate the price of the rebalancing order (support on-demand reloading)"""
        if direction == Direction.LONG:
            price: float = reference + self.price_add
        else:
            price: float = reference - self.price_add

        return price
```

### Example of Using Functional Functions of Position Target Rebalancing Trading

The biggest difference between the functional functions of position target rebalancing trading and the basic usage of StrategyTemplate is in the processing difference in the on_bars function of the strategy. The specific steps of the position target rebalancing trading are shown below through the example strategy class TrendFollowingStrategy:

**on_bars**

* Input: bars: Dict[str, BarData]

* Output: None

When the strategy receives the latest K-line data (by default, the one-minute K-line synthesized based on the Tick is pushed in during real trading, and it depends on the K-line data frequency parameter filled in during backtesting), the on_bars function will be called.

The example strategy class TrendFollowingStrategy generates signals based on the return of one-minute K-line data. There are three parts in total, as shown in the following code:

```python3
    def on_bars(self, bars: Dict[str, BarData]) -> None:
        """K-line slice callback"""
        # Update K-line to calculate RSI value
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

- Call K-line Time Series Management Module: Calculate the corresponding technical indicators, such as ATR Index, RSI Index, etc., based on the latest one-minute K-line data. First, get the ArrayManager object, then push the received K-line into it, check the initialization status of ArrayManager, if it has not been initialized successfully, return directly, there is no need to go through the subsequent trading-related logical judgment. Because many technical indicator calculations have requirements for the minimum number of K-lines, if the quantity is not enough, the calculated indicators will be incorrect or meaningless. On the contrary, if there is no return, you can start calculating technical indicators;

- Signal Calculation: Set the target position based on the judgment of the position (get_pos) and the calculation result of the indicator at the channel breakthrough point.

- Execute rebalancing trading (rebalance_portfolio)

**calculate_price**

* Input: vt_symbol: str, direction: Direction, reference: float

* Output: pricetick: float

When the rebalance_portfolio function detects a difference between the target position and the actual position, the calculate_price function will be called to calculate the price of the rebalancing order.

The default writing in the strategy is to calculate the order price based on the price_add set for the order direction, and you can also refer to the example strategy PairTradingStrategy to calculate the order price based on the tick_add set for the order direction.
