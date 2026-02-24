# Feature Introduction

As a Python-based quantitative trading program development framework, VeighNa is committed to providing quantitative solutions from trading API integration to automated strategy trading.

## Target Users

If you have the following needs, consider trying VeighNa:

* Develop your own quantitative trading programs based on the Python language, fully utilizing Python's powerful data research and machine learning ecosystem
* Connect to many different types of financial markets at home and abroad through a standardized trading platform system: securities, futures, options, foreign markets, etc.
* Use a fully tested quantitative strategy engine to complete the entire business process from data maintenance, strategy development, backtesting research to automated live trading
* Customize and extend the platform with various customizations to meet personalized trading needs: add trading interfaces, modify GUI graphical interfaces, develop complex strategy applications based on event-driven engines
* Control the source code details of trading programs, eliminate various program backdoors, and avoid risks such as strategy theft, trading signal interception, account password theft, etc.
* Save capital costs for quantitative trading platforms, no longer need to pay software licensing fees of tens of thousands per year or additional point additions per transaction


## Application Scenarios

From professional individual investors, startup private equity firms, to securities company asset management departments, all can find application scenarios for VeighNa.

* Professional individual investors: Use VeighNa Trader to directly connect to the futures company's CTP futures counter, implementing the CTA business process from strategy development to automated live trading
* Startup private equity firms: Build a unified order placement channel on the server side based on RpcService, allowing traders to develop various trading strategy applications on their local computers
* Securities company asset management departments: Connect to the O32 asset management system uniformly deployed by securities companies, customize and develop multi-strategy complex systems based on event-driven engines


## Supported Interfaces

**vnpy.gateway**, covering trading interfaces for all domestic and international trading varieties:

* Domestic Market

  * CTP (ctp): Futures, Futures Options

  * CTP Test (ctptest): Futures, Futures Options

  * CTP Mini (mini): Futures, Futures Options

  * Femas (femas): Futures

  * CTP Option (sopt): ETF Options

  * Vertex Feichuang (sec): ETF Options

  * Vertex HTS (hts): ETF Options

  * Hundsun UFT (uft): Futures, ETF Options

  * Esunny (esunny): Futures, Gold TD

  * Zhongtai XTP (xtp): A-shares, Margin Trading, ETF Options

  * Guotai Junan Unified Trading Gateway (hft): A-shares, Margin Trading

  * Huaxin Qidian Stock (torastock): A-shares

  * Huaxin Qidian Option (toraoption): ETF Options

  * Comstar (comstar): Interbank Market

  * Oriental Securities OST (ost): A-shares

  * Ronghang (rohon): Futures Asset Management

  * TTS (tts): Futures

  * Feishu (sgit): Gold TD

  * Kingstar Gold (ksgold): Gold TD

* Overseas Market

  * Interactive Brokers (ib): Overseas Multi-variety

  * Esunny 9.0 Foreign (tap): Foreign Futures

  * Direct Futures (da): Foreign Futures

* Special Applications

  * RPC Service (rpc): Cross-process communication interface for distributed architecture


## Supported Applications

**vnpy.app**, ready-to-use quantitative strategy trading applications:

* cta_strategy: CTA strategy engine module, while maintaining ease of use, allows users to finely control the order placement and cancellation behavior during CTA strategy operation (reduce trading slippage, implement high-frequency strategies)

* cta_backtester: CTA strategy backtesting module, without using Jupyter Notebook, directly use the graphical interface to perform strategy backtesting analysis, parameter optimization, and related work

* spread_trading: Multi-contract spread arbitrage module, in addition to allowing users to manually start algorithm spread trading, also supports users to use the SpreadStrategyTemplate strategy template to develop various spread quantitative trading strategies

* algo_trading: Algorithm trading module, providing multiple commonly used intelligent trading algorithms: TWAP, Sniper, Iceberg, BestLimit, etc. Supports saving common algorithm configurations

* option_master: Option volatility trading module, providing volatility curve charts, allowing users to make corresponding judgment analysis, and then use volatility management components to set pricing reference volatility, and then automatically scan market trading opportunities through option electronic eye algorithm and complete transactions instantly

* portfolio_strategy: Multi-contract portfolio strategy module, specifically designed for quantitative strategies that need to trade multiple contracts simultaneously, meeting their historical data backtesting and automated live trading needs

* script_trader: Script strategy module, designed for multi-instrument portfolio trading strategies, can also directly implement trading in the form of REPL commands in the command line, does not support backtesting functionality

* chart_wizard: Real-time K-line chart module, can achieve simple real-time K-line market display, directly enter the vt_symbol in the local contract code edit box, click the [New Chart] button to open the chart for the corresponding contract

* rpc_service: RPC service module, allows a VeighNa Trader process to be started as a server, as a unified market data and trading routing channel, allowing multiple clients to connect simultaneously, implementing a multi-process distributed system

* excel_rtd: EXCEL RTD module, RTD stands for RealTimeData, is an Excel data docking solution designed by Microsoft mainly for real-time data needs in the financial industry. This module is used to implement the function of accessing any data information in the VeighNa program in Excel

* data_manager: Historical data management module, is a multi-functional management tool for historical data inside VeighNa Trader. Can support data import, data viewing, and data export functions, supports custom data table header formats

* data_recorder: Market recording module, configured through the graphical interface, records Tick or K-line market data to the database in real-time according to requirements, used for strategy backtesting or live initialization

* risk_manager: Risk management module, providing statistics and limits on rules including trading flow control, order quantity, active orders, total cancelled orders, etc., effectively implementing front-end risk control functions

* web_trader: Web service module, designed for B-S architecture requirements, implements a web server that provides active function calls (REST) and passive data push (Websocket)

* portfolio_manager: Investment portfolio management module, this module is mainly oriented to investors using fundamental strategies, for each investment strategy, creates an independent portfolio strategy object

* paper_account: Simulated trading account module, is designed to solve the current problem of various simulation trading accounts that need to rely on server-side functions, directly provides a localized simulated trading environment inside the trading client, and matches orders based on actual market tick data


## General Components

**vnpy.event**, a concise and easy-to-use event-driven engine, as the core of event-driven trading programs.

**vnpy.chart**, Python high-performance K-line chart, supporting large data volume chart display and real-time data update functions.

**vnpy.trader.database**, integrates several major database management modules to support database read/write performance and future new database extensions.

**vnpy.trader.datafeed**, provides a standardized interface BaseDataFeed, bringing more flexible data service support.
