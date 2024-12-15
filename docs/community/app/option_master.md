# OptionMaster - Options Volatility Trading Module

## Function Introduction

OptionMaster is a functional module for **options volatility trading**. Users can use OptionMaster to complete real-time pricing of options, tracking of volatility surfaces, monitoring of position Greeks, portfolio stress testing, automatic trading of electronic eyes, etc.


## Load and Start

### VeighNa Station Load

After starting and logging into VeighNa Station, click the **Trading** button, and check the **OptionMaster** in the **Application Module** column in the configuration dialog.

### Script Load

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_optionmaster import OptionMasterApp

# Write after creating the main_engine object
main_engine.add_app(OptionMasterApp)
```


## Start Module

After starting VeighNa Trader, click **Function** -> **Options Trading** in the menu bar, or click the icon on the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/1.png)

You can enter the OptionMaster management interface (hereinafter referred to as the management interface), as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/2.png)


## Configure Portfolio

On the management interface, select the options products to be traded, and click the **Configure** button to open the portfolio configuration dialog as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/3.png)


The configuration parameters are as follows:

* Pricing Model
  * Black-76 model: for European futures options (stock index options);
  * Black-Scholes model: for European stock options (ETF options);
  * Binomial-Tree model: for American futures options (commodity options);
* Annualized Interest Rate
  * Risk-free discount rate used in the pricing model;
* Contract Mode
  * Positive: including ETF options, futures options, stock index options and most other products;
* Greeks Decimal Places
  * The number of decimal places to be retained when displaying the Greek values;
* Pricing Underlying Asset for Option Chain
  * Note that only the option chain of the underlying asset is selected, it will be added to the trading portfolio;
  * Pricing underlying asset support
    * Futures contract: the futures price provided by the exchange itself;
    * Synthetic futures: the synthetic futures price calculated based on the option price;
    * OptionMaster will automatically adjust the underlying asset price relative to the option chain during the pricing calculation process, so it is recommended to select the most active contract as the underlying asset.

Click the **Confirm** button at the bottom to complete the initialization of the options portfolio. At this time, the **Configure** button on the management interface will be locked, while the other buttons will be activated.


## Market Monitoring

Click the **T-type Quote** button on the management interface to open the T-type quote window:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/4.png)

The window is divided into left and right areas, with the middle white column as the strike price, the left side as the call option, and the right side as the put option.

Each row displays the information corresponding to a certain strike price option, and the information displayed from the outside to the inside includes:

* Contract Code
* Real-time cash Greeks of the option
  * Vega
  * Theta
  * Gamma
  * Delta
* Trading Information
  * Position
  * Volume
* 1st Level Market Information
  * Buy Implied Volatility
  * Buy Volume
  * Buy Price
  * Sell Price
  * Sell Volume
  * Sell Implied Volatility
* Net Position


## Quick Trading

Click the **Quick Trading** button on the management interface to open the manual order window:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/5.png)

The overall usage method is similar to the trading component of VeighNa Trader's main interface. After entering the contract code, buying and selling direction, opening and closing direction, trading price and quantity, click the **Order** button to place a limit order, and click the **Cancel All** button to cancel all active orders at once.

Double-click the cell of a certain option in the T-type quote, and you can quickly fill in the **Code** edit box of this window.


## Position Greeks Monitoring

Click the **Position Greeks** button on the management interface to open the Greeks risk monitoring window:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/16.png)

The monitoring information in the window is divided into four dimensions:

* Trading Portfolio (including all subordinate option chains and underlying asset summary data)
* Underlying Asset Contract
* Option Chain (including all subordinate option summary data)
* Option Contract

The monitoring information of each dimension includes:

* Position-related
  * Long Position: current long position
  * Short Position: current short position
  * Net Position: Long Position - Short Position
* Total Greeks
  * Delta: the amount of profit and loss corresponding to a 1% rise or fall in the underlying price
  * Gamma: the change in Delta corresponding to a 1% rise or fall in the underlying price
  * Theta: the amount of profit and loss of this dimension for each trading day
  * Vega: the amount of profit and loss of this dimension corresponding to a 1% rise or fall in the implied volatility

## Premium Monitoring

Click the **Premium Monitoring** button on the management interface to open the premium calibration amplitude monitoring window of the option chain pricing:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/6.png)

Taking the above figure as an example, you can see:

* IO2104, priced according to the corresponding month futures IF2104, the premium is close to 0;
* IO2105, IO2106, IO2109, priced according to the active contract IF2104, the premium increases in turn;
* IO2112, IO2203, priced according to the synthetic futures of the corresponding month, the premium is 0.


## Volatility Curve

Click the **Volatility Curve** button on the management interface to open the current market volatility curve monitoring chart:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/7.png)

The volatility curve of each option chain is displayed in different colors, and the specific color corresponds to the legend of the option chain on the left.

Each option chain will include three curves:

* Upward Arrow: the 1st level market implied volatility median of the call option in that month, that is, the average of the implied volatility of the buy 1 price and the sell 1 price;
* Downward Arrow: the 1st level market implied volatility median of the put option in that month;
* Small Circle: the numerical value of the pricing volatility of that month, the pricing volatility is used for Greeks calculation and electronic eye trading, and is set through the **Volatility Management** component behind.

The curves displayed in the chart are controlled by the check boxes corresponding to each option chain at the top of the window, and can be adjusted according to the needs. For example, only the IO2109 option chain is displayed in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/17.png)


## Delta Hedging

Click the **Delta Hedging** button on the management interface to open the automatic Delta hedging function of the trading portfolio:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/8.png)

* Hedging Underlying: You can choose any underlying asset contract in the portfolio;
* Execution Frequency: How often to check, to determine whether to execute the hedging;
* Delta Target: If the hedging is triggered, the Delta value will be hedged to how much;
  * Choose 0, that is, to maintain the overall Delta neutrality of the portfolio;
  * Choose a positive number, that is, to maintain the overall Delta long position of the portfolio;
  * Choose a negative number, that is, to maintain the overall Delta short position of the portfolio;
* Delta Range: When the Delta value of the position type deviates from the above Delta target by more than how much, trigger the hedging task;
* Order Price: When sending a hedging order, the price relative to the opposite side of the market;

Click the **Start** button to start the automatic hedging function. When the countdown reaches the execution interval, a check will be performed. If the conditions are met, the TWAP algorithm will be started to execute the hedging operation.

Click the **Stop** button to stop the operation of the automatic hedging function.

## Scenario Analysis

Click the **Scenario Analysis** button on the management interface to open the stress testing and scenario analysis function of the overall position risk of the trading portfolio:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/9.png)

First, configure the analysis task to be executed:

* Target Data: Support profit and loss, Delta, Gamma, Theta, Vega;
* Time Decay: The number of trading days to decay;
* Price Change:
  * The range of price rise and fall in the analysis;
  * Assuming the current price is 100, the change is 10%, then the range is 90~110;
* Volatility Change:
  * The range of volatility rise and fall in the analysis;
  * Assuming the current volatility is 20%, the change is 10%, then the range is 10%~30%.

After clicking the **Execute Analysis** button, the stress testing engine will calculate the corresponding target data based on the current trading portfolio position, and the price and implied volatility situation under each scenario, and draw the result as a 3D surface.

The figure below shows the result of using Gamma value as the calculation target, 10% price change, and 15% volatility change:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/18.png)

The vertical axis in this 3D chart is the numerical value of the calculation target, and the two horizontal axes are the numerical values of the price and volatility changes.


## Volatility Management

Click the **Volatility Management** button on the management interface to open the pricing volatility management interface:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/11.png)

Click the top option chain label to switch to the corresponding option chain pricing volatility management component. The first time you open it, the **Pricing Implied Volatility** values in the table below are all 0.

First, initialize the pricing curve. Click the **Reset** button at the top to map the median implied volatility of the out-of-the-money options at the current strike price to the pricing implied volatility.

After mapping, you can check the current shape of the pricing volatility curve in the volatility chart. If there is any non-smooth situation in the pricing implied volatility of the out-of-the-money options at the current strike price compared to the overall curve, you can fit it based on the pricing implied volatility of the out-of-the-money options at the relatively smooth strike price.

In the **Execute Fitting** column of the component table, check the check boxes of the out-of-the-money options at the current strike price that you want to fit, and click the **Fit** button at the top to fit the volatility curve based on the Cubic Spline (trinomial interpolation) algorithm built into OptionMaster.

After the fitting is completed, if there are still unsatisfactory parts, you can manually adjust them through the scrolling box in the **Pricing Implied Volatility** column, click the up and down arrows to increase or decrease by 0.1% each time, or you can also directly enter the value you want to modify.

When the overall view of the volatility curve needs to be shifted due to high and low, you can use the **+0.1%** and **-0.1%** buttons at the top of the component to shift and adjust the pricing volatility of all the strike prices.

## Electronic Eye

Click the **Electronic Eye** button on the management interface to open the automatic arbitrage algorithm function of the trading portfolio:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/12.png)

The electronic eye algorithm can automatically capture the transient trading opportunities in the market within the allowed position range based on the preset pricing volatility curve of the trader, and at the same time, it can ensure the overall Delta neutrality of the trading portfolio by combining with the automatic Delta hedging function.

The electronic eye interface is similar to the T-type quote, divided into left and right areas, with the middle white as the strike price, the left side as the call option, and the right side as the put option. Each option has an independent electronic eye trading algorithm, and the trader can start hundreds of trading algorithms at the same time (the specific number depends on the CPU performance) without interfering with each other.

The configuration parameters of each electronic eye algorithm include:

* Trading Spread Related
  * Price Spread
  * Volatility Spread
* Position Limit Related
  * Position Range
  * Target Position
* Maximum Order
  * The maximum number of orders per transaction
* Direction
  * The trading direction allowed by the algorithm
  * Including only long, only short, and both long and short trading

The execution process of the electronic eye algorithm is as follows:

1. Calculate the **Theoretical Price** of the option based on the pricing volatility.
2. Calculate the spread of the target buy and sell:
   1. The price value of the volatility spread = the volatility spread * the theoretical Vega value of the option
   2. The trading spread = max(price spread, the price value of the volatility spread)
3. Calculate the target buy and sell price:
   1. The target buy price = theoretical price - trading spread / 2
   2. The target sell price = theoretical price + trading spread / 2
4. Taking the long trade as an example, when the sell 1 price of the market is lower than the target buy price, the buy signal is triggered
5. Calculate the order quantity for this round:
   1. The maximum long position limit of the algorithm = target position + position range
   2. The remaining long position tradable quantity = maximum long position limit of the algorithm - current net position
   3. The order quantity for this round = min(remaining long position tradable quantity, sell 1 volume, maximum order quantity)
6. Use the target buy price and the order quantity for this round to place the corresponding trading order

After configuring the algorithm parameters, click the **Pricing** button in the **Pricing** column of this row to start the algorithm's pricing calculation, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/13.png)

The status display of the **Pricing** and **Trading** buttons:

* When it is N, it means that the algorithm is currently not performing this task
* When it is Y, it means that the algorithm is already performing the corresponding task

Starting the pricing calculation of the 4 option algorithms will start to update the target buy and sell prices and other related values in real time.

At this time, click the **Trading** button in the **Trading** column of this row to start the algorithm's trading execution. When the price and position meet the conditions, the trading order will be automatically placed. You can monitor the detailed running status log information through the right log area:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/14.png)

When you need to make batch modifications to the algorithm configuration, you can use the global modification function in the upper right corner of the electronic eye window, which is more convenient and efficient.
