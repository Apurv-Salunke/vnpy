# 4.3.0 Release

## New Features

1. vnpy.alpha adds WorldQuant's Alpha 101 factor feature dataset

## Changes

1. vnpy_sec/vnpy_esunny upgraded for v4.0 compatibility
2. vnpy_ctabacktester strategy code editing now supports Cursor and PyCharm editors
3. vnpy_ctastrategy backtesting engine adds RGR performance statistics metric (thanks to @上弦之月)
4. ArrayManager adds type hint declarations for indicator calculation function overloads
5. vnpy_ctp adds log output for order cancellation in special cases (non-trading hours, insufficient funds, etc.)
6. DataProxy comparison operations now return pl.Int32 directly (instead of Bool)
7. Refactored ts_slope / ts_rsquare / ts_resi operator functions

## Bug Fixes

1. vnpy_ib fixed historical data query issue (query_history function now uses query lock to resolve multi-threading conflicts)
2. vnpy_optionmaster fixed implied volatility calculation convergence issue for deep out-of-the-money options


# 4.2.0 Release

## New Features

1. vnpy_riskmanager module refactored
    a. Plugin-based design with standardized risk rule development templates
    b. Supports risk control rules required by Chinese futures programmatic trading regulations
    c. Outputs interception logs with audio alerts (Windows only)
    d. Uses system tray icon to display trading risk interception log popups
    e. Provides Cython version risk rule development templates and implementations
    f. Supports automatic scanning and loading of user-defined risk rules (placed in rules folder under Trader directory)
2. vnpy_polygon datafeed interface supports historical data for international stocks, futures, and options

## Changes

1. vnpy_ctp updated underlying API to 6.7.11 (unified production and test version)
2. vnpy_dolphindb upgraded for v4.0 compatibility
3. vnpy_tqsdk simplified timestamp formatting for improved performance
4. vnpy_sqlite now supports data files declared in configuration
5. vnpy_taos optimized get_bar_overview and get_tick_overview function performance (direct access to super table tags)
6. vnpy_spreadtrading / vnpy_portfoliostrategy / vnpy_scripttrader module registration logs now output to log engine
7. vnpy_optionmaster optimized minimum value boundary logic in pricing model
8. Global config log.level changed to INFO (10), verbose logging enabled by default
9. MainEngine added call logging for trading functions
10. vnpy.alpha Dataset added process_data function for testing different data processors
11. vnpy_ib updated to support ibapi version 10.40.1

## Bug Fixes

1. vnpy_gm fixed CFFEX and DCE contract code conversion issue
2. vnpy_rqdata fixed market data subscription function error in RqdataGateway
3. vnpy_optionmaster fixed exception when closing window
4. vnpy_portfoliostrategy fixed parameter passing issue in genetic algorithm optimization
5. Fixed Linux sdist installation issues: vnpy_mini / vnpy_sopt / vnpy_rohon / vnpy_tap / vnpy_tts
6. vnpy_xt fixed XtGateway parameter error during reconnection
7. vnpy_optionmaster fixed theta calculation formula in Black-76 model
8. vnpy_postgresql fixed data not updating on primary key conflict


# 4.1.0 Release

## New Features

1. vnpy_mcdata adds Tick data query support
2. OrderType enum added ETF type for ETF subscription and redemption

## Changes

1. Upgraded extension modules for v4.0 compatibility:
    * Trading Gateways:
        * Futures: vnpy_uft/vnpy_mini/vnpy_femas/vnpy_ctptest
        * Stocks: vnpy_xtp/vnpy_tora
        * Options: vnpy_hts/vnpy_sopt/vnpy_sopttest
        * Asset Management: vnpy_rohon/vnpy_lstar/vnpy_jees
        * Others: vnpy_ksgold/vnpy_tts/vnpy_tap/vnpy_da/vnpy_ib
    * Strategy Apps:
        * Strategy: vnpy_portfoliostrategy/vnpy_ctabacktester/vnpy_spreadtrading/vnpy_scripttrader
        * Trading: vnpy_algotrading/vnpy_optionmaster/vnpy_portfoliomanager/vnpy_paperaccount
        * Data: vnpy_datarecorder/vnpy_excelrtd/vnpy_datamanager
        * Utilities: vnpy_chartwizard/vnpy_webtrader/vnpy_rpcservice/vnpy_riskmanager
    * Databases: vnpy_mysql/vnpy_postgresql/vnpy_mongodb/vnpy_taos
    * Datafeeds: vnpy_gm/vnpy_xt/vnpy_tqsdk/vnpy_ifind/vnpy_tushare/vnpy_wind
