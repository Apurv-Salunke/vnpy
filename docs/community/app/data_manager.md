# DataManager - Historical Data Management Module

## Function Overview

DataManager is a functional module for **historical data management**. Users can conveniently complete tasks such as data downloading, data viewing, data importing, and data exporting through its UI interface.

## Loading and Launching

### Loading via VeighNa Station

After launching and logging into VeighNa Station, click the [Trading] button. In the configuration dialog, check [DataManager] in the [Application Module] section.

### Loading via Script

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_datamanager import DataManagerApp

# Write after creating the main_engine object
main_engine.add_app(DataManagerApp)
```


## Starting the Module

After launching VeighNa Trader, click [Function] -> [Data Management] in the menu bar, or click the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/00.png)

You can then enter the historical data management UI interface, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/1.png)


## Downloading Data

The DataManager module provides one-click historical data downloading functionality. Click the [Download Data] button in the upper right corner, and a download historical data window will pop up, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/2.png)

You need to fill in four fields: code, exchange, period, and start date:

<span id="jump">

- Code
  - Code format is contract variety
  - Such as IF888, rb2105
- Exchange
  - Exchange where the contract is traded (click the arrow button on the right side of the window to select the list of exchanges supported by VeighNa)
- Period
  - MINUTE (1-minute K-line)
  - HOUR (1-hour K-line)
  - DAILY (daily K-line)
  - WEEKLY (weekly K-line)
  - TICK (one Tick)
- Start Date
  - Format is yy/mm/dd
  - Such as 2018/2/25

</span>

After filling in, click the [Download] button below to start the download program. Successful download is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/3.png)

Note that historical data after download completion will be saved in the local database and can be used directly in subsequent backtesting or live trading without repeated downloads.

### Data Source: Data Services (Futures, Stocks, Options)

Taking RQData as an example, [RQData](https://www.ricequant.com/welcome/purchase?utm_source=vnpy) provides historical data for domestic futures, stocks, and options. Before use, ensure the data service is correctly configured (for configuration methods, see the Global Configuration section in the Basic Usage chapter).

### Data Source: IB (Foreign Futures, Stocks, Spot, etc.)

Interactive Brokers (IB) provides rich historical data downloads for foreign markets (including stocks, futures, options, spot, etc.). Note that before downloading, you need to start the IB TWS trading software first, connect the IB interface on the VeighNa Trader main interface, and subscribe to the required contract market data.


## Importing Data

If you have obtained CSV format data files from other channels, you can quickly import them into the VeighNa database through DataManager's data import function. Click the [Import Data] button in the upper right corner, and a dialog will pop up as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/21.png)

Click the [Select File] button at the top, and a window will pop up to select the CSV file path to import, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/5.png)

Then configure the details of data import:

- Contract Information
  - Format details are in the [Downloading Data](#jump) section of this chapter;
  - Please note that the imported contract code (symbol) and exchange (exchange) two fields combined constitute the local code (vt_symbol) used in modules such as CTA Backtester;
  - If the contract code is **IF2003** and the exchange selected is **CFFEX** (China Financial Futures Exchange), then the local code used in backtesting in CtaBacktester should be **IF2003.CFFEX**;
  - You can select the timestamp timezone;
- Header Information
  - You can view the CSV file header information and input the corresponding header strings in the header information;
  - For fields that do not exist in the CSV file (such as stock data does not have [Open Interest] field), please leave it blank;
- Format Information
  - Uses the time format definition of Python's built-in datetime module to parse timestamp strings;
  - Default time format is "%Y-%m-%d %H:%M:%S", corresponding to "2017-1-3 0:00:00";
  - If the timestamp is "2017-1-3  0:00", then the time format should be "%Y-%m-%d %H:%M".

After filling in, it is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/22.png)

Click the [OK] button to start importing data from the CSV file into the database. During the import process, the interface may be somewhat stuck. The larger the CSV file (the more data), the longer the stuck time will be. After successful loading, a window will pop up showing successful loading, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/20.png)


## Viewing Data

Currently, there are three ways to obtain data in VeighNa Trader:

- Download through data services or trading interfaces

- Import from CSV files

- Record using the DataRecorder module

Regardless of which method is used to obtain data, click the [Refresh] button in the upper left corner to see the statistical situation of existing data in the current database (except Tick data). During the refresh process, the interface may have occasional lag. Usually, the more data, the longer the lag time. After successful refresh, it is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/7.png)

Click the [View] button, and a dialog box for selecting the data interval to view will pop up, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/10.png)

After selecting the data range to display, click the [OK] button to see specific data fields at each time point in the right table:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/11.png)

With existing data in the database, click the small arrow before the data frequency in the leftmost [Data] column of the table to expand or collapse the contract information under that data frequency.

If the right area of the table is incomplete, you can drag the horizontal scroll bar at the bottom of the interface to adjust.


## Exporting Data

If you want to export data from the database to a local CSV file, you can select the contract to export, click the [Export] button on the right side of the row where the contract is located, and a dialog for selecting the data interval will pop up, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/8.png)

Select the data interval range to export, click [OK], and a dialog will pop up again to select the output file location, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/9.png)

After selecting the directory where the exported file should be placed and filling in the CSV file name, click the [Save] button to complete the CSV file export.


## Deleting Data

If you want to delete specific contract data, you can select the contract to delete, click the [Delete] button on the right side of the contract row data, and a dialog will pop up, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/12.png)

Click the [OK] button to delete the contract data, and a deletion success window will pop up, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/13.png)

At this time, click the [Refresh] button again, and the contract information has disappeared from the GUI, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/14.png)


## Updating Data

When users **have configured data services** or **trading interfaces (connected) provide sufficient historical data**, click the [Update Data] button in the upper right corner to execute one-click automatic download update based on all contract data displayed in the GUI.

The GUI display before update is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/17.png)

Click the [Update Data] button, and an information prompt dialog for update progress will pop up, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/19.png)

At this time, DataManager will automatically **download data from the end date of existing data in the database to the current latest date** and update it to the database.

If there is less data to update, the update task may be completed instantly. In this case, it is normal not to observe the update dialog.

After update is completed, click the [Refresh] button in the upper left corner to see that the contract data has been updated to the current latest date.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/18.png)

## Data Range

Please note that although the interface displays the start and end times of existing data in the database, **it does not mean that the database stores all data from the start time to the end time**.

If relying on historical data provided by the trading interface, once the time span between the start time and end time exceeds the data range that the interface can provide, it may cause data gaps. Therefore, it is recommended to click the [View] button after updating data to check whether the contract data is continuous.
