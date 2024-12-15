# RiskManager - Pre-Trade Risk Management Module

## Function Overview

RiskManager is a functional module designed for **pre-trade risk management**. Users can use its UI interface to conveniently complete tasks such as starting risk control, modifying parameters, and stopping risk control.

## Loading and Starting

### VeighNa Station Loading

After logging into VeighNa Station, click the 【Trading】 button, and in the configuration dialog box, check the 【RiskManager】 box under the 【Application Modules】 column.

### Script Loading

Add the following code to your script:

```python3
# At the top
from vnpy_riskmanager import RiskManagerApp

# After creating the main_engine object
main_engine.add_app(RiskManagerApp)
```

## Starting the Module

In the menu bar, click 【Function】 -> 【Trade Risk Control】, or click the icon in the left sidebar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/risk_manager/1-1.png)

This will enter the pre-trade risk control module's UI interface, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/risk_manager/1-2.png)


## Starting Risk Control

The pre-trade risk control module is responsible for checking whether the status of each order meets various risk control rules before it is sent through the trading API interface. The risk control rules include trade flow control, single order limit, total trade limit, active order limit, and contract cancellation limit, as follows:

 - Trade flow control related:
   - Trade flow control upper limit: the maximum number of orders allowed to be sent within a given time window
   - Trade flow control reset: the interval at which the above order count is reset
 - Single order limit: the maximum order quantity allowed for each order
 - Total trade limit: the maximum total trade quantity allowed for today (note: not the order quantity)
 - Active order limit: the maximum number of active orders (submitted, unexecuted, and partially executed) allowed
 - Contract cancellation limit: the maximum number of cancellations allowed for a single contract today (each contract is counted separately)

It is recommended to start pre-trade risk control every day before running automated trading to check if each order sent meets the risk control requirements:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/risk_manager/1-3.png)

1. In the 【Risk Control Running Status】 dropdown box, select 【Start】;
2. After setting the parameters for various risk control rules, click the 【Save】 button below to start the risk control;
3. At this point, every order within the system must meet all risk control requirements (not exceeding the limit) before it can be sent through the underlying interface.


## Modifying Parameters

The pre-trade risk control module allows users to customize risk control parameters:

* Users can modify parameters by clicking the up and down arrows on the right side of the input box, or by directly entering numbers, as shown below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/risk_manager/1-4.png)
* Please click the 【Save】 button to take effect.

## Stopping Risk Control

When risk control is not needed, users can stop risk control:

* In the 【Risk Control Running Status】 dropdown box, select 【Stop】, as shown below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/risk_manager/1-5.png)
* Click the 【Save】 button below to stop the risk control check for orders.