2. Replaced unbind with close function for safe zmq.Socket shutdown in vnpy.rpc
3. Changed PySide6 dependency to 6.8.2.1 to resolve底层 warning issues
4. Changed ta-lib dependency to 0.6.4 to fix Linux and Mac installation issues
5. Adjusted Qt global exception log level to Critical
6. vnpy_datarecorder removed unnecessary quote recording exceptions, changed to logging
7. vnpy_rqdata changed stock data adjustment method from pre to pre_volume
8. Database module defaults to skipping extra field when recording market data
9. vnpy_ib supports ibapi 10.30.1, added support for new cancel order function parameters

## Bug Fixes

1. Fixed indicator calculation issues due to MA_Type class no longer being an enum in new ta-lib version
2. Fixed missing get_tick function in MainEngine
3. Fixed email sending issue with QQ email provider
4. Fixed log module missing default gateway_name parameter causing Qt global exception error
5. vnpy_rohon added Linux installation script to resolve missing dynamic library issue
6. vnpy_rqdata fixed lowercase contract code secondary continuous 88A2 historical data query issue


# 4.0.0 Release

## New Features

1. Added vnpy.alpha module for machine learning multi-factor strategies
2. MultiCharts datafeed module vnpy_mcdata

## Changes

1. Core support upgraded to Python 3.13
2. Use pyproject.toml for unified project configuration
3. Replaced logging with loguru for logging functionality
4. Use mypy for static type checking optimization
5. Use ruff for code quality optimization
6. Use uv as development environment management tool
7. Upgraded extension modules for v4.0 compatibility: vnpy_ctp/vnpy_ctastrategy/vnpy_sqlite/vnpy_rqdata

## Bug Fixes

1. Fixed potential sorting disorder in PySide6 cells


# 3.9.4 Release

## New Features

1. vnpy_tora added dynamic terminal key support for login
2. vnpy_taos upgraded to support TDengine 3.0

## Changes

1. vnpy_xt market data interface added limit up/down price fields
2. vnpy_taos removed unnecessary timezone conversion for performance
3. vnpy_dolphindb optimized memory usage when writing large data volumes
4. vnpy_portfoliostrategy simplified calculate_pnl daily PnL calculation in backtesting engine
5. vnpy_tap/vnpy_tts upgraded pybind11 wrapper library to support Python 3.12
6. EmailEngine catches exceptions and logs on email sending failure

## Bug Fixes

1. vnpy_optionmaster removed unnecessary price cache code
2. vnpy_dolphindb fixed incorrect timezone when saving overview


# 3.9.3 Release

## New Features

1. Lstar asset management gateway vnpy_lstar
2. Voltrader datafeed vnpy_voltrader
3. vnpy_rpcservice added RpcDatafeed for datafeed proxy

## Changes

1. Adapted to PySide6 6.3.0+: vnpy/vnpy_ctastrategy/vnpy_ctabacktester/vnpy_portfoliostrategy/vnpy_spreadtrading/vnpy_datamanager/vnpy_algotrading/vnpy_portfoliomananger/vnpy_optionmaster
2. vnpy_uft upgraded to API 3.7.4.1004
3. vnpy_ib execDetails trade callback now uses cached order record to populate exchange, resolving SMART exchange field changes
4. vnpy_ib openOrder order callback prioritizes cached order record for exchange field stability
5. vnpy_ib historical data query now uses UTC timestamps
6. vnpy_ib historical data async wait time extended to 600 seconds
7. vnpy_ib added option chain contract data update completion callback
8. vnpy_ib contract multiplier now supports float values
9. ContractData added max_volume field for maximum single order size

## Bug Fixes

1. Fixed spread position not cleared in vnpy_spreadtrading backtesting engine clear_data
2. Fixed vnpy_ib historical data query error log output


# 3.9.2 Release

## New Features

1. vnpy_xt added real-time market data interface XtGateway
2. vnpy_xt implemented xtdc singleton using file lock
3. vnpy_ib added market data unsubscription
4. vnpy_ib contract multiplier now supports float values
5. vnpy_ib added option chain contract data update completion callback
6. vnpy_ctabacktester, vnpy_ctastrategy, vnpy_portfoliostrategy added i18n internationalization support

## Changes

