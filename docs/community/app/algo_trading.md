# AlgoTrading - Algorithmic Order Execution Trading Module

## Function Introduction

AlgoTrading is a module for **algorithmic order execution trading**. Users can use its UI interface to easily complete tasks such as starting algorithms, saving configurations, and stopping algorithms.

The algorithmic trading is responsible for the specific execution process of the delegated orders. Currently, AlgoTrading provides a variety of example algorithms. Users can effectively reduce trading costs and impact costs (such as Iceberg algorithm, Sniper algorithm) by automatically splitting large orders into appropriate small orders for batch delegation. They can also operate high and low within the set threshold (such as Grid algorithm, Arbitrage algorithm).

## Loading and Starting

### VeighNa Station Loading

After starting and logging into VeighNa Station, click the 【Trading】 button, and check the 【AlgoTrading】 in the 【Application Module】 column in the configuration dialog.

### Script Loading

Add the following code to the startup script:

```python3
# At the top
from vnpy_algotrading import AlgoTradingApp

# After creating the main_engine object
main_engine.add_app(AlgoTradingApp)
```

## Starting the Module

For algorithms built by users, they need to be placed in the algo_trading.algos directory to be recognized and loaded.

Before starting the module, please connect to the trading interface first (the connection method is detailed in the basic usage section of the connection interface). After seeing the "Contract information query successful" output in the 【Log】 column of the VeighNa Trader main interface, start the module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/1.png)

Please note that because the IB interface cannot automatically obtain all contract information when logging in, it can only be obtained when the user manually subscribes to market data on the main interface. Therefore, you need to manually subscribe to the contract market data on the main interface before starting the module.

After successfully connecting to the trading interface, click on the 【Function】-> 【Algorithmic Trading】 in the menu bar, or click on the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/1.png)

You can enter the UI interface of the algorithmic order execution trading module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/10.png)


## Configuring the Algorithm

The configuration parameters are as follows:

- Algorithm: Select the trading algorithm to be executed in the drop-down box;
- Local code: The format is vt_symbol (contract code + exchange name);
- Direction: Long, short;
- Price: The price at which the order is placed;
- Quantity: The total quantity of the order, which needs to be split into small batch orders for trading;
- Execution time (seconds): The total time for running the algorithmic trading, in seconds;
- Interval per round (seconds): The time interval for placing order operations, in seconds;
- Open/close: Open, close, close today, close yesterday.


## Starting the Algorithm

Currently, VeighNa provides a total of five commonly used example algorithms. This document takes the Time Weighted Average Price algorithm (TWAP) as an example to introduce the algorithm startup process.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/3.png)

After the parameter configuration is completed (the saved algorithm information, you can switch the content of the left side of the interface to the configured algorithm by clicking 【Use】 under the corresponding algorithm in the 【Configuration】 column), click the 【Start Algorithm】 button to immediately execute the algorithmic trading.

If the startup is successful, you can observe the execution status of the algorithm in the upper right corner of the 【Executing】 interface.

The specific task of the algorithm execution in the figure is: using the Time Weighted Average Price algorithm, buy 10,000 lots of soybean oil 2109 contract (y2409), the execution price is 7420 yuan, the execution time is 600 seconds, the interval per round is 6 seconds; that is, every 6 seconds, when the contract selling price is less than or equal to 7420, buy 100 lots of soybean oil 2409 contract at the price of 7420, and split the buy operation into 100 times.

## CSV Startup

When there are many algorithms that need to be started, you can use a CSV file to start them in batches. Click the 【CSV Startup】 button on the left side of the graphical interface, and open the CSV file to be imported in the pop-up dialog box to quickly start the algorithms.

Please note that the format of the CSV file should be consistent with the fields in the left editing area, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/12.png)

With the quick editing function of Excel, it is more convenient to add algorithms in batches. After the startup is successful, the execution status of all algorithms in the CSV file will be displayed in the 【Executing】 interface.


## Stopping the Algorithm

When the user needs to pause the execution of a trading algorithm, they can click the 【Pause】 button in the 【Executing】 interface to pause a trading algorithm that is currently executing, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/6.png)

