# PortfolioManager - Investment Portfolio Management Module

## Function Introduction

PortfolioManager is a functional module for **investment portfolio management**. Users can use its UI interface to track the performance of trading strategies in real-time and analyze profits and losses.

## Loading and Startup

### VeighNa Station Loading

After logging into VeighNa Station, click the 【Trading】 button, and in the configuration dialog, check the 【PortfolioManager】 in the 【Application Module】 column.

### Script Loading

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_portfoliomanager import PortfolioManagerApp

# Write after creating the main_engine object
main_engine.add_app(PortfolioManagerApp)
```


## Module Startup

To start the module, click on the menu bar 【Function】-> 【Portfolio】, or click on the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_manager/1.jpg)

This will enter the UI interface of the investment portfolio management module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_manager/6.png)


## Portfolio Information Table

The interface can be divided into two parts on the left and right sides. The left side displays the information table of the current investment portfolios, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_manager/7.png)


The meaning of each column in the portfolio information table is as follows:

 - Portfolio Name: Reference identifier (reference), all trade requests sent from VeighNa can be directly distinguished by this identifier, such as manual trading, algorithm execution, quantitative strategies, etc., each trade source can be viewed as an independent investment portfolio.

   - Manual Trading: ManualTrading

   - CTA Strategy: CtaStrategy_strategy name

   - Spread Trading: SpreadTrading_spread name

   - Options Trading: OptionMaster_ElectronicEye/DeltaHedging

   - Algorithm Trading: AlgoTrading_algorithm number

   - Script Strategy: ScriptTrader

   - Portfolio Strategy: PortfolioStrategy_strategy name

 - Local Symbol: Contract code with exchange suffix (vt_symbol)

 - Opening Position: The position held by the investment portfolio in the contract at the close of the previous day (today's opening), including the position held by the contract.

 - Current Position: The result of adding the opening position to the trading volume of the day (buy open and sell close transactions).

 - Trading Profit/Loss: The profit and loss of all trades today, mapped to the current latest price.

 - Holding Profit/Loss: The profit and loss of the opening position of the portfolio, mapped to the current latest price.

 - Total Profit/Loss: The sum of trading profit and loss and holding profit and loss.

 - Buy Volume: The trading volume of buying open and buying close transactions of the contract in the investment portfolio today.

 - Sell Volume: The trading volume of selling open and selling close transactions of the contract in the investment portfolio today.

The calculation method for trading profit and loss (TradingPnl) and holding profit and loss (HoldingPnl) adopts the daily marking-to-market algorithm used by futures exchanges, and the calculation process is as follows:

 - Trading Profit/Loss = Position quantity * (Today's closing price - Yesterday's closing price) * Contract scale  

 - Holding Profit/Loss = Position change quantity * (Today's closing price - Opening transaction price) * Contract scale  

 - Total Profit/Loss = Trading Profit/Loss + Holding Profit/Loss  

 - Net Profit/Loss = Total Profit/Loss - Total Commission - Total Slippage  

Users can view information by expanding and collapsing investment portfolios and adjusting column widths:

 - Clicking the arrow on the left side of each investment portfolio can expand and collapse the information of each investment portfolio;

 - Clicking the top buttons for "Expand All" and "Collapse All" can perform batch operations on all investment portfolios;

 - Clicking the "Adjust Column Width" button can automatically adjust the width of each column in the table.

## Transaction Record Table

The right side of the interface displays all transaction records. Clicking the dropdown box in the top right corner can filter by investment portfolio, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_manager/8.png)


## Refresh Frequency

The profit and loss of the investment portfolio are automatically calculated based on a timed logic, and the calculation frequency can be adjusted through the option box in the top middle, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_manager/5.png)


Please note that all portfolio holding data will be written to a cache file when VeighNa Trader is closed, so do not directly kill the process to exit, as this will result in data loss.  

When loading the next day, the program will automatically settle yesterday's total position to today's yesterday's position field, which may not be suitable for 24-hour trading markets (foreign futures). The feature of daily settlement or manual settlement will be considered in the future.

If errors are found in position records or strategies have been removed, users can manually modify the cache file and restart VeighNa Trader.

The default path of the cache file on Windows systems is:

    C:\Users\Administrator\.vntrader\portfolio_manager_data.json

Where Administrator is the current Windows system username.