1. vnpy_algotrading added algorithm status filtering for order/trade events
2. vnpy_tushare to_ts_asset function added ETF fund support
3. vnpy_xt adapted to xtquant 240613.1.1
4. vnpy_xt enabled actual futures night trading hours, added auction call K-line synthesis
5. vnpy_tts updated API to 6.7.2
6. vnpy_rohon updated API: market 1.4.1.3, trading 30.4.1.24
7. vnpy_tap improved API log output
8. vnpy_rest added json parameter support for REST requests
9. vnpy_excelrtd optimized PyXLL module loading on startup
10. vnpy_spreadtrading uses thread pool for async strategy initialization
11. vnpy_ib removed auto option contract query
12. vnpy_ib caches queried IB contract data, simplified ticker query function
13. vnpy_ib historical data query uses UTC timestamps, max wait time extended to 600 seconds
14. vnpy_ctastrategy performance metrics added EWM Sharpe ratio based on exponential moving average
15. vnpy_ctastrategy backtesting engine show_chart function now returns chart object directly

## Bug Fixes

1. Fixed vnpy_rohon market login failure judgment logic
2. Fixed missing localtime field in vnpy_datarecorder spread data recording
3. Fixed missing timezone info in datafeed timestamp for vnpy_spreadtrading
4. Fixed ZeroDivisionError in vnpy_paperaccount when volume is 0 after matching
5. Fixed vnpy_portfoliostrategy not canceling active orders when stopping strategy


# 3.9.1 Release

## New Features

1. Added i18n internationalization support with English translations
2. Added CFD and SWAP product type enums
3. vnpy_ib added COMEX, Eurex exchange support
4. vnpy_ib added CFD product support

## Changes

1. vnpy_rqdata improved Friday night trading data query support
2. vnpy_ib checks for spaces in code string when subscribing/orders
3. vnpy_ib added ConId non-digit character validation in contract parsing
4. vnpy_ib historical K-line data supports longer time spans (no longer limited to 6 months)
5. vnpy_da updated API to 1.18.2.0
6. vnpy_da removed historical data query function
7. vnpy_tora adjusted option order ID generation rule, supports up to 100k quantity
8. vnpy_xtp adjusted account frozen funds calculation
9. vnpy_optionmaster added IB stock option support
10. vnpy_optionmaster pricing model changed to calculate theoretical Greeks
11. vnpy_optionmaster adjusted object Greeks to theoretical mode
12. vnpy_optionmaster adjusted mid-IV calculation method
13. vnpy_spreadtrading uses thread pool for async strategy initialization
14. vnpy_postgresql supports automatic reuse of open database connections
15. vnpy_ctptest updated API to 6.7.2
16. Upgraded pybind11 to 2.11.1: vnpy_ctptest, vnpy_sopttest
17. vnpy_ctp updated API to 6.7.2
18. Adjusted extract_vt_symbol to handle "." in codes (e.g., HHI.HK-HKD-FUT.HKFE)
19. Updated vnpy core dependencies to 2024 versions

## Bug Fixes

1. Fixed vnpy_portfoliostrategy stop_strategy not canceling active orders
2. Fixed vnpy_xtp queryTickersPriceInfo underlying call error
3. Fixed RpcClient _last_received_ping variable type issue


# 3.9.0 Release

## New Features

1. Xuntou datafeed vnpy_xt supports stocks, futures, options, bonds, funds historical data
2. vnpy_ib added CBOE, CBOT exchange support, index options support
3. vnpy_rqdata added 88A2 continuous secondary contract support
4. vnpy_wind added GFEX, INE exchange support

## Changes

1. vnpy_sopt upgraded to API 3.7.0
2. vnpy_portfoliostrategy backtesting engine supports annual_days trading days parameter
3. BarGenerator removed tick timestamp check, delegated to user layer
4. vnpy_ib auto-queries option chain slice data after receiving contract
5. vnpy_paperaccount implemented special routing for IB contracts
6. Upgraded pybind11 to 2.11.1: vnpy_ctp, vnpy_sopt, vnpy_tora
7. vnpy_ctp filters unsupported order status push
8. vnpy_mysql compatible with no database write permissions for table initialization
9. vnpy_chartwizard supports closing individual chart tabs
10. vnpy_portfoliostrategy clears strategy state cache on removal
11. vnpy_portfoliostrategy adjusted daily PnL initialization for opening positions
12. Genetic optimization function added ngen_size and max_workers parameters

## Bug Fixes

1. Fixed vnpy_tora partial cancel order status mapping missing
2. Fixed vnpy_wind daily historical data NaN values
3. Fixed vnpy_mongodb Tick aggregation count error
4. Fixed vnpy_chartwizard spread quote display for upgraded vnpy_spreadtrading
5. Fixed vnpy_ctastrategy backtest error when trade records empty
6. Fixed vnpy_ctastrategy duplicate on_bar calls during strategy initialization


