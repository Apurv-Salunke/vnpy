# ChartWizard - Real-time K-line Chart Module

## Function Overview

ChartWizard is a functional module for **real-time K-line chart display**. Users can view real-time and historical K-line market data through its UI interface. Currently, it only supports displaying 1-minute level K-line data. Real-time K-lines (the latest K-line) are refreshed at the Tick level.

## Loading and Launching

### Loading via VeighNa Station

After launching and logging into VeighNa Station, click the [Trading] button. In the configuration dialog, check [ChartWizard] in the [Application Module] section.

### Loading via Script

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_chartwizard import ChartWizardApp

# Write after creating the main_engine object
main_engine.add_app(ChartWizardApp)
```


## Starting the Module

Before starting the module, please connect to the trading interface first (for connection methods, see the Interface Connection section in the Basic Usage chapter). After seeing "Contract information query successful" output in the [Log] section of the VeighNa Trader main interface, start the module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_strategy/1.png)

Please note that because the IB interface cannot automatically obtain all contract information upon login, it can only be obtained when the user manually subscribes to market data. Therefore, you need to manually subscribe to contract market data on the main interface before starting the module.

Since VeighNa itself does not provide any data services, for historical data used in K-line chart drawing, domestic futures historical data is provided by data services. Users need to prepare and configure data service accounts (for configuration methods, see the Global Configuration section in the Basic Usage chapter).

After successfully connecting to the trading interface, click [Function] -> [K-line Chart] in the menu bar, or click the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/chart_wizard/1.png)

You can then enter the UI interface of the real-time K-line chart module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/chart_wizard/2.png)


## Creating New Charts

After opening the chart window, enter the contract code in the [Local Code] edit box (note that the local code consists of two parts: code prefix and exchange suffix, such as rb2112.SHFE).

Click the [New Chart] button to create a K-line chart for the corresponding contract, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/chart_wizard/3.png)

Users can create K-line charts for multiple contracts and switch between them quickly by switching windows:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/chart_wizard/4.png)


## Viewing Charts

Each contract's chart is divided into upper and lower sub-chart areas:

- The upper sub-chart shows the market K-line;
- The lower sub-chart shows volume data.

The crosshair cursor on the chart can be used to position and display specific data at a specific time point. It will correspond to data point labels on both the X-axis and Y-axis, and the OHLCV information for this K-line will also be displayed in the upper left corner.

Other quick operations:

- You can drag left and right with the left mouse button to translate the time range displayed in the K-line chart;
- You can use the mouse wheel to zoom in and out of the time range displayed in the K-line chart.
