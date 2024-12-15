# CtaBacktester - CTA Backtesting Research Module

## Function Introduction

CtaBacktester is a functional module for **CTA backtesting research**. Users can easily complete tasks such as data download, historical backtesting, result analysis, and parameter optimization through its UI interface.

## Load and Start

### VeighNa Station Load

After starting and logging into VeighNa Station, click the 【Trading】 button, and check the 【CtaBacktester】 in the 【Application Module】 column in the configuration dialog.

### Script Load

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_ctabacktester import CtaBacktesterApp

# Write after creating the main_engine object
main_engine.add_app(CtaBacktesterApp)
```


## Start Module

For strategies developed by users, they need to be placed in the **strategies** directory under the runtime directory of VeighNa Trader to be recognized and loaded. The specific runtime directory path can be viewed in the title bar at the top of the main interface of VeighNa Trader.

For users who have installed on Windows by default, the path of the strategies directory is usually:

```
C:\Users\Administrator\strategies
```

Where Administrator is the system username currently logged in to Windows.

After starting VeighNa Trader, click on the menu bar 【Function】-> 【CTA Backtesting】, or click on the icon on the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/00.png)

You can open the graphical backtesting interface, as shown in the following figure:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/25.png)


## Download Data

Before starting the strategy backtesting, it is necessary to ensure that there is enough historical data in the database. The CtaBacktester module also provides a one-click download of historical data.

To download data, you need to fill in four fields: local code, K-line period, start date, and end date:

<span id="jump">

- Local code
  - The format is contract code + exchange name
  - Such as IF888.CFFEX, rb2105.SHFE
- K-line period:
  - 1m (1-minute K-line)
  - 1h (1-hour K-line)
  - d (daily K-line)
  - w (weekly K-line)
  - tick (one Tick)
- Start and end date
  - The format is yyyy/mm/dd
  - Such as 2018/2/25, 2021/2/28

</span>

After filling in, click the 【Download Data】 button below to start the download task. After successful download, it will be displayed as shown in the following figure:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/27.png)

Note that after the historical data is downloaded, it will be saved in the local database. It can be used directly for subsequent backtesting without the need to download it repeatedly each time.

### Data Source: Data Service (Futures, Stocks, Options)

Taking RQData as an example, [RQData](https://www.ricequant.com/welcome/purchase?utm_source=vnpy) provides historical data for domestic futures, stocks, and options. Before using it, make sure that the data service is correctly configured (the configuration method is detailed in the basic usage section of the global configuration). When opening CtaBacktester, the data service login initialization will be automatically executed. If successful, the log will output "Data service initialization successful", as shown in the following figure:

 ![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/26.png)

### Data Source: IB (Foreign Futures, Stocks, Spot, etc.)

Interactive Brokers (IB) provides rich historical data download for foreign markets (including stocks, futures, options, spot, etc.). Note that before downloading, you need to start the IB TWS trading software, and connect the IB interface and subscribe to the required contract market data on the main interface of VeighNa Trader. After successful download, it will be displayed as shown in the following figure:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/28.png)


## Execute Backtesting

After preparing the data, you can start using historical data to backtest the strategy. When backtesting, you need to configure the relevant parameters:

- Strategy variety
  - Trading strategy: Select the strategy name to be backtested in the drop-down box;
  - Local code: Pay attention to not miss the exchange suffix;
- Data range
  - The format is detailed in the [Download Data](#jump) section of this chapter;
- Trading cost
  - Slippage: The difference between the order trading point and the actual trading point;
  - Percentage commission: Fill in the number, do not fill in the percentage;
  - Fixed commission: You can fill in the commission as 0, and then add the commission divided by the contract multiplier to the slippage;
- Contract attributes
  - Contract multiplier: The trading unit of the contract;
  - Price movement: The minimum price change of the contract;
  - Backtesting capital: Account capital;
  - Contract mode: Forward.

After the configuration is completed, click the 【Start Backtesting】 button below, and a strategy parameter configuration dialog will pop up, as shown in the following figure:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/29.png)

After clicking the 【OK】 button, the backtesting task will start, and the log interface will output relevant information, as shown in the following figure:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/10.png)

After the backtesting is completed, the statistical indicators of the strategy backtesting performance and related charts will be automatically displayed in the right area, as shown in the following figure:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/30.png)

If the required historical data is not ready in the database and you click the 【Start Backtesting】 button, the log interface will output the log "Insufficient historical data, backtesting terminated", as shown in the following figure:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/15.png)


## Result Analysis

### Performance Charts

The performance chart on the right consists of the following four sub-charts:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/31.png)

The horizontal axis of the 【Account Net Worth】 chart is time, and the vertical axis is capital, reflecting the situation of the account net worth changing with the trading day during the trading period.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/32.png)

The horizontal axis of the 【Net Worth Drawdown】 chart is time, and the vertical axis is the drawdown, reflecting the degree of drawdown of the net worth from the recent high point changing with the trading day.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/33.png)

The horizontal axis of the 【Daily Profit and Loss】 chart is time, and the vertical axis is the amount of daily profit and loss (settled at the closing price according to the daily mark-to-market rule), reflecting the daily profit and loss change of the strategy during the entire backtesting period.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/34.png)

The horizontal axis of the 【Profit and Loss Distribution】 chart is the numerical value of the daily profit and loss, and the vertical axis is the probability of the occurrence of this profit and loss value, reflecting the probability distribution of the overall daily profit and loss.

### Statistical Indicators

The statistical indicator area is used to display the relevant statistical values of the historical backtesting performance of the strategy, as shown in the following figure:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/35.png)

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/36.png)

According to the data type, the indicators can be classified as:

- Date information
  - First trading day
  - Last trading day
  - Total trading days
  - Profitable trading days
  - Losing trading days
- Capital profit and loss
  - Initial capital
  - Final capital
  - Total return
  - Annualized return
  - Maximum drawdown
  - Percentage maximum drawdown
  - Total profit and loss
- Trading cost
  - Total commission
  - Total slippage
  - Total turnover
  - Total number of transactions
- Daily average data
  - Daily average profit and loss
  - Daily average commission
  - Daily average slippage
  - Daily average turnover
  - Daily average number of transactions
  - Daily average return
  - Return standard deviation (daily average)
- Performance evaluation
  - Sharpe ratio
  - Return drawdown ratio

### Detailed Information

After the backtesting is completed, you can click the 【Order Record】 button in the left area to view the detailed information of the strategy's order during the backtesting process:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/43.png)

If you find that the table content is not displayed completely, you can click the right mouse button to pop up the menu, and select the 【Adjust Column Width】 button, and the table will automatically adjust the column width:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/46.png)

The table also supports one-click saving the data in the table as a CSV file. In the menu popped up in the previous step, click the 【Save Data】 button, and a dialog for selecting the file name to be saved will pop up, as shown in the following figure:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/42.png)

The **execution price** of the order issued by the strategy during the backtesting process is not necessarily the original order price. It needs to be matched by the backtesting engine based on the market data at that time and the order price. The specific execution details of each order can be viewed by clicking the 【Execution Record】 button:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/38.png)

After clicking the 【Daily Profit and Loss】 button, you can see the detailed daily profit and loss of the strategy, as shown in the following figure:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/39.png)

The daily profit and loss statistics here are calculated using the widely used daily mark-to-market (Marking-to-Market) rule in the futures market:

- Position profit and loss: The part of the position held at the opening today, opened at the closing price yesterday, closed at the closing price today, and the calculated profit and loss amount;
- Trading profit and loss: The part of the intraday trading today, opened at the trading price, closed at the closing price today, and the calculated profit and loss amount;
- Total profit and loss: The amount of the position profit and loss and the trading profit and loss after summarization;
- Net profit and loss: The amount of the total profit and loss minus the commission and slippage, and it is also the daily profit and loss amount used in the final calculation and display of the four charts.

### K-line Chart

Click the 【K-line Chart】 button, and you can open the chart that displays the backtesting K-line data and the specific buy and sell positions of the strategy, as shown in the following figure:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/44.png)

Note that the drawing of the chart may take some time (usually from tens of seconds to a few minutes), please be patient.

The legend explanation in the K-line chart can be seen at the bottom of the window, and the overall color and style of the chart use the standard of the domestic market. The line between opening and closing is drawn using the first-in, first-out (FIFO) rule, and each transaction will be automatically matched with other transactions according to its quantity, even if the strategy has complex adding and reducing positions, it can be correctly drawn.

## Parameter Optimization

For a developed strategy, you can use the built-in optimization algorithm of CtaBacktester to quickly perform parameter optimization. Currently, it supports two optimization algorithms: exhaustive and genetic.

### Set Optimization Parameters

Click the 【Parameter Optimization】 button, and a window for "Optimization Parameter Configuration" will pop up:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/37.png)

Click the 【Objective】 drop-down box, and select the objective function to be used during the optimization process (that is, the objective is to maximize this value):

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/45.png)

For the strategy parameters to be optimized, you need to configure:

- 【Start】 and 【End】: Used to specify the range of parameter optimization;
- 【Step】: Used to specify the value of each change of the parameter;

For example: If the 【Start】 of a parameter is set to 10, the 【End】 is set to 20, and the 【Step】 is set to 2, then the optimization space of this parameter during the optimization process is: 10, 12, 14, 16, 18, 20.

For strategy parameters that need to be set to a fixed value, just set both the 【Start】 and 【End】 to the same value.

### Exhaustive Algorithm Optimization

After setting the parameters to be optimized, click the 【Multi-Process Optimization】 button at the bottom of the window. At this time, CtaBacktester will call the Python multiprocessing module, and start the corresponding number of processes to execute the exhaustive optimization task in parallel according to the number of CPU cores of the current computer.

During the optimization process, the exhaustive algorithm will traverse every combination in the parameter optimization space. The process of traversal is to run the historical backtesting with this combination as the strategy parameter, and return the value of the optimization objective function. After the traversal is completed, the results will be sorted according to the value of the optimization objective function, and the best parameter combination result will be selected.

The efficiency of the exhaustive algorithm optimization is directly related to the number of CPU cores: If the user's computer is 2 cores, the optimization time is 1/2 of the single core; If the computer is 10 cores, the optimization time will be greatly reduced to 1/10 of the single core.

### Genetic Algorithm Optimization

After setting the parameters to be optimized, click the 【Genetic Algorithm Optimization】 button at the bottom of the window. At this time, CtaBacktester will call the Python multiprocessing module and the deap module to execute the efficient and intelligent multi-process genetic algorithm optimization task.

Here is a brief working principle of the genetic algorithm:

1. Define the optimization direction, such as maximizing the total return;
2. Randomly select a part of the parameter combinations from the global optimization space to form the initial population;
3. Evaluate all individuals in the population, that is, run the backtesting to get the value of the optimization objective function;
4. Sort based on the value of the optimization objective function, and remove the individuals (parameter combinations) with poor performance;
5. Cross or mutate the remaining individuals, and form a new population through evaluation and screening;
6. The above 3-5 steps form a complete population iteration, and need to be repeated multiple times in the entire optimization process;
7. After multiple iterations, the diversity within the population decreases, the parameters converge to the optimal solution, and the final output result is obtained.

### Optimization Result Analysis

After the optimization is completed, information prompts will be output in the log area:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/49.png)

At this time, click the 【Optimization Result】 button to view the relevant results:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/50.png)

The parameter optimization results in the above figure are sorted from high to low based on the value of the optimization objective function selected when starting the optimization task.

Finally, click the 【Save】 button in the lower right corner to save the optimization results to a local CSV file, which is convenient for subsequent analysis and use.


## Strategy Code

### Code Editing

If you need to modify the strategy, select the strategy in the drop-down box in the upper left corner of the CtaBacktester interface, and click the 【Code Editing】 button in the lower left corner to automatically open Visual Studio Code for code editing. If Visual Studio Code is not found, a dialog box will pop up, indicating that the code editor startup failed, as shown in the following figure:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/61.png)

### Strategy Reload

When a user modifies the source code of the strategy through CtaBacktester, the modification is still at the level of the code file on the hard disk, and the original strategy code is still in the memory.

If you want the modified content to take effect immediately in the memory, you need to click the 【Strategy Reload】 button in the lower left corner. At this time, CtaBacktester will automatically scan and reload the strategy code in all strategy files, and there will be relevant log output, as shown in the following figure:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/cta_backtester/59.png)

After the reload is completed, when you run the backtesting or optimization again, the modified strategy code will be used.
