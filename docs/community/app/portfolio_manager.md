
# PortfolioManager - Investment Portfolio Management Module

## Function Overview

PortfolioManager is a functional module for **investment portfolio management**. Users can conduct real-time performance tracking and P&L analysis on trading strategies during trading through its UI interface.


## Loading and Launching

### Loading via VeighNa Station

After launching and logging into VeighNa Station, click the [Trading] button. In the configuration dialog, check [PortfolioManager] in the [Application Module] section.

### Loading via Script

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_portfoliomanager import PortfolioManagerApp

# Write after creating the main_engine object
main_engine.add_app(PortfolioManagerApp)
```


## Starting the Module

Click [Function] -> [Investment Portfolio] in the menu bar, or click the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_manager/1.jpg)

You can then enter the UI interface of the investment portfolio management module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_manager/6.png)


## Portfolio Information Table

The interface can be divided into left and right parts overall. The left side displays the information table of current investment portfolios, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_manager/7.png)


The meaning of each column in the portfolio information table is as follows:

 - Portfolio Name: Order source identifier (reference). All order requests sent from VeighNa can directly distinguish their trading source through this identifier, such as manual trading, algorithm execution, quantitative strategies, etc. Each trading source can be regarded as an independent investment portfolio.

   - Manual Trading: ManualTrading

   - CTA Strategy: CtaStrategy_StrategyName

   - Spread Trading: SpreadTrading_SpreadName

   - Option Trading: OptionMaster_ElectronicEye/DeltaHedging

   - Algorithm Trading: AlgoTrading_AlgorithmNumber

   - Script Strategy: ScriptTrader

   - Portfolio Strategy: PortfolioStrategy_StrategyName

 - Local Code: Contract code with exchange suffix (vt_symbol)

 - Opening Position: Position of the contract in the investment portfolio at yesterday's close (today's open)

 - Current Position: Result of opening position plus today's trade quantity (long trades - short trades)

 - Trading P&L: All trades today, P&L mapped to current latest price at execution price

 - Position P&L: Portfolio opening position, P&L mapped to current latest price at yesterday's closing price

 - Total P&L: Sum of trading P&L and position P&L

 - Long Trades: Today's buy open and buy close trade quantity of the contract in the investment portfolio

 - Short Trades: Today's sell open and sell close trade quantity of the contract in the investment portfolio

Among them, the calculation method of TradingPnl and HoldingPnl adopts the Marking to Market algorithm used by futures exchanges for daily settlement. The calculation process is as shown below:

 - Trading P&L = Position Quantity * (Closing Price - Yesterday's Closing Price) * Contract Size

 - Position P&L = Position Change Quantity * (Closing Price - Opening Execution Price) * Contract Size

 - Total P&L = Trading P&L + Position P&L

 - Net P&L = Total P&L - Total Commission - Total Slippage

Users can view information by expanding and collapsing investment portfolios and adjusting column widths:

 - Click the arrow on the left side of each investment portfolio to expand and collapse the information of each investment portfolio;

 - Click the [Expand All] and [Collapse All] buttons at the top to batch operate on all investment portfolios;

 - Click the [Adjust Column Width] button to automatically adjust the width of each column in the table.

## Trade Record Table

The right part of the interface displays all trade records. Click the dropdown box in the upper right corner to filter by investment portfolio, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_manager/8.png)


## Refresh Frequency

Portfolio P&L is calculated automatically based on timed logic. The calculation frequency can be adjusted through the option box in the middle of the top, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/portfolio_manager/5.png)


Please note that all portfolio position data will be written to cache files when closing VeighNa Trader, so do not kill the process directly to exit, as data will be lost.

During next-day loading, the program will automatically settle yesterday's total position to yesterday's position data field. This logic may not be suitable for markets trading 24 hours a day (foreign futures). Subsequent consideration will be given to adding daily timed settlement or manual settlement functions.

If you find position record errors, or strategies have been removed, you can manually modify the cache file and then restart VeighNa Trader.

The default path for cache files on Windows systems is located at:

    C:\Users\Administrator\.vntrader\portfolio_manager_data.json

Where Administrator is the username of the current Windows system.
