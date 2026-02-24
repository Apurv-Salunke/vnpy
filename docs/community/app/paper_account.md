# PaperAccount - Local Simulation Trading Module


## Function Overview

PaperAccount is a functional module for **local simulation trading**. Users can conduct localized simulated trading based on live market data through its UI interface.

## Loading and Launching

### Loading via VeighNa Station

After launching and logging into VeighNa Station, click the [Trading] button. In the configuration dialog, check [PaperAccount] in the [Application Module] section.

### Loading via Script

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_paperaccount import PaperAccountApp

# Write after creating the main_engine object
main_engine.add_app(PaperAccountApp)
```


## Starting the Module

Before starting the module, please connect to the interface for simulated trading first (for connection methods, see the Interface Connection section in the Basic Usage chapter). After seeing "Contract information query successful" output in the [Log] section of the VeighNa Trader main interface, start the module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/1.png)

Please note that because the IB interface cannot automatically obtain all contract information upon login, it can only be obtained when the user manually subscribes to market data. Therefore, you need to manually subscribe to contract market data on the main interface before starting the module.

After the trading interface is connected, the local simulation trading module automatically starts. At this time, all contract trading orders and cancellation requests are **taken over by the local simulation trading module** and will no longer be sent to the live server.


## Function Configuration

Click [Function] -> [Simulation Trading] in the menu bar, or click the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/paper_account/4.png)

You can then enter the UI interface of the local simulation trading module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/paper_account/5.png)

Users can configure the following functions through the UI interface:

- Execution slippage for market orders and stop orders
  - Used to affect the **slippage ticks** of the execution price relative to the order book price when market orders and stop orders are executed;

- Simulation trading position P&L calculation frequency
  - How many seconds to execute a position P&L calculation update. If you find the program lagging when there are many positions, it is recommended to try reducing the frequency;

- Immediately match using current order book after placing order
  - By default, orders placed by users need to **wait for the next TICK order book push to be matched** (simulating live trading scenarios). For inactive contracts with low TICK push frequency, you can check this option. After placing an order, it will **be immediately matched based on the current latest TICK order book**;

- Clear all positions
  - Clear all local position data with one click.

The local simulation trading module can also be used together with other strategy application modules (such as CtaStrategy module, SpreadTrading module, etc.), thereby achieving localized quantitative strategy simulation trading testing.


## Data Monitoring

Users can query and confirm the trading interface status of contracts through [Query Contract]:

Click [Help] -> [Query Contract] in the menu bar, and directly click the [Query] button in the pop-up dialog. You will find that the [Trading Interface] column of all contracts displays PAPER, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/paper_account/2.png)

Before placing orders and cancelling orders for a certain contract, users must first **subscribe** to the market data of that contract.

In the figure below, the information displayed in the [Order], [Trade], and [Position] three monitoring components all have PAPER in the interface column (local simulation data):

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/paper_account/3.png)

Please note that the local simulation trading module **does not provide capital calculation functions**, so the [Capital] component displays the capital of the live trading account and will not change due to orders generated in the local simulation trading module.


## Business Logic

The business logic of the local simulation trading module is as shown below:

- Supported order types (unsupported types will be rejected):

  - Limit orders;
  - Market orders;
  - Stop orders;

- Order matching rules adopt **price-arrival execution** mode. Taking buy orders as an example:

  - Limit orders: When the order book ask price ask_price_1 is less than or equal to the order price, execution occurs;
  - Stop orders: When the order book ask price ask_price_1 is greater than or equal to the order price, execution occurs;

- **Order book hanging volume is not considered** when orders are executed; they are executed all at once;

- After order execution, OrderData order status update is pushed first, then TradeData trade information is pushed, **consistent with the order in live trading**;

- After order execution, the module will automatically record corresponding position information PositionData:

  - Maintain corresponding position information according to the contract's own position mode (long/short positions vs. net positions) information;
  - **When opening positions are executed, the weighted average is used to calculate and update the position cost price;**
  - **When closing positions are executed, the position cost price remains unchanged;**
  - In long/short position mode, hanging closing orders will freeze corresponding position quantities. Orders will be rejected when available quantity is insufficient;
  - Position P&L will be calculated regularly based on position cost price and latest transaction price (default frequency 1 second);

- Data persistence saving:

  - Trade data and order data are not saved. They disappear after closing VeighNa Trader;
  - Position data will be **immediately written to hard disk files** when there are changes. After restarting VeighNa Trader and logging into the trading interface, you can see them (after receiving corresponding contract information).
