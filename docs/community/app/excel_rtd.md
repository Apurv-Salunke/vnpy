# ExcelRtd - EXCEL RTD Module

## Function Overview

ExcelRtd is a functional module for **accessing any data information in VeighNa programs through Excel**. RTD stands for RealTimeData, which is an Excel data docking solution designed by Microsoft mainly for real-time data requirements in the financial industry. ExcelRtd depends on the PyXLLC module (www.pyxll.com), which is commercial software and needs to be purchased to use (30-day free trial is provided).

## Installing PyXLL
To use the ExcelRtd module, you need to install the PyXLL plugin. The steps are as follows:

First, go to the [PyXLL official website](https://www.pyxll.com/), click Download PyXLL, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/excel_rtd_0.png)

Then you will be redirected to the download interface, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/13.png)

At this time, you need to fill in the corresponding fields. Among them, **Python Version** should select Python 3.10, and **Excel Version** should be selected according to your installed Excel version, generally 64bit (x64).

After filling in, click [Download PyXLL] to jump to the download page. After downloading the file, enter the folder where the file is placed, hold the shift key and click the right mouse button, select [Open PowerShell window here], and run the following commands:
```bash
pip install pyxll
pyxll install
```

Then you can successfully install according to the software requirements.

Please note that when executing to the step shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/excel_rtd_9.png)

If no specific path is specified, it will be installed to the default location shown in the figure (because you need to enter this folder later, please remember this path).

Then enter the examples directory under this directory, and put vnpy_rtd.py from the path ~/veighna_studio/Lib/site-packages/vnpy_excelrtd/ into this directory, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/excel_rtd_5.png)

This completes the formal installation.

## Loading and Launching

### Loading via VeighNa Station

After launching and logging into VeighNa Station, click the [Trading] button. In the configuration dialog, check [ExcelRtd] in the [Application Module] section.

### Loading via Script

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_excelrtd import ExcelRtdApp

# Write after creating the main_engine object
main_engine.add_app(ExcelRtdApp)
```

## Starting the Module

Before starting the module, please connect to the trading interface first (for connection methods, see the Interface Connection section in the Basic Usage chapter). After seeing "Contract information query successful" output in the [Log] section of the VeighNa Trader main interface, start the module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/1.png)

Please note that because the IB interface cannot automatically obtain all contract information upon login, it can only be obtained when the user manually subscribes to market data. Therefore, you need to manually subscribe to contract market data on the main interface before starting the module.

After successfully connecting to the trading interface, click [Function] -> [Excel RTD] in the menu bar, or click the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/excel_rtd_6.png)

You can then enter the UI interface of the Excel RTD module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/15.png)


## Functions and Configuration

### Basic Applications

After starting the Excel RTD module, you can call the functions provided by this module through PyXll in Excel tables (mainly obtaining real-time data through the rtd_tick_data function).

First, open an Excel table, and call the rtd_tick_data function in each cell and pass in the corresponding parameters to obtain the corresponding data, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/14.png)

The figure above is an example of obtaining real-time data for four fields of Soybean Meal 2205 (namely bid_price_1, high_price, low_price, and last_price).

From the figure, it can be seen that the rtd_tick_data function requires two parameters: one is vt_symbol, and the other is the attribute of TickData defined in VeighNa (specific attributes can be found in the source code vnpy.trader.object.TickData). Both parameters are strings. The first parameter can be specified through the specific position of the cell, such as "A1" indicating the data in column A, row 1.

At the same time, corresponding output can also be seen in the GUI of the Excel RTD module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/16.png)

### Advanced Applications
Of course, the above is just a simple demonstration of the ExcelRtd module's functions. As for what specific data to obtain and how to display it in Excel, it is up to the user to write according to their actual needs. Here are several advanced cases, including futures market quote tracking, market depth market tracking, and spread monitoring:

#### Futures Market Quote Tracking
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/excel_rtd_10.png)

#### Market Depth Market Tracking

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/excel_rtd_11.png)

#### Spread Monitoring

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/excel_rtd_12.png)
