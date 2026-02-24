# OptionMaster - Option Volatility Trading Module

## Function Overview

OptionMaster is a functional module for **option volatility trading**. Users can complete functions such as option real-time pricing, volatility surface tracking, position Greek value monitoring, portfolio stress testing, and electronic eye automatic trading through OptionMaster.


## Loading and Launching

### Loading via VeighNa Station

After launching and logging into VeighNa Station, click the [Trading] button. In the configuration dialog, check [OptionMaster] in the [Application Module] section.

### Loading via Script

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_optionmaster import OptionMasterApp

# Write after creating the main_engine object
main_engine.add_app(OptionMasterApp)
```


## Starting the Module

After launching VeighNa Trader, click [Function] -> [Option Trading] in the menu bar, or click the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/1.png)

You can then enter the OptionMaster management interface (hereinafter referred to as the management interface), as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/2.png)


## Configuring Portfolio

On the management interface, select the option product to trade and click the [Configure] button to open the portfolio configuration dialog as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/3.png)


Configuration parameters are as follows:

* Pricing Model
  * Black-76 Model: For European futures options (stock index options);
  * Black-Scholes Model: For European stock options (ETF options);
  * Binomial-Tree Model: For American futures options (commodity options);
* Annual Interest Rate
  * Risk-free discount rate used in the pricing model;
* Contract Mode
  * Forward: Includes most products such as ETF options, futures options, stock index options, etc.;
* Greeks Decimal Places
  * Number of decimal places retained when displaying Greek values;
* Pricing Underlying for Option Chain
  * Note that only option chains with underlying selected will be added to the trading portfolio;
  * Pricing underlying supports
    * Futures Contracts: Futures prices provided by the exchange itself;
    * Synthetic Futures: Synthetic futures prices calculated based on option prices;
    * OptionMaster will automatically adjust the premium/discount of the underlying price relative to the option chain during pricing calculation, so it is recommended to select the most actively traded contract as the underlying.

Click the [Confirm] button at the bottom to complete option portfolio initialization. At this time, the [Configure] button on the management interface will be locked, and other buttons will be activated.


## Market Monitoring

Click the [T-type Quote] button on the management interface to open the T-type quote window:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/4.png)

The window is divided into left and right areas overall, with the middle white column being the strike price, left side being call options, and right side being put options.

Each row displays information corresponding to an option with a certain strike price. From outside to inside, the displayed information includes:

* Contract Code
* Option's real-time cash Greek values
  * Vega
  * Theta
  * Gamma
  * Delta
* Trading Information
  * Open Interest
  * Volume
* Level 1 Order Book Information
  * Bid IV
  * Bid Quantity
  * Bid Price
  * Ask Price
  * Ask Quantity
  * Ask IV
* Net Position


## Quick Trading

Click the [Quick Trading] button on the management interface to open the manual order window:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/5.png)

The overall usage method is similar to the trading component on the VeighNa Trader main interface. After entering the contract code, buy/sell direction, open/close direction, trading price, and quantity, click the [Order] button to send a limit order, or click the [Cancel All] button to cancel all current active orders with one click.

Double-clicking a cell of an option in the T-type quote can quickly fill in the [Code] edit box of this window.


## Position Greek Values

Click the [Position Greek Values] button on the management interface to open the Greek value risk monitoring window:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/16.png)

Monitoring information in the window is divided into four dimensions:

* Trading Portfolio (including all subordinate option chains and underlying aggregated data)
* Underlying Contract
* Option Chain (including all subordinate option aggregated data)
* Option Contract

Monitoring information for each dimension includes:

* Position Related
  * Long: Current long position
  * Short: Current short position
  * Net: Long - Short
* Total Greek Values
  * Delta: P&L amount corresponding to 1% change in underlying price
  * Gamma: Delta change of this dimension corresponding to 1% change in underlying price
  * Theta: P&L amount of this dimension per trading day passed
  * Vega: P&L amount of this dimension corresponding to 1% change in implied volatility

## Premium/Discount Monitoring

Click the [Premium/Discount Monitoring] button on the management interface to open the option chain pricing premium/discount calibration amplitude monitoring window:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/6.png)

Taking the figure above as an example, you can see:

* IO2104, priced with corresponding month futures IF2104, premium/discount is close to 0;
* IO2105, IO2106, IO2109, priced with active contract IF2104, discount increases sequentially;
* IO2112, IO2203, priced with synthetic futures of corresponding months, premium/discount is 0.


## Volatility Curve

Click the [Volatility Curve] button on the management interface to open the current market volatility curve monitoring chart:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/7.png)

The volatility curve of each option chain in the chart is displayed in different colors, with the legend corresponding to the option chain on the left.

Each option chain will include three curves:

* Upward Arrow: Median of level 1 order book implied volatility for call options of that month, i.e., the mean of bid 1 price and ask 1 price volatility;
* Downward Arrow: Median of level 1 order book implied volatility for put options of that month;
* Small Dots: Pricing volatility value for that month, pricing volatility is used for Greek value calculation and electronic eye trading, set through the [Volatility Management] component below.

The curves displayed in the chart are controlled by the checkbox corresponding to each option chain at the top of the window and can be adjusted according to needs, as shown in the figure below which only displays the IO2109 option chain:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/17.png)


## Delta Hedging

Click the [Delta Hedging] button on the management interface to open the portfolio's Delta automatic hedging function:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/8.png)

* Hedging Underlying: You can choose any underlying contract in the investment portfolio;
* Execution Frequency: How often to execute a check to judge whether to execute hedging;
* Delta Target: If hedging is triggered, what value to hedge the Delta to;
  * Select 0, i.e., maintain overall portfolio Delta neutrality;
  * Select a positive number, i.e., maintain overall portfolio Delta long exposure;
  * Select a negative number, i.e., maintain overall portfolio Delta short exposure;
* Delta Range: When the Delta value of the position type deviates from the above Delta target by more than how much, trigger hedging tasks;
* Order Price Improvement: Price improvement relative to the opposite side of the order book when sending hedging orders;

Click the [Start] button to start the automatic hedging function. When the countdown reaches the execution interval, a check will be executed. If conditions are met, the TWAP algorithm will be started to execute hedging operations.

Click the [Stop] button to stop the automatic hedging function from running.

## Scenario Analysis

Click the [Scenario Analysis] button on the management interface to open the portfolio overall position risk stress testing and scenario analysis function:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/9.png)

First configure the analysis tasks to execute:

* Target Data: Supports P&L, Delta, Gamma, Theta, Vega;
* Time Decay: Number of days of trading day decay;
* Price Change:
  * Price rise and fall change range in analysis;
  * Assuming current price is 100, change is 10%, then the range is 90~110;
* Volatility Change:
  * Volatility rise and fall change range in analysis;
  * Assuming current volatility is 20%, change is 10%, then the range is 10%~30%.

After clicking the execute analysis button, the stress testing engine will calculate the corresponding target data based on the current trading portfolio positions and the price and implied volatility situation under each scenario, and draw the results as a 3D surface.

The figure below shows the results with Gamma value as the calculation target, 10% price change, and 15% volatility change:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/18.png)

The vertical axis in the 3D graph is the calculation target value, and the two horizontal axes are the price and volatility change values respectively.


## Volatility Management

Click the [Volatility Management] button on the management interface to open the pricing volatility management interface:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/11.png)

Click the option chain label at the top to switch the pricing volatility management component of the corresponding option chain. When opened for the first time, the [Pricing IV] values in the table below are all 0.

First, perform pricing curve initialization. Click the [Reset] button at the top to map the median IV of out-of-the-money options at the current strike price to the pricing IV.

After mapping is completed, you can view the current pricing volatility curve shape in the volatility chart. If the pricing IV of a certain strike price is not smooth compared to the overall curve, you can fit it based on the relatively smooth pricing IV of the strike price.

In the [Execute Fit] column of the component table, check the strike price checkbox to be fitted. After checking is completed, click the [Fit] button at the top to execute volatility curve fitting based on OptionMaster's built-in Cubic Spline (cubic interpolation) algorithm.

After fitting is completed, if there are still unsatisfactory parts, you can manually fine-tune through the scroll box in the [Pricing IV] column. Click the up and down arrows to rise or fall by 0.1% each time, or you can directly enter the value you want to modify.

When the overall view of the volatility curve height needs to be shifted due to overall view of the volatility curve height, you can use the [+0.1%] and [-0.1%] buttons at the top of the component to shift and adjust the pricing volatility of all strike prices.

## Electronic Eye

Click the [Electronic Eye] button on the management interface to open the portfolio's electronic eye automatic arbitrage algorithm function:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/12.png)

The electronic eye algorithm can automatically capture instantaneous trading execution opportunities appearing in the market within the allowed position range based on the pricing volatility curve preset by the trader, and combine with the Delta automatic hedging function to ensure the overall Delta neutrality of the investment portfolio.

The electronic eye interface is similar to T-type quote, divided into left and right areas, with the middle white being the strike price, left side being call options, and right side being put options. Each option corresponds to an independent electronic eye trading algorithm. Traders can start hundreds of trading algorithms simultaneously (specific number depends on CPU performance) without interfering with each other.

Configuration parameters for each electronic eye algorithm include:

* Trading Spread Related
  * Price Spread
  * IV Spread
* Position Limit Related
  * Position Range
  * Target Position
* Maximum Order
  * Maximum order quantity per single order
* Direction
  * Trading direction allowed by the algorithm
  * Including only allowed to go long, only allowed to go short, allowed to trade in both directions

The execution flow of the electronic eye algorithm is as follows:

1. Based on pricing volatility, calculate the option's **theoretical price**
2. Calculate the target buy/sell spread:
   1. IV spread price value = IV spread * option theoretical Vega value
   2. Trading spread = max(price spread, IV spread price value)
3. Calculate target buy/sell prices:
   1. Target bid = theoretical price - trading spread / 2
   2. Target ask = theoretical price + trading spread / 2
4. Taking long trading as an example, when the order book ask 1 price is lower than the target bid, trigger a buy signal
5. Calculate this round's order quantity:
   1. Algorithm position upper limit = target position + position range
   2. Remaining long tradable quantity = algorithm long position upper limit - current net position
   3. This round's order quantity = min(remaining long tradable quantity, ask 1 quantity, maximum order quantity)
6. Use the target bid and this round's order quantity to send the corresponding trading order

After configuring the algorithm parameters, click the button in the [Pricing] column of that row to start the algorithm's pricing calculation, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/13.png)

[Pricing] and [Trading] button status display:

* When N, it means the algorithm has not started the task currently
* When Y, it means the algorithm is already executing the corresponding task

Starting pricing for the 4 option algorithms will start updating target buy/sell prices and related values in real-time.

At this time, click the button in the [Trading] column to start the algorithm's trading execution. When price and position conditions are met, trading orders will be automatically sent. Detailed algorithm running status log information can be monitored through the log area on the right:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/option_master/14.png)

When batch modification of algorithm configuration is needed, it can be operated through the global modification function in the upper right corner of the electronic eye window, which is more convenient and quick.