# 3.8.0 Release

## New Features

1. BarGenerator added daily K-line synthesis support
2. Refactored vnpy_tora based on Tora C++ API, supports VeighNa Station loading
3. vnpy_ib added option contract query, volatility and Greeks extended market data support

## Changes

1. vnpy_rest/vnpy_websocket restricted to Selector event loop on Windows
2. vnpy_rest/vnpy_websocket ensures all sessions complete on client shutdown
3. vnpy_ctp upgraded to API 6.6.9
4. vnpy_ctp supports DCE 1ms timestamp
5. vnpy_tqsdk filters unsupported K-line frequency queries
6. vnpy_datamanager added exchange display by data frequency, optimized loading speed
7. vnpy_ctabacktester skips backtesting if historical data is empty
8. vnpy_spreadtrading optimized UI with lightweight data structures
9. vnpy_spreadtrading spread engine events no longer go through event engine (reduced latency)
10. vnpy_rpcservice added gateway_name replacement for order return IDs
11. vnpy_portfoliostrategy strategy template added get_engine_type function
12. vnpy_sec updated market API to 1.6.45.0, trading API to 1.6.88.18
13. vnpy_ib updated to API 10.19.1, restored ConId numeric code support
14. Uses BaseDatafeed as default when no datafeed configured
15. Genetic algorithm spawns child processes with spawn mode to avoid database connection issues
16. Contract manager widget added option-specific data fields

## Bug Fixes

1. Fixed vnpy_datarecorder spread data recording for new vnpy_spreadtrading version
2. Fixed vnpy_algotrading StopAlgo status update missing after full execution
3. Fixed vnpy_ctastrategy duplicate on_bar calls during initialization
4. Fixed vnpy_wind daily historical data NaN values


# 3.7.0 Release

## New Features

1. Added Shanghai-HK Stock Connect and Shenzhen-HK Stock Connect exchange enums
2. Added Linux support for vnpy_tap
3. Added new continuous contract data support for vnpy_rqdata (pre-switch day close ratio adjustment)

## Changes

1. vnpy_ctastrategy/vnpy_ctabacktester filters out TargetPosTemplate when loading strategy classes
2. vnpy_ctp only blocks re-authentication on authorization code errors
3. vnpy_uft added GFEX exchange support
4. vnpy_tqsdk added output log function support
5. vnpy_dolphindb allows user-specified database instance configuration
6. vnpy_rqdata optimized ZCE futures/options query conversion rules
7. vnpy_rqdata added GFEX exchange support
8. vnpy_portfoliostrategy added bankruptcy check in backtesting
9. vnpy_portfoliostrategy strategy template added get_size contract multiplier function
10. vnpy_portfoliostrategy backtesting doesn't use segmented loading for daily/hourly bars

## Bug Fixes

1. Fixed vnpy_rpcservice RPC interface vt prefix field error for push data
2. Fixed vnpy_mini INE exchange position special handling
3. Fixed vnpy_datamanager missing output function in batch data update
4. Fixed vnpy_spreadtrading backtest loading data from datafeed instead of local database


# 3.6.0 Release

## New Features

1. Added Mac system support (M1/M2) for vnpy_ctp

## Changes

1. BaseDatafeed functions added output parameter for logging
2. Updated datafeed modules for output parameter: vnpy_rqdata/vnpy_ifind/vnpy_wind/vnpy_tushare
3. Updated strategy modules for output parameter: vnpy_ctastrategy/vnpy_ctabacktester/vnpy_portfoliostrategy/vnpy_spreadtrading/vnpy_datamanager
4. OffsetConverter added SHFE/INE lock position mode support
5. Added global OffsetConverter in OmsEngine, removed from individual AppEngines
6. Added max process count limit for CTA strategy optimization: vnpy_ctastrategy/vnpy_ctabacktester
7. Added tqdm progress bar for exhaustive optimization
8. Added iteration count output for genetic optimization
9. Added underlying contract matching function for vnpy_optionmaster products
10. Upgraded vnpy_tts dll library, fixed openctp upgrade fund display issue
11. Fixed vnpy_ctastrategy to use unified timezone from vnpy.trader.database for data loading
12. Added get_size contract multiplier function to vnpy_ctastrategy template
13. Added bankruptcy check in vnpy_spreadtrading backtesting statistics
14. Added vt_symbol and direction position query function to vnpy_scripttrader
15. Modified vt_positionid string content, added gateway_name prefix

