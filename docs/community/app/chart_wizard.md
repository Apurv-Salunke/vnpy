# ChartWizard - Real-time K-line Chart Module

## Function Introduction

ChartWizard is a functional module for **real-time K-line chart display**, allowing users to view real-time and historical K-line market data through its UI interface. Currently, it only supports displaying 1-minute level K-line data, with the real-time K-line (the latest K-line) updated at the Tick level.

## Loading and Startup

### VeighNa Station Loading

After logging into VeighNa Station, click the 【Trading】 button, and in the configuration dialog, check the 【ChartWizard】 in the 【Application Module】 column.

### Script Loading

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_chartwizard import ChartWizardApp

# Write after creating the main_engine object
main_engine.add_app(ChartWizardApp)
```


## Starting the Module

Before starting the module, please connect to the trading interface (the connection method is detailed in the basic usage section of the connection interface). After seeing the output of "Contract information query successful" in the VeighNa Trader main interface 【Log】 column, start the module as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/1.png)

Please note, the IB interface cannot automatically obtain all contract information when logging in, and can only obtain it when the user manually subscribes to market data. Therefore, you need to manually subscribe to market data on the main interface before starting the module.

Since VeighNa itself does not provide any data services, for the historical data used in the K-line chart drawing process, domestic futures historical data is provided by the data service, and users need to prepare and configure data service accounts (configuration method detailed in the basic usage section of the global configuration part).

After successfully connecting to the trading interface, in the menu bar, click 【Function】-> 【K-line Chart】, or click the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/chart_wizard/1.png)

This will enter the UI interface of the real-time K-line chart module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/chart_wizard/2.png)


## Creating a New Chart

After opening the chart window, in the 【Local Code】 editing box, enter the contract code (note that the local code consists of two parts: the code prefix and the exchange suffix, such as rb2112.SHFE).

Click the 【Create New Chart】 button to create a K-line chart for the corresponding contract, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/chart_wizard/3.png)

Users can create K-line charts for multiple contracts, and switch between them quickly through window switching: 

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/chart_wizard/4.png)


## Viewing Charts

Each contract's chart is divided into two sub-chart areas:

- The top sub-chart is for market K-line;
- The bottom sub-chart is for trading volume data.

The crosshair cursor on the chart can be used to locate and display specific data points at a given time, and labels corresponding to the data points will appear on the X-axis and Y-axis, and the OHLCV information of the K-line will also be displayed in the top left corner.

Other quick operations:

- You can drag the K-line chart display time range left and right with the left mouse button;
- You can zoom in and out of the K-line chart display time range by scrolling the mouse wheel.
