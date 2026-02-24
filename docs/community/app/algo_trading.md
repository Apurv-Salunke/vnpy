# AlgoTrading - Algorithmic Order Execution Trading Module

## Function Overview

AlgoTrading is a module for **algorithmic order execution trading**. Users can conveniently complete tasks such as launching algorithms, saving configurations, and stopping algorithms through its UI interface.

Algorithmic trading is responsible for the specific execution process of order placements. Currently, AlgoTrading provides various example algorithms. Users can automatically split large orders into appropriate smaller orders for phased placement, effectively reducing trading costs and impact costs (such as Iceberg algorithm, Sniper algorithm). They can also conduct buy-low-sell-high operations within set thresholds (such as Grid algorithm, Arbitrage algorithm).

## Loading and Launching

### Loading via VeighNa Station

After launching and logging into VeighNa Station, click the [Trading] button. In the configuration dialog, check [AlgoTrading] in the [Application Module] section.

### Loading via Script

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_algotrading import AlgoTradingApp

# Write after creating the main_engine object
main_engine.add_app(AlgoTradingApp)
```

## Starting the Module

For user-built algorithms, they need to be placed in the algo_trading.algos directory to be recognized and loaded.

Before starting the module, please connect to the trading interface first (for connection methods, see the Interface Connection section in the Basic Usage chapter). After seeing "Contract information query successful" output in the [Log] section of the VeighNa Trader main interface, start the module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/1.png)

Please note that because the IB interface cannot automatically obtain all contract information upon login, it can only be obtained when the user manually subscribes to market data. Therefore, you need to manually subscribe to contract market data on the main interface before starting the module.

After successfully connecting to the trading interface, click [Function] -> [Algorithmic Trading] in the menu bar, or click the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/1.png)

You can then enter the UI interface of the algorithmic order execution trading module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/10.png)


## Configuring Algorithms

Algorithm configuration parameter requirements are as follows:

- Algorithm: Select the trading algorithm to execute from the dropdown box;
- Local Code: Format is vt_symbol (contract code + exchange name);
- Direction: Long, Short;
- Price: Order placement price;
- Quantity: Total order quantity, which needs to be split into smaller orders for trading;
- Execution Time (seconds): Total time to run the algorithmic trading, in seconds;
- Interval (seconds): How often to place orders, in seconds;
- Open/Close: Open, Close, Close Today, Close Yesterday.


## Launching Algorithms

Currently, VeighNa provides five commonly used example algorithms. This document uses the Time-Weighted Average Price (TWAP) algorithm as an example to introduce the algorithm launching process.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/3.png)

After configuring the parameters (for saved algorithm information, click [Use] under the corresponding algorithm in the [Configuration] section to switch the information content on the left side of the interface), click the [Start Algorithm] button to immediately execute algorithmic trading.

If launched successfully, you can observe the algorithm's execution status in the [Executing] interface in the upper right corner.

The specific task executed by the algorithm in the figure is: Use the Time-Weighted Average Price algorithm to buy 10,000 lots of Soybean Meal 2409 contract (y2409), execution price is 7420 yuan, execution time is 600 seconds, interval is 6 seconds; that is, every 6 seconds, when the contract's ask price is less than or equal to 7420, buy 100 lots of Soybean Meal 2409 contract at 7420, dividing the buy operation into 100 times.

## CSV Launch

When there are many algorithms to launch, you can batch launch them at once through a CSV file. Click the [CSV Launch] button on the left side of the GUI, find the CSV file to import in the pop-up dialog, and open it to quickly launch the algorithms.

Please note that the CSV file format should be as shown in the figure below, consistent with the fields in the left editing area:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/12.png)

Combined with Excel's quick table editing features, batch adding algorithms is more convenient. After successful launch, the execution status of all algorithms in the CSV file will be displayed in the [Executing] interface.


## Stopping Algorithms

When users need to pause a trading algorithm that is currently executing, they can click the [Pause] button in the [Executing] interface to pause a certain executing algorithmic trading, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/6.png)

When users need to resume a paused trading algorithm, they can click the [Resume] button in the [Executing] interface to resume a certain paused algorithmic trading, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/15.png)

When users need to stop a trading algorithm that is currently executing, they can click the [Stop] button in the [Executing] interface to stop a certain executing algorithmic trading, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/6.png)

Users can also click the [Stop All] button at the bottom of the order trading interface to stop all executing algorithmic trading with one click, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/7.png)


## Data Monitoring

The data monitoring interface consists of four parts:

Executing Component: Displays algorithmic trading that is currently executing, including: algorithm, parameters, variables, and status. After successfully launching the algorithm, switch to the [Executing] interface in the upper right corner to display the algorithm's execution status, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/6.png)

Finished Component: Displays completed algorithmic trading, also including: algorithm, parameters, variables, and status. After the algorithm ends or stops, switch to the [Finished] interface in the upper right corner to display the algorithm's execution status, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/9.png)

Log Component: Displays relevant log information for launching, stopping, and completing algorithms. After opening the algorithmic trading module, initialization is performed, so the [Log] component will first output "Algorithmic trading engine started", as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/11.png)


## Example Algorithms

Example algorithm paths are located in the vnpy_algotrading.algos folder (please note that some algorithms do not have open/close direction written. If needed, you can make personalized modifications based on your own requirements). Currently, the algorithmic trading module provides the following five built-in algorithms:

### TWAP - Time-Weighted Average Price Algorithm

The Time-Weighted Average Price (TWAP) algorithm execution steps are as follows:

- Distribute the order quantity evenly over a certain time period, placing buy (or sell) orders at specified prices at regular intervals.

- Buy situation: When the ask price is lower than the target price, send an order. The order quantity is the minimum of the remaining order quantity and the order split quantity.

- Sell situation: When the bid price is higher than the target price, send an order. The order quantity is the minimum of the remaining order quantity and the order split quantity.

### Iceberg - Iceberg Algorithm

The Iceberg algorithm execution steps are as follows:

- Place an order at a certain price level, but only for a portion, until all are filled.

- Buy situation: First check for order cancellation. If the latest Tick ask price is lower than the target price, execute cancellation. If there is no active order, send an order. The order quantity is the minimum of the remaining order quantity and the displayed order quantity.

- Sell situation: First check for order cancellation. If the latest Tick bid price is higher than the target price, execute cancellation. If there is no active order, send an order. The order quantity is the minimum of the remaining order quantity and the displayed order quantity.

### Sniper - Sniper Algorithm

The Sniper algorithm execution steps are as follows:

- Monitor the latest Tick market data push, and immediately quote when good prices are discovered.

- Buy situation: When the latest Tick ask price is lower than the target price, send an order. The order quantity is the minimum of the remaining order quantity and the ask quantity.

- Sell situation: When the latest Tick bid price is higher than the target price, send an order. The order quantity is the minimum of the remaining order quantity and the bid quantity.

### Stop - Conditional Order Algorithm

The Conditional Order (Stop) algorithm execution steps are as follows:

- Monitor the latest Tick market data push, and immediately quote when a price breakout is discovered.

- Buy situation: When the Tick latest price is higher than the target price, send an order. The order price is the target price plus the price improvement.

- Sell situation: When the Tick latest price is lower than the target price, send an order. The order price is the target price minus the price improvement.

### BestLimit - Best Limit Algorithm

The Best Limit algorithm execution steps are as follows:

- Monitor the latest Tick market data push, and immediately quote when good prices are discovered.

- Buy situation: First check for order cancellation: When the latest Tick bid price is not equal to the target price, execute cancellation. If there is no active order, send an order. The order price is the latest Tick bid price, and the order quantity is the remaining order quantity.

- Sell situation: First check for order cancellation: When the latest Tick ask price is not equal to the target price, execute cancellation. If there is no active order, send an order. The order price is the latest Tick ask price, and the order quantity is the remaining order quantity.
