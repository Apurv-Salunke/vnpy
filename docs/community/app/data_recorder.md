# DataRecorder - Real-Time Market Data Recording Module

DataRecorder is a module designed for **real-time market data recording**. Users can utilize this module to record real-time Tick data and K-line data, which are automatically written and saved to a database.

The recorded data can be viewed through the DataManager module, and can also be used for historical backtesting with CtaBacktester, as well as for the initialization of real-time strategies such as CtaStrategy and PortfolioStrategy.

## Loading and Starting

### VeighNa Station Loading

After logging into VeighNa Station, click the 【Trading】 button, and in the configuration dialog box, check the 【DataRecorder】 box under the 【Application Modules】 column.

### Script Loading

Add the following code to your script:

```python3
# At the top
from vnpy_datarecorder import DataRecorderApp

# After creating the main_engine object
main_engine.add_app(DataRecorderApp)
```

## Starting the Module

Before starting the module, please first connect to the trading interface (connection methods are detailed in the basic usage section's connection interface part). Wait until you see "Contract information query successful" in the VeighNa Trader main interface's 【Log Bar】 before starting the module, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/1.png)

Please note that the IB interface cannot automatically obtain all contract information during login, and can only obtain it when the user manually subscribes to market data. Therefore, you need to manually subscribe to contract market data on the main interface before starting the module.

After successfully connecting to the trading interface, click 【Function】 -> 【Market Data Recording】 in the menu bar, or click the icon in the left sidebar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_recorder/1.png)

This will start DataRecorder and pop up the DataRecorder UI interface, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_recorder/4.png)


## Adding Records

The DataRecorder module supports adding recording tasks for K-line (1-minute) and Tick data as needed:

1. In the 【Local Code】 edit box, enter the local code (vt_symbol) of the contract you want to record, as shown below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_recorder/5.png)
- Note that the local code consists of two parts: the code prefix and the exchange suffix, such as rb2112.SHFE;
- The edit box provides auto-complete functionality (case-sensitive) for contract information received after connecting to the interface;

2. In the 【Write Interval】 edit box, select the frequency for batch writing, as shown below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_recorder/6.png)
This allows you to take all pending data from the queue and write it to the database in one go, reducing database pressure and recording latency;

3. Click the corresponding 【Add】 button for K-line recording or Tick recording to add the recording task:

- After adding successfully, the local code of the contract will appear in the 【K-line Recording List】 or 【Tick Recording List】 below, and the corresponding log will be output at the bottom of the interface, as shown below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_recorder/10.png)


## Removing Records

When you no longer need to record market data for a particular contract, you can remove its corresponding recording task:

1. In the 【Local Code】 edit box, enter the local code (vt_symbol) of the contract for which you want to remove the recording task;
2. Click the corresponding 【Remove】 button for K-line recording or Tick recording to remove the recording task.

After removing successfully, the recording task information corresponding to the contract will be removed from the 【K-line Recording List】 or 【Tick Recording List】, and the corresponding log will be output at the bottom of the interface, as shown below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_recorder/9.png)