## Bug Fixes

1. Fixed exception hook threading_excepthook parameter error
2. Fixed vnpy_ib historical data retrieval failure
3. Fixed vnpy_rest/vnpy_websocket aiohttp proxy parameter must be None
4. Fixed vnpy_optionmaster Greeks monitor table row count issue
5. Fixed vnpy_rqdata stock option query error
6. Fixed vnpy_rqdata RqdataGateway futures index/continuous contract info error
7. Fixed vnpy_portfoliostrategy defaultdict conversion issue when restoring from cache


# 3.5.0 Release

## New Features

1. Added RQData cross-market data interface RqdataGateway
2. Added East Money Securities EMT gateway vnpy_emt

## Changes

1. Adjusted vnpy_algotrading module design (template, engine), single-contract execution only
2. Optimized vnpy_algotrading algorithm status control, added status enum, pause/resume support
3. Upgraded vnpy_hft to HFT Guojun unified gateway 2.0 API
4. Optimized vnpy_portfoliostrategy strategy template, supports target position adjustment trading

## Bug Fixes

1. Fixed Python 3.7 syntax compatibility for background thread exception hook
2. Fixed vnpy_mysql historical data loading time period duplication
3. Fixed vnpy_ib order failure due to TWS client upgrade
4. Fixed vnpy_rest/vnpy_websocket Python 3.10+ asyncio support
5. Fixed vnpy_sopt [SUBMITTING] status return on flow control order failure


# 3.4.0 Release

## New Features

1. Added Jees asset management gateway vnpy_jees

## Changes

1. Enabled keepalive mechanism for vnpy.rpc pyzmq connections
2. Removed EVENT_TIMER push from vnpy_rpcservice server
3. vnpy_postgresql now uses batch data writing for efficiency
4. Added VeighNa Trader sub-thread exception capture (Python>=3.8)
5. Adjusted vnpy_ib historical K-line data to use mid-price for forex and precious metals
6. Added bankruptcy check (<=0) for vnpy_ctastrategy backtesting
7. Optimized vnpy_webtrader encryption authentication, supports web process restart

## Bug Fixes

1. Fixed vnpy.rpc pyzmq 23.0+ NOBLOCK compatibility issue
2. Fixed vnpy_taos TDengine version upgrade d series compatibility issues
3. Fixed vnpy_datamanager data refresh failure to remove old data points


# 3.3.0 Release

## New Features

1. Added TickOverview object to vnpy.trader.database
2. Added Goldminer simulation gateway vnpy_gm
3. BaseData added extra field (dict type) for arbitrary related data

## Changes

1. Replaced pytz with Python built-in zoneinfo
2. Updated gateways, datafeeds, database adapters to use new ZoneInfo timezone
3. Database adapter vnpy.trader.database added stream parameter for streaming data writing

## Bug Fixes

1. Fixed vnpy_mongodb K-line data count issue (using new count_documents function)
2. Fixed BaseMonitor auto-save failure due to PySide6 object destruction order


# 3.2.0 Release

## New Features

1. Added GFEX (Guangzhou Futures Exchange) enum
2. Added CTP Option (ETF) penetration test gateway vnpy_sopttest
3. Added Currency.CAD (Canadian Dollar) enum
4. Added Exchange.TSE (Toronto) and Exchange.AMEX (Americas) enums
5. Added vnpy_taos TDengine time-series database adapter
6. Added vnpy_timescaledb TimescaleDB time-series database adapter

## Changes

1. Updated vnpy_ctp/vnpy_ctptest for GFEX support
2. Updated vnpy_tora spot API to latest: API_Python3.7_Trading_v4.0.3_20220222
3. Updated vnpy_tora option API to latest: API_Python3.7_v1.3.2_20211201
4. Updated vnpy_esunny/vnpy_tap API shutdown function calls
5. Removed inverse contract support from vnpy_ctastrategy/vnpy_ctabacktester/vnpy_optionmaster
6. Added Shanghai-HK Stock Connect, Shenzhen-HK Stock Connect, Toronto, Americas support to vnpy_ib
7. Added index market data support to vnpy_ib
8. Added strategy instance search to vnpy_ctastrategy trading management UI

## Bug Fixes

1. Fixed vnpy_mongodb K-line count issue (using new count_documents function)
2. Fixed PySide6 object destruction order causing BaseMonitor state save failure


# 3.1.0 Release

## New Features

