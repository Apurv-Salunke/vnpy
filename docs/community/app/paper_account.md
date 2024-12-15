# PaperAccount - Local Simulation Trading Module


## Function Introduction

PaperAccount is a functional module used for **local simulation trading**. Users can use its UI interface to simulate trading based on real-time market data.

## Loading and Startup

### VeighNa Station Loading

After logging into VeighNa Station, click the 【Trading】 button, and in the configuration dialog, check the 【PaperAccount】 in the 【Application Module】 column.

### Script Loading

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_paperaccount import PaperAccountApp

# Write after creating the main_engine object
main_engine.add_app(PaperAccountApp)
```


## Module Startup

Before starting the module, please connect to the interface for simulated trading (connection method detailed in the basic usage section of the connection interface). After seeing the "Contract information query successful" output in the VeighNa Trader main interface 【Log】 column, start the module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/1.png)

Please note that the IB interface cannot automatically obtain all contract information when logging in, and can only obtain it when the user manually subscribes to market data. Therefore, you need to manually subscribe to market data on the main interface first, and then start the module.

After the trading interface is connected, the local simulation trading module will start automatically. At this time, all contract trading orders and cancellation requests are **handled by the local simulation trading module**, and will not be sent to the real server.

## Function Configuration

Click on the menu bar 【Function】-> 【Simulation Trading】, or click on the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/paper_account/4.png)

You can enter the UI interface of the local simulation trading module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/paper_account/5.png)

Users can configure the following functions through the UI interface:

- Slippage for market orders and stop orders
  - Used to affect the **slippage number** of the transaction price relative to the market price when the market order and stop order are executed;

- Calculation frequency of simulated trading position profit and loss
  - How many seconds to execute the position profit and loss calculation update. If the program is found to be stuck when there are many positions, it is recommended to try to reduce the frequency;

- Use the current market order immediately after placing an order
  - By default, the order placed by the user needs to **wait until the next TICK market order push to be matched** (simulated real market scenario). For inactive contracts with low TICK push frequency, you can check this option, and the order will be **immediately matched based on the current latest TICK market order** after placing the order;

- Clear all positions after placing an order
  - One-click to clear all local position data.

The local simulation trading module can also be used together with other strategy application modules (such as CtaStrategy module, SpreadTrading module, etc.) to achieve localized quantitative strategy simulation trading test.


## Data Monitoring

Users can use the 【Query Contract】 to confirm the trading interface status of the contract:

Click on the menu bar 【Help】->【Contract Query】, and in the pop-up dialog, click the 【Query】 button directly in the upper right corner. It is found that the 【Trading Interface】 column of all contracts is displayed as PAPER, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/paper_account/2.png)

Before placing an order and canceling an order for a certain contract, the user must first **subscribe** to the market data of this contract.

In the following figure, the information displayed in the three monitoring components of 【Order】, 【Trade】, and 【Position】 is all PAPER (local simulation data):

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/paper_account/3.png)

Please note that the local simulation trading module **does not provide capital calculation function**, so the 【Capital】 component displays the capital of the real account, and will not change due to the orders generated in the local simulation trading module.


## Business Logic

The business logic of the local simulation trading module is as follows:

- Supported order types (unsupported types will be rejected):

  - Limit order;
  - Market order;
  - Stop order;

- The order matching rule adopts the **price-to-price transaction** mode. Taking the buy order as an example:

  - Limit order: When the ask_price_1 of the market order is less than or equal to the order price, the order is executed;
  - Stop order: When the ask_price_1 of the market order is greater than or equal to the order price, the order is executed;

- When the order is executed, the **pending order quantity on the market order is not considered**, and all are executed at once;

- After the order is executed, the module will automatically record the corresponding position information PositionData:

  - According to the position mode of the contract itself (long position vs net position), maintain the corresponding position information;
  - **For opening transactions, use weighted average to calculate and update the position cost price;**
  - **For closing transactions, the position cost price remains unchanged;**
  - After placing a pending order in the long and short position mode, the corresponding position quantity will be frozen. If the available quantity is insufficient, the order will be rejected;
  - The profit and loss of the position will be calculated based on the position cost price and the latest transaction price (default frequency is 1 second);

- Persistent storage of data:

  - The transaction data and order data are not saved and will disappear after VeighNa Trader is closed;
  - The position data will be **immediately written to the hard disk file** when there is a change, and can be seen after restarting VeighNa Trader and logging in to the trading interface (need to receive the corresponding contract information).
