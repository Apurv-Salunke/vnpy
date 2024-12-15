# DataManager - Historical Data Management Module

## Function Introduction

DataManager is a functional module for **historical data management**, allowing users to conveniently complete tasks such as data downloading, data viewing, data importing, and data exporting through its UI interface.

## Loading and Starting

### VeighNa Station Loading

After logging in to VeighNa Station, click the 【Transaction】 button, and in the configuration dialog box, check the 【DataManager】 in the 【Application Module】 column.

### Script Loading

Add the following code to your startup script:

```python3
# Write at the top
from vnpy_datamanager import DataManagerApp

# Write after creating the main_engine object
main_engine.add_app(DataManagerApp)
```


## Starting the Module

After starting VeighNa Trader, click 【Function】 -> 【Data Management】 in the menu bar, or click the icon in the left sidebar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/00.png)

This will enter the historical data management UI interface, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/1.png)


## Downloading Data

The DataManager module provides a one-click function for downloading historical data. Click the 【Download Data】 button in the top right corner, and the download historical data window will pop up, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/2.png)

You need to fill in the following four fields of information:

<span id="jump">

- Symbol
  - The format is the contract variety
  - For example, IF888, rb2105
- Exchange
  - The exchange where the contract is traded (you can select the list of exchanges supported by VeighNa by clicking the arrow button on the right side of the window)
- Period
  - MINUTE (1-minute K-line)
  - HOUR (1-hour K-line)
  - DAILY (daily K-line)
  - WEEKLY (weekly K-line)
  - TICK (one Tick)
- Start Date
  - The format is yy/mm/dd
  - For example, 2018/2/25

</span>

After filling in the information, click the 【Download】 button at the bottom to start the download program. The download is successful, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/3.png)

Note that the downloaded historical data will be saved in the local database, which can be directly used for backtesting or live trading without needing to be downloaded again.

### Data Source: Data Service (Futures, Stocks, Options)

Taking RQData as an example, [RQData](https://www.ricequant.com/welcome/purchase?utm_source=vnpy) provides historical data for domestic futures, stocks, and options. Ensure that the data service is correctly configured before use (configuration methods are detailed in the global configuration section of the basic usage chapter).

### Data Source: IB (Foreign Futures, Stocks, Commodities, etc.)

Interactive Brokers (IB) provides rich historical data downloads for foreign markets (including stocks, futures, options, and commodities), noting that you need to start IB TWS trading software and connect to the IB interface in the VeighNa Trader main interface, and subscribe to the required contract quotes before downloading.

## Importing Data

If you have obtained CSV format data files from other channels, you can quickly import them into the VeighNa database using the DataManager's data import function. Click the 【Import Data】 button in the top right corner, and the following dialog box will pop up:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/21.png)

Click the 【Select File】 button at the top, and a window will pop up to select the path of the CSV file to be imported, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/5.png)

Then, configure the details of the data import:

- Contract Information
  - The format is detailed in the [Downloading Data](#jump) section;
  - Please note that the combination of the contract code (symbol) and exchange two fields forms the local code (vt_symbol) used in modules such as CTA backtesting;
  - If the contract code is **IF2003**, the exchange selected is **CFFEX** (China Financial Futures Exchange), then the local code used in CtaBacktester should be **IF2003.CFFEX**;
  - You can select the time zone for the timestamp;
- Header Information
  - You can view the header information of the CSV file and input the corresponding header strings;
  - For fields that do not exist in the CSV file (such as the "Position" field for stock data), please leave them blank;
- Format Information
  - Use the time format definition of the Python built-in library datetime module to parse the timestamp string;
  - The default time format is "%Y-%m-%d %H:%M:%S", corresponding to "2017-1-3 0:00:00";
  - If the timestamp is "2017-1-3  0:00", then the time format should be "%Y-%m-%d %H:%M".

After filling in the information, it will look like this:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/22.png)

Click the 【OK】 button to start importing data from the CSV file into the database. During the import process, the interface may be temporarily stuck, and the longer the import time, the larger the CSV file (the more data). After successful loading, a window will pop up to display the loading success, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/20.png)


## Viewing Data

There are currently three ways to obtain data in VeighNa Trader:

- Downloading through data services or trading interfaces

- Importing from CSV files

- Using the DataRecorder module to record

Regardless of the method used to obtain the data, clicking the 【Refresh】 button in the top left corner will show the statistical situation of the data already in the database (excluding Tick data). The refresh process may occasionally be stuck, and the longer the refresh time, the more data there is. After successful refresh, it will look like this:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/7.png)

Clicking the 【View】 button will pop up a dialog box for selecting the data range to view, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/10.png)

After selecting the data range to display, click the 【OK】 button to see the specific data fields for each time point in the right table:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/11.png)

On the premise that there is already data in the database, clicking the small arrow in the leftmost column of the table will expand or collapse the display of contract information for that data frequency.

If the right area of the table does not display completely, you can adjust it by dragging the horizontal scroll bar at the bottom of the interface.

## Exporting Data

If you want to export data from the database to a local CSV file, you can select the contract to export, click the 【Export】 button on the right side of the contract row, and a dialog box for selecting the data range will pop up, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/8.png)

Select the data range to export, click 【OK】, and then another dialog box will pop up to select the location of the output file, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/9.png)

Select the directory where the export file will be placed, fill in the CSV file name, and click the 【Save】 button to complete the CSV file export.

## Deleting Data

If you want to delete specific contract data, select the contract to delete, click the 【Delete】 button on the right side of the contract row, and a dialog box will pop up, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/12.png)

Click the 【OK】 button to delete the contract data, and a window will pop up to display the deletion success, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/13.png)

At this time, clicking the 【Refresh】 button again, the graphical interface will no longer have information about this contract, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/14.png)


## Updating Data

In the case where the user has **configured the data service** or **trading interface (already connected) providing sufficient historical data**, clicking the 【Update Data】 button in the top right corner will automatically download and update all contract data displayed on the graphical interface.

Before updating, the graphical interface displays as follows:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/17.png)

Clicking the 【Update Data】 button will pop up a dialog box with update progress information, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/19.png)

At this time, DataManager will automatically **download and update the data from the end date of the existing data in the database to the current latest date**.

If the amount of data to be updated is small, the update task may be completed instantly, and it is normal not to observe the update dialog box.

After the update is complete, clicking the 【Refresh】 button in the top left corner will show that the contract data has been updated to the current latest date.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/data_manager/18.png)

## Data Range

Please note that although the interface displays the start and end times of the data already in the database, **it does not mean that the database stores all the data between the start and end times**.

If relying on historical data provided by trading interfaces, once the time span between the start and end times exceeds the data range that the interface can provide, it may lead to gaps in the data. Therefore, it is recommended to check the continuity of the contract data after updating by clicking the 【View】 button.