1. Added Hundsun Cloud UF2.0 securities simulation gateway vnpy_uf
2. Added Huoxiang simulation gateway vnpy_hx

## Changes

1. Upgraded tzlocal to 4.2, eliminated get_localzone() warning
2. Improved function and variable type hints
3. Replaced QtCore.pyqtSignal with QtCore.Signal
4. Optimized vnpy_rohon order/trade details
5. Updated vnpy_xtp to 2.2.32.2.0, supports SSE new bond system
6. Optimized vnpy_mongodb batch writing (pymongo 4.0)
7. Added vnpy_ctp non-zero return value handling for order function
8. Changed vnpy_ctastrategy/vnpy_ctabacktester strategy dropdown to alphabetical sorting

## Bug Fixes

1. Fixed vnpy_optionmaster Greeks monitor data refresh issue
2. Fixed vnpy_mongodb timestamp timezone missing data loading range issue
3. Fixed vnpy_tts sdist lib file missing issue
4. Fixed vnpy_rqdata NaN parsing issue in query results


# 3.0.0 Release

## Changes

1. Removed api, gateway, app subdirectories
2. Removed requirements.txt default plugin dependencies
3. Simplified vnpy.rpc for reliable inter-process communication (local, LAN)
4. Removed authentication support from vnpy.rpc
5. Adjusted vnpy.rpc heartbeat mechanism
6. Removed QScintilla code editor, now uses VSCode
7. Optimized MainWindow QAction icon loading
8. MainEngine now supports custom gateway names when adding

## Bug Fixes

1. Fixed Linux/Mac [Settings] button not displaying with non-native menu bar


# 2.9.0 Release

## New Features

1. Added Hundsun HTS gateway vnpy_hts

## Changes

1. Removed Hundsun Option hsoption gateway
2. vnpy_webtrader added custom listen address/port support
3. vnpy_mongodb locked pymongo to 3.12.3
4. vnpy_udata added hs_udata library dependency
5. vnpy_uft upgraded to Hundsun API 3.7.2.4

## Separated

1. Separated Guotai Junan Securities gateway to vnpy_hft
2. Separated Hundsun Feichuang gateway to vnpy_sec
3. Separated RPC service to vnpy_rpcservice

## Bug Fixes

1. Fixed vnpy_tora cancel order conflict between cancel ID and order ID
2. Fixed vnpy_tora stock order [NOT_TRADED] status mapping error
3. Fixed vnpy_ctabacktester backtest start date cache issue
4. Fixed vnpy_udata infinite loop on empty download
5. Fixed vnpy_udata exception on empty download volume
6. Fixed vnpy_dolphindb contract name symbol read issue


# 2.8.0 Release

## New Features

1. Added Orient Securities OST gateway vnpy_ost
2. Added portfolio strategy parameter optimization

## Bug Fixes

1. Fixed C++ gateway separation installation script compilation errors
2. Fixed vnpy_xtp SSE market subscription crash issue
3. Fixed vnpy_tushare None data field errors
4. Fixed vnpy_mini SHFE night trading timestamp date error
5. Fixed vnpy_uft ETF option contract info parsing missing
6. Fixed vnpy_wind N/A parsing on missing data
7. Fixed vnpy_webtrader html static files missing
8. Fixed vnpy_dolphindb Tick data type issue
9. Fixed vnpy_dolphindb empty data read BUG
10. Fixed vnpy_esunny Gold TD contract multiplier 0 issue
11. Fixed vnpy_ctastrategy false boolean value read failure
12. Fixed vnpy_rohon option contract field assignment error
13. Fixed vnpy_leveldb Linux installation dependency issue

## Changes

1. Removed old requests-based RestClient
2. Removed old websocket-client-based WebsocketClient
3. vnpy_tts added SSE/SEZ stock simulation trading
4. Removed vnpy_ctp option inquiry instruction
5. Added vnpy_ctp authorization failure duplicate operation prevention
6. Optimized vnpy_uft reconnection market subscription logic
7. Added vnpy_arctic username/password authentication
8. Added stock option support to vnpy_mini

## Separated

1. Separated Tora gateway to vnpy_tora, upgraded to 4.0
2. Separated Femas gateway to vnpy_femas
3. Separated Kingstar Gold gateway to vnpy_ksgold
4. Separated Portfolio Strategy to vnpy_portfoliostrategy
5. Separated Excel RTD to vnpy_excelrtd
6. Separated Paper Account to vnpy_paperaccount


# 2.7.0 Release

## New Features

