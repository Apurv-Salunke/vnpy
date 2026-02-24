# CtaBacktester - CTA Backtesting Research Module

## Function Overview

CtaBacktester is a functional module for **CTA backtesting research**. Users can conveniently complete tasks such as data downloading, historical backtesting, result analysis, and parameter optimization through its UI interface.

## Loading and Launching

### Loading via VeighNa Station

After launching and logging into VeighNa Station, click the [Trading] button. In the configuration dialog, check [CtaBacktester] in the [Application Module] section.

### Loading via Script

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_ctabacktester import CtaBacktesterApp

# Write after creating the main_engine object
main_engine.add_app(CtaBacktesterApp)
```


## Starting the Module

For user-developed strategies, they need to be placed in the **strategies** directory under the VeighNa Trader runtime directory to be recognized and loaded. The specific runtime directory path can be viewed in the title bar at the top of the VeighNa Trader main interface.

For users with default installation on Windows, the strategies directory path for placing strategies is usually:

```
C:\Users\Administrator\strategies
```

Where Administrator is the system username currently logged into Windows.

After launching VeighNa Trader, click [Function] -> [CTA Backtesting] in the menu bar, or click the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/00.png)

You can then open the graphical backtesting interface, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/25.png)


## Downloading Data

Before starting strategy backtesting, you first need to ensure there is sufficient historical data in the database. The CtaBacktester module also provides one-click historical data downloading functionality.

To download data, you need to fill in four fields: local code, K-line period, start date, and end date:

<span id="jump">

- Local Code
  - Format is contract code + exchange name
  - Such as IF888.CFFEX, rb2105.SHFE
- K-line Period:
  - 1m (1-minute K-line)
  - 1h (1-hour K-line)
  - d (daily K-line)
  - w (weekly K-line)
  - tick (one Tick)
- Start and End Dates
  - Format is yyyy/mm/dd
  - Such as 2018/2/25, 2021/2/28

</span>

After filling in, click the [Download Data] button below to start the download task. After success, it is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/27.png)

Note that historical data after download completion will be saved in the local database and can be used directly in subsequent backtesting without repeated downloads.

### Data Source: Data Services (Futures, Stocks, Options)

Taking RQData as an example, [RQData](https://www.ricequant.com/welcome/purchase?utm_source=vnpy) provides historical data for domestic futures, stocks, and options. Before use, ensure the data service is correctly configured (for configuration methods, see the Global Configuration section in the Basic Usage chapter). When opening CtaBacktester, data service login initialization is automatically executed. If successful, "Data service initialization successful" log will be output, as shown in the figure below:

 ![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/26.png)

### Data Source: IB (Foreign Futures, Stocks, Spot, etc.)

Interactive Brokers (IB) provides rich historical data downloads for foreign markets (including stocks, futures, options, spot, etc.). Note that before downloading, you need to start the IB TWS trading software first, connect the IB interface on the VeighNa Trader main interface, and subscribe to the required contract market data. Successful download is shown as below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/28.png)


## Executing Backtesting

After preparing the data, you can start using historical data for strategy backtesting research. When backtesting, you need to configure relevant parameters:

- Strategy Variety
  - Trading Strategy: Select the strategy name to backtest from the dropdown box;
  - Local Code: Note not to omit the exchange suffix;
- Data Range
  - Format details are in the [Downloading Data](#jump) section of this chapter;
- Trading Costs
  - Slippage: Difference between order execution price and actual trading price;
  - Percentage Commission: Fill in numbers only, do not fill in percentages;
  - Fixed Commission: You can set commission to 0, then divide the commission by the contract multiplier and add it to slippage;
- Contract Attributes
  - Contract Multiplier: Contract trading unit;
  - Price Tick: Minimum price movement of the contract;
  - Backtesting Capital: Account capital;
  - Contract Mode: Forward.

After configuration, click the [Start Backtesting] button below. A strategy parameter configuration dialog will pop up for setting strategy parameters, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/29.png)

After clicking the [OK] button, the backtesting task starts executing, and the log interface will output relevant information, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/10.png)

After backtesting is completed, the strategy backtesting performance statistics and related charts will be automatically displayed in the right area, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/30.png)

If you click [Start Backtesting] without preparing the required historical data in the database, the log interface will output "Insufficient historical data, backtesting terminated" log, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/15.png)


## Result Analysis

### Performance Charts

The performance charts on the right consist of the following four sub-charts:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/31.png)

[Account Net Value] chart: The horizontal axis is time, the vertical axis is capital, reflecting the account net value changes with trading days during the trading period.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/32.png)

[Net Value Drawdown] chart: The horizontal axis is time, the vertical axis is drawdown, reflecting the degree of net value drawdown from recent highs as trading days change.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/33.png)

[Daily P&L] chart: The horizontal axis is time, the vertical axis is the daily P&L amount (using Mark-to-Market rules for settlement at closing price), reflecting the daily P&L changes of the strategy throughout the backtesting period.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/34.png)

[P&L Distribution] chart: The horizontal axis is the daily P&L value, the vertical axis is the probability of that P&L value occurring, reflecting the overall probability distribution of daily P&L.

### Statistical Indicators

The statistical indicators area displays relevant statistical values for strategy historical backtesting performance, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/35.png)

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/36.png)

According to data type, indicators can be classified as:

- Date Information
  - First Trading Day
  - Last Trading Day
  - Total Trading Days
  - Profitable Trading Days
  - Losing Trading Days
- Capital P&L
  - Starting Capital
  - Ending Capital
  - Total Return
  - Annualized Return
  - Maximum Drawdown
  - Percentage Maximum Drawdown
  - Total P&L
- Trading Costs
  - Total Commission
  - Total Slippage
  - Total Turnover
  - Total Number of Trades
- Daily Average Data
  - Daily Average P&L
  - Daily Average Commission
  - Daily Average Slippage
  - Daily Average Turnover
  - Daily Average Number of Trades
  - Daily Average Return
  - Return Standard Deviation (Daily)
- Performance Evaluation
  - Sharpe Ratio
  - Return-Drawdown Ratio

### Detailed Information

After backtesting is completed, you can click the [Order Record] button in the left area to view the details of each order placed by the strategy during backtesting:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/43.png)

If you find the table content is incomplete, you can right-click to pop up the menu and select the [Adjust Column Width] button for automatic column width scaling:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/46.png)

The table also supports one-click saving of table data as CSV files. In the right-click menu from the previous step, click the [Save Data] button to pop up a dialog for selecting the file name to save, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/42.png)

The **execution price** of strategy orders during backtesting is not necessarily the original order price, but is calculated by the backtesting engine based on market data and order price at that time. You can click the [Trade Record] button to view specific execution details for each order:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/38.png)

After clicking the [Daily P&L] button, you can see the strategy's daily P&L details as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/39.png)

The daily P&L statistics here are calculated using the Marking-to-Market rules commonly used in the futures market:

- Position P&L: For positions held at today's open, calculate P&L by opening at yesterday's closing price and closing at today's closing price;
- Trading P&L: For positions traded during the day, calculate P&L by opening at execution price and closing at today's closing price;
- Total P&L: Sum of position P&L and trading P&L;
- Net P&L: Total P&L minus commission and slippage, which is also the daily P&L amount used when calculating and displaying the four charts.

### K-line Charts

Click the [K-line Chart] button to open a chart for displaying backtesting K-line data and the strategy's specific buy/sell points, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/44.png)

Note that drawing may take some time (usually from tens of seconds to several minutes), please wait patiently.

The legend for the K-line chart can be seen at the bottom of the window. Overall, it adopts the standard color scheme and style of the domestic market. The connection line between open and close positions is drawn using First-in, First-out (FIFO) rules. Each trade is automatically matched with other trades based on its quantity, so even if the strategy has complex position adjustment operations, it can be drawn correctly.


## Parameter Optimization

For developed strategies, you can use the built-in optimization algorithms in CtaBacktester to quickly perform parameter optimization. Currently, it supports exhaustive and genetic optimization algorithms.

### Setting Optimization Parameters

Click the [Parameter Optimization] button to pop up the "Optimization Parameter Configuration" window:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/37.png)

Click the [Target] dropdown box to select the objective function to use during optimization (i.e., optimize with the goal of maximizing this value):

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/45.png)

For strategy parameters to be optimized, you need to configure:

- [Start] and [End]: Used to define the parameter optimization range;
- [Step]: Used to define the numerical change for each parameter iteration;

Example: If a parameter's [Start] is set to 10, [End] is set to 20, and [Step] is set to 2, then the optimization space for this parameter during optimization is: 10, 12, 14, 16, 18, 20.

For strategy parameters to be set to fixed values, please set both [Start] and [End] to the same value.

### Exhaustive Algorithm Optimization

After setting the parameters to be optimized, click the [Multi-process Optimization] button at the bottom of the window. At this time, CtaBacktester will call Python's multiprocessing module and start the corresponding number of processes based on the current computer's CPU core count to execute exhaustive optimization tasks in parallel.

During optimization, the exhaustive algorithm will traverse every combination in the parameter optimization space. The traversal process uses each combination as strategy parameters to run a historical backtest once and return the optimization objective function value. After completing the traversal, sorting is performed based on all objective function values to select the optimal parameter combination result.

The efficiency of exhaustive algorithm optimization is directly related to CPU core count: if the user's computer has 2 cores, the optimization time is 1/2 of a single core; if the computer has 10 cores, the optimization time will be significantly reduced to 1/10 of a single core.

### Genetic Algorithm Optimization

After setting the parameters to be optimized, click the [Genetic Algorithm Optimization] button at the bottom of the window. At this time, CtaBacktester will call Python's multiprocessing module and deap module to execute efficient and intelligent multi-process genetic algorithm optimization tasks.

Attached is a brief working principle of the genetic algorithm:

1. Define the optimization direction, such as maximizing total return;
2. Randomly select some parameter combinations from the global optimization space to form the initial population;
3. Evaluate all individuals in the population, i.e., run backtesting to obtain objective function results;
4. Sort based on objective function results and eliminate poorly performing individuals (parameter combinations);
5. Crossover or mutate the remaining individuals, and form a new population after evaluation and screening;
6. Steps 3-5 above constitute one complete population iteration, which needs to be repeated multiple times throughout the optimization process;
7. After multiple iterations, population diversity decreases, parameters converge to the optimal solution, and finally output results.

### Optimization Result Analysis

After optimization is completed, information will be output in the log area:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/49.png)

At this time, click the [Optimization Result] button to view related results:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/50.png)

The parameter optimization results in the figure above are sorted from high to low based on the value of the objective function [Total Return] selected when starting the optimization task.

Finally, click the [Save] button in the lower right corner to save the optimization results to a local CSV file for subsequent analysis.


## Strategy Code

### Code Editing

If you need to modify the strategy, select the strategy from the dropdown box in the upper left corner of the CtaBacktester interface and click the [Code Editing] button in the lower left corner to automatically open Visual Studio Code for code editing. If Visual Studio Code cannot be found, a dialog indicating code editor launch failure will pop up, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/61.png)

### Strategy Reload

When users modify the strategy source code through CtaBacktester, the modifications remain at the code file level on the hard disk, while the memory still contains the strategy code before modification.

To make the modifications take effect immediately in memory, you need to click the [Strategy Reload] button in the lower left corner. At this time, CtaBacktester will automatically scan and reload all strategy code from strategy files, and relevant logs will be output, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/59.png)

After the reload refresh is completed, when running backtesting or optimization again, the modified strategy code will be used.