When the user needs to resume a trading algorithm that has been paused, they can click the 【Resume】 button in the 【Executing】 interface to resume a trading algorithm that has been paused, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/15.png)

When the user needs to stop a trading algorithm that is currently executing, they can click the 【Stop】 button in the 【Executing】 interface to stop a trading algorithm that is currently executing, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/6.png)

The user can also click the 【Stop All】 button at the bottom of the order trading interface to stop all executing trading algorithms with one click, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/7.png)


## Data Monitoring

The data monitoring interface is composed of four parts:

Executing component: Displaying the executing trading algorithms, including: algorithm, parameters, variables, and status. After successfully starting the algorithm, switch to the upper right corner 【Executing】 interface, and the execution status of the algorithm will be displayed, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/6.png)

Completed component: Displaying the completed trading algorithms, also including: algorithm, parameters, variables, and status. After the algorithm is completed or stopped, switch to the upper right corner 【Completed】 interface, and the execution status of the algorithm will be displayed, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/9.png)

Log component: Displaying the relevant log information of starting, stopping, and completing the algorithm. After opening the algorithmic trading module, it will be initialized, so the 【Log】 component will first output "Algorithmic trading engine started", as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/algo_trading/11.png)


## Example Algorithms

The example algorithm path is located in the vnpy_algotrading.algos folder (please note that some algorithms do not have the open/close direction written, if necessary, you can make personalized modifications based on your own needs). Currently, the algorithmic trading module provides the following five built-in algorithms:

### TWAP - Time Weighted Average Price Algorithm

The specific execution steps of the Time Weighted Average Price algorithm (TWAP) are as follows:

- Distribute the order quantity evenly in a certain time period, and place a buy order (or sell order) at a specified price every time.

- Buy situation: When the selling price is lower than the target price, place an order. The order quantity is the minimum of the remaining order quantity and the order split quantity.

- Sell situation: When the selling price is higher than the target price, place an order. The order quantity is the minimum of the remaining order quantity and the order split quantity.

### Iceberg - Iceberg Algorithm

The specific execution steps of the Iceberg algorithm are as follows:

- Place an order at a certain price, but only place a part of it, until all are executed.

- Buy situation: First check the cancellation, if the latest Tick selling price is lower than the target price, execute the cancellation; if there is no active order, place an order. The order quantity is the minimum of the remaining order quantity and the order placed quantity.

- Sell situation: First check the cancellation, if the latest Tick buying price is higher than the target price, execute the cancellation; if there is no active order, place an order. The order quantity is the minimum of the remaining order quantity and the order placed quantity.

### Sniper - Sniper Algorithm

The specific execution steps of the Sniper algorithm are as follows:

- Monitor the market data pushed by the latest Tick, and immediately quote and execute when good prices are found.

- Buy situation: When the latest Tick selling price is lower than the target price, place an order. The order quantity is the minimum of the remaining order quantity and the selling quantity.

- Sell situation: When the latest Tick buying price is higher than the target price, place an order. The order quantity is the minimum of the remaining order quantity and the buying quantity.

### Stop - Conditional Order Algorithm

The specific execution steps of the Stop algorithm are as follows:

- Monitor the market data pushed by the latest Tick, and immediately quote and execute when the market data breaks through.

- Buy situation: When the latest Tick price is higher than the target price, place an order. The order price is the target price plus the premium.

- Sell situation: When the latest Tick price is lower than the target price, place an order. The order price is the target price minus the premium.

### BestLimit - Best Limit Price Algorithm

The specific execution steps of the Best Limit Price algorithm are as follows:

- Monitor the market data pushed by the latest Tick, and immediately quote and execute when good prices are found.

- Buy situation: First check the cancellation: if the latest Tick buying price is not equal to the target price, execute the cancellation; if there is no active order, place an order. The order price is the latest Tick buying price, and the order quantity is the remaining order quantity.

- Sell situation: First check the cancellation: if the latest Tick buying price is not equal to the target price, execute the cancellation; if there is no active order, place an order. The order price is the latest Tick selling price, and the order quantity is the remaining order quantity.