1. Added TinySoft datafeed vnpy_tinysoft
2. Added iFinD datafeed vnpy_ifind
3. Added dYdx gateway vnpy_dydx
4. Added Wind datafeed vnpy_wind
5. Added PortfolioBarGenerator for PortfolioStrategy

## Changes

1. Removed KasiaGateway
2. Removed MarketRadarApp
3. Removed arbitrage and grid algorithms from AlgoTrading
4. vnpy_tushare added open_interest and turnover fields
5. vnpy_datamanager displays K-line info sorted by contract code
6. vnpy_dolphindb optimized data loading speed
7. vnpy_influxdb uses pandas CSV parsing for speed

## Bug Fixes

1. Fixed vnpy_ctp SHFE night trading timestamp date error
2. Fixed vnpy_arctic data overwrite issue on duplicate write

## Separated

1. Separated IB gateway to vnpy_ib
2. Separated Sgit gateway to vnpy_sgit
3. Separated Tap gateway to vnpy_tap
4. Separated Da gateway to vnpy_da
5. Separated AlgoTrading to vnpy_algotrading
6. Separated ScriptTrader to vnpy_scripttrader
7. Separated PortfolioManager to vnpy_portfoliomanager


# 2.6.0 Release

## New Features

1. Added two-sided quote send and cancel functions
2. Added two-sided quote monitor UI component
3. Added abstract database interface vnpy.trader.database
4. Added Arctic MongoDB interface vnpy_arctic
5. Added LevelDB interface vnpy_leveldb
6. Added DolphinDB interface vnpy_dolphindb
7. Added abstract datafeed interface vnpy.trader.datafeed
8. Added TuShare datafeed vnpy_tushare
9. Added Hundsun UData datafeed vnpy_udata
10. Added TQSDK datafeed vnpy_tqsdk
11. Added CoinAPI datafeed vnpy_coinapi

## Changes

1. Removed batch order and batch cancel functions
2. Removed TigerGateway
3. Removed XgjGateway
4. Removed AlgoTrading Jinna algorithm service support
5. RestClient added OS proxy support
6. RestClient/WebsocketClient default exception changed to print output
7. SpreadTrading removed inverse contract, linear spread, offset field support
8. SpreadTrading optimized flexible spread support, optimized quote filtering
9. SpreadTrading algorithm waits for all orders to complete and legs balanced before stopping

## Bug Fixes

1. Fixed Linux/Mac multiprocessing optimization startup error
2. Fixed WebsocketClient frequent disconnection due to heartbeat mechanism

## Separated

1. Separated RQData to vnpy_rqdata, upgraded to 2.9.38
2. Separated DataRecorder to vnpy_datarecorder
3. Separated ChartWizard to vnpy_chartwizard
4. Separated SQLite to vnpy_sqlite
5. Separated MySQL to vnpy_mysql
6. Separated PostgreSQL to vnpy_postgresql
7. Separated MongoDB to vnpy_mongodb
8. Separated InfluxDB to vnpy_influxdb
9. Separated OptionMaster to vnpy_optionmaster


# 2.5.0 Release

## New Features

1. Added TTS trading system gateway vnpy_tts (6.5.1)
2. Added Esunny gateway vnpy_esunny (1.0.2.2)
3. Added BarData and TickData turnover field

## Changes

1. SpreadTrading strategy initialization now queries RQData first for K-line spread data
2. MainWindow AboutDialog uses importlib_metadata for version info
3. Hidden [?] button in all dialogs
4. Changed TapGateway contract info from market to trading interface (avoid size=0 issue)
5. Improved VeighNa Trader exception dialog to prevent crash on repeated errors

## Bug Fixes

1. Fixed Linux/Mac XTP API auto-compilation during installation
2. Fixed PortfolioManager UI trade event listening type error
3. Fixed vnpy_rest Response missing text field
4. Fixed RestClient proxy port empty causing connection error
5. Fixed ArrayManager Aroon indicator output order error
6. Fixed database manager TickData localtime field missing

## Separated

1. Separated Rohon gateway to vnpy_rohon, upgraded to 6.5.1
2. Separated CTP MINI to vnpy_mini, upgraded to 1.5.6
3. Separated CTP Option to vnpy_sopt
4. Separated Hundsun UFT to vnpy_uft


# 2.4.0 Release

## New Features

1. Added TickData local timestamp field local_time (without timezone)
2. Added asyncio/aiohttp-based async REST API client vnpy_rest
3. Added asyncio/aiohttp-based async Websocket API client vnpy_websocket
4. Added multiprocessing genetic algorithm optimization
5. Added XTP API market login local network card address parameter

