# DataRecorder - Live Market Recording Module

DataRecorder is a module for **live market recording**. Users can use this module to record real-time Tick data and K-line data, and automatically write and save them to the database.

Recorded data can be viewed through the DataManager module and can also be used for historical backtesting in CtaBacktester, as well as live initialization of strategies such as CtaStrategy and PortfolioStrategy.

## Loading and Launching

### Loading via VeighNa Station

After launching and logging into VeighNa Station, click the [Trading] button. In the configuration dialog, check [DataRecorder] in the [Application Module] section.

### Loading via Script

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_datarecorder import DataRecorderApp

# Write after creating the main_engine object
main_engine.add_app(DataRecorderApp)
```

## Starting the Module

Before starting the module, please connect to the trading interface first (for connection methods, see the Interface Connection section in the Basic Usage chapter). After seeing "Contract information query successful" output in the [Log Bar] of the VeighNa Trader main interface, start the module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/1.png)

Please note that because the IB interface cannot automatically obtain all contract information upon login, it can only be obtained when the user manually subscribes to market data. Therefore, you need to manually subscribe to contract market data on the main interface before starting the module.

After successfully connecting to the trading interface, click [Function] -> [Market Recording] in the menu bar, or click the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_recorder/1.png)

You can then start DataRecorder, and the DataRecorder UI interface will pop up, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_recorder/4.png)


## Adding Records

The DataRecorder module supports adding K-line (1-minute) and Tick data recording tasks on demand:

1. Enter the contract local code (vt_symbol) to be recorded in the [Local Code] edit box, as shown in the figure below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_recorder/5.png)
- Note that the local code consists of two parts: code prefix and exchange suffix, such as rb2112.SHFE;
- The edit box provides auto-completion function for contract information received after interface connection (case-sensitive);

2. Select the timed batch writing frequency in the [Write Interval] edit box, as shown in the figure below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_recorder/6.png)
This way, all data to be recorded is first taken out from the queue each time, and then all existing data in the queue is written to the database at once, thereby reducing database pressure and recording delay;

3. Click the [Add] button corresponding to [K-line Record] or [Tick Record] on the right to add recording tasks:

- After successful addition, the contract local code will appear in the [K-line Record List] or [Tick Record List] below, and corresponding logs will be output at the bottom of the interface, as shown in the figure below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_recorder/10.png)


## Removing Records

When you no longer need to record market data for a certain contract, you can remove its corresponding recording task:

1. Enter the contract local code (vt_symbol) for which you want to remove the recording task in the [Local Code] edit box;
2. Click the [Remove] button corresponding to [K-line Record] or [Tick Record] on the right to remove the corresponding recording task.

After successful removal, the recording task information under the [K-line Record List] or [Tick Record List] will be removed, and corresponding logs will be output at the bottom of the interface, as shown in the figure below:
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_recorder/9.png)
