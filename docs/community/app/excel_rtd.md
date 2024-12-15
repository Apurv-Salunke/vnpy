# ExcelRtd - EXCEL RTD Module

## Function Introduction

ExcelRtd is a functional module for **accessing any data information within VeighNa programs in Excel**, RTD stands for RealTimeData, which is a data connection solution designed by Microsoft primarily for the financial industry's real-time data needs. ExcelRtd relies on the PyXLLC module (www.pyxll.com), which is commercial software that requires purchase for use (offers a 30-day free trial).

## Installing PyXLL
To use the ExcelRtd module, you need to install the PyXLL plugin. The steps are as follows:

First, enter the [PyXLL website](https://www.pyxll.com/), click Download PyXLL, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/excel_rtd_0.png)

Then, jump to the download interface, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/13.png)

At this time, you need to fill in the corresponding fields, where **Python Version** selects Python3.10, and **Excel Version** selects according to your installed Excel version, usually 64bit(x64).

After filling in, click 【Download PyXLL】, which will jump to the download page. After downloading the file, enter the folder where the file is located, hold down the shift key and right-click, select 【Open PowerShell window here】, and run the following commands:
```bash
pip install pyxll
pyxll install
```

Then, follow the software requirements to successfully install.

Please note, when you reach the following step:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/excel_rtd_9.png)

If no specific path is specified, it will be installed to the default location shown in the figure (because you need to enter this directory later, so please remember this path).

Then, enter the examples directory under the directory, and put the path ~/veighna_studio/Lib/site-packages/vnpy_excelrtd/ under vnpy_rtd.py into this directory, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/excel_rtd_5.png)

This completes the formal installation.

## Loading and Starting

### VeighNa Station Loading

After logging into VeighNa Station, click the 【Trading】 button, and in the configuration dialog, check the 【ExcelRtd】 in the 【Application Module】 column.

### Script Loading

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_excelrtd import ExcelRtdApp

# Write after creating the main_engine object
main_engine.add_app(ExcelRtdApp)
```

## Starting the Module

Before starting the module, please connect to the trading interface (the connection method is detailed in the basic usage section of the connection interface). After seeing the output of "Contract information query successful" in the VeighNa Trader main interface 【Log】 column, start the module as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/1.png)

Please note that the IB interface cannot automatically obtain all contract information when logging in, and can only obtain it when the user manually subscribes to market data. Therefore, you need to manually subscribe to market data on the main interface before starting the module.

Successfully connecting to the trading interface, in the menu bar click 【Function】-> 【Excel RTD】, or click on the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/excel_rtd_6.png)

You can enter the UI interface of the Excel RTD module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/15.png)


## Function and Configuration

### Basic Application

After starting the Excel RTD module, you can call the functions provided by the module in Excel through PyXll (mainly through the rtd_tick_data function to get real-time data).

First, open an Excel spreadsheet, and in each cell, call the rtd_tick_data function and pass in the corresponding parameters to get the corresponding data, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/14.png)

The above figure is an example of getting four fields of real-time data for soybean oil 2205 (bid_price_1, high_price, low_price, and last_price).

From the figure, it can be seen that the rtd_tick_data function requires two parameters: one is vt_symbol, and the other is the attribute of TickData defined in VeighNa (specific attributes can be referenced in the source code vnpy.trader.object.TickData). Both parameters are strings, the first parameter can be specified by the specific position of the cell, such as "A1" indicating the data in the A column and the first row.

At the same time, in the graphical interface of the Excel RTD module, you can also see the corresponding output, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/16.png)

### Advanced Application
Of course, the above is just a simple demonstration of the ExcelRtd module's functionality. As for which data to get and how to display it in Excel, it depends on the user's actual needs to write. Here are a few advanced examples, including futures market quote tracking, market depth quote tracking, and spread monitoring:

#### Futures Market Quote Tracking
![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/excel_rtd_10.png)

#### Market Depth Quote Tracking

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/excel_rtd_11.png)
#### Spread Monitoring

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/excel_rtd/excel_rtd_12.png)