## Changes

1. Separated CTA strategy exhaustive/genetic optimization to vnpy.trader.optimize
2. Genetic optimization outputs all tested parameter results (not just best)
3. CTA engine reloads strategy files on modification (immediate effect)
4. CTA engine uses glob for strategy file scanning (avoids subdirectory files)
5. Separated CTA Strategy to vnpy_ctastrategy
6. Separated CTA Backtester to vnpy_ctabacktester
7. Separated XTP to vnpy_xtp, upgraded to 2.2.27.4
8. Separated RiskManager to vnpy_riskmanager
9. Separated DataManager to vnpy_datamanager

## Bug Fixes

1. Fixed MySQL/PostgreSQL K-line deletion error
2. Fixed aiohttp RestClient/WebsocketClient event loop restart failure
3. Fixed CtaBacktester Tick-level parameter optimization failure


# 2.3.0 Release

## Bug Fixes

1. Fixed IbGateway not auto-resubscribing after reconnection
2. Fixed CTA net position mode partial close/open order error
3. Fixed CtpGateway FAK/FOK order handling error
4. Fixed IbGateway historical data query parameter error
5. Fixed IbGateway hang on non-existent historical data
6. Fixed IbGateway contract multiplier string conversion missing
7. Fixed BarGenerator hourly K-line close price update missing
8. Fixed UftGateway ETF option connection issue
9. Fixed UftGateway millisecond timestamp handling error

## Changes

1. Modified CTA net position mode to support SHFE/INE today/yesterday position split
2. Adjusted PortfolioStrategy backtest K-line replay (no forward fill on missing data)
3. Separated CTP to vnpy_ctp
4. Separated CTP Test to vnpy_ctptest

## New Features

1. DataManager CSV import timezone selection
2. CtaStrategy strategy rollover assistant for futures contract month switching


# 2.2.0 Release

## Bug Fixes

1. Fixed DataManager K-line query date range reversed
2. Fixed PostgreSQL save_tick_data interval access error
3. Fixed DataRecorder add_bar_recording contract config error
4. Fixed PostgreSQL transaction failure, added autorollback=True
5. Fixed DataManager auto-update query range function call error
6. Fixed RQData historical data float precision issue
7. Fixed BarGenerator N-hour K-line close/volume/open_interest missing
8. Fixed ChartWidget duplicate time labels on sparse data
9. Fixed SpreadTrading spread quote timezone missing
10. Fixed IbGateway spot precious metals last price/timestamp missing
11. Fixed BarGenerator hourly K-line volume missing
12. Fixed vnpy.rpc exit failure after encryption enabled

## Changes

1. vnpy.chart ChartItem now draws on-demand (faster first display)
2. IbGateway historical data query includes all hours (including overnight electronic trading)
3. DataRecorder changed to batch database writing for performance

## New Features

1. IbGateway auto-reconnection on disconnect (10s check)
2. Added two-sided quote data structures and functions
3. Added OffsetConverter net position mode
4. Added CtaStrategy net position mode parameter
5. Added CtaStrategy backtesting annual trading days parameter
6. Added ChartWizard spread quote chart support
7. Added MarketRadar radar signal condition alerts


# 2.1.9.1 Release

## Bug Fixes

1. Fixed pyopenssl.extract_from_urllib3 compatibility issue in RestClient

## Changes

1. Adjusted OptionMaster at-the-money strike search algorithm (no longer depends on underlying contract)

## New Features

1. Added synthetic futures as pricing underlying in OptionMaster


# 2.1.9 Release

## Bug Fixes

1. Fixed BarGenerator hourly K-line duplicate push
2. Fixed genetic algorithm lru_cache causing identical optimization results
3. Fixed RestClient OpenSSL WinError 10054 WSAECONNRESET
4. Fixed exception dialog crash on frequent exceptions
5. Fixed ActiveOrderMonitor CSV save includes all orders
6. Fixed XtpGateway crash on duplicate login
7. Fixed XtpGateway stock market order type mapping error

## Changes

1. XTP price rounded to pricetick, funds to 2 decimals
2. BaseMonitor CSV header changed to UI Chinese (was field names)
3. TWAP algorithm order volume rounded to min_volume
4. Separated database client to vnpy.database module
5. Refactored SQLite/MySQL/PostgreSQL/MongoDB/InfluxDB clients, added BarOverview query

## New Features

1. BaseMonitor auto-saves column width
2. Added ToraGateway FENS server and fund account login support
3. Added InfluxDB Tick data storage/loading support
