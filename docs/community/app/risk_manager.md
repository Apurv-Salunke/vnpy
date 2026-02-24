# RiskManager - Pre-trade Risk Control Management Module

## Function Overview

The RiskManager module is a functional module for **pre-trade risk control management**. Users can conveniently complete tasks such as starting risk control, modifying parameters, and stopping risk control through its UI interface.

## Loading and Launching

### Loading via VeighNa Station

After launching and logging into VeighNa Station, click the [Trading] button. In the configuration dialog, check [RiskManager] in the [Application Module] section.

### Loading via Script

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_riskmanager import RiskManagerApp

# Write after creating the main_engine object
main_engine.add_app(RiskManagerApp)
```

## Starting the Module

Click [Function] -> [Trading Risk Control] in the menu bar, or click the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/risk_manager/1-1.png)

You can then enter the UI interface of the pre-trade risk control module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/risk_manager/1-2.png)


## Starting Risk Control

The pre-trade risk control module is responsible for checking whether the status of orders meets various risk control rules before they are sent through the trading API interface. Risk control rules include trading flow control, order quantity, active orders, total cancellation count, etc., as follows:

 - Order Flow Control Related:
   - Order Flow Control Upper Limit: Maximum number of orders allowed to be sent within a given time window
   - Order Flow Control Clear: How many seconds to clear the above statistics of order count
 - Single Order Upper Limit: Maximum order quantity allowed for each order
 - Total Trade Upper Limit: Maximum total number of trades allowed today (note not number of orders)
 - Active Order Upper Limit: Maximum number of orders allowed to be in active state (submitted, not filled, partially filled)
 - Contract Cancellation Upper Limit: Maximum number of cancellations allowed per contract today (each contract is counted independently)

It is recommended to start pre-trade risk control before running automatic trading every day to check whether each order sent meets risk control requirements:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/risk_manager/1-3.png)

1. Select [Start] from the dropdown box in the [Risk Control Running Status] section;
2. After setting various risk control rule parameters, click the [Save] button below to start running risk control;
3. At this time, every order in the system needs to meet all risk control requirements (not exceeding limits) before it can be sent through the underlying interface.


## Parameter Modification

The pre-trade risk control module allows users to customize risk control parameters:

* Users can click the up and down arrows on the right side of the input box to modify parameters, or directly enter numbers to modify, as shown in the figure below.
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/risk_manager/1-4.png)
* After modification, please click the [Save] button to take effect.

## Stopping Risk Control

When risk control is not needed, users can stop risk control:

* Select [Stop] from the dropdown box in the [Risk Control Running Status], as shown in the figure below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/risk_manager/1-5.png)
* Click the [Save] button below to stop risk control checking for orders.
