"""
This program usesVeighNaframeworkviaCTPinterfaceconnect tofutures market，and automatically recordsspecified exchangesandinstrumentsmarket data。

Suitable forbeginnersto learnVeighNaframeworkbasic usageanddata recording process。
"""

# LoadPythonstandard library
from logging import INFO
from time import sleep

# LoadVeighNacore framework
from vnpy.event import EventEngine, Event
from vnpy.trader.setting import SETTINGS
from vnpy.trader.engine import MainEngine, LogEngine
from vnpy.trader.object import ContractData
from vnpy.trader.constant import Exchange, Product
from vnpy.trader.event import EVENT_CONTRACT

# LoadVeighNaplugin modules
from vnpy_ctp import CtpGateway
from vnpy_datarecorder import DataRecorderApp, RecorderEngine
from vnpy_datarecorder.engine import EVENT_RECORDER_LOG


# Enable logging functionality
# Logging is very important for troubleshooting and monitoring system status
SETTINGS["log.active"] = True       # Activate logging
SETTINGS["log.level"] = INFO        # Set log level toINFO，for detailed output
SETTINGS["log.console"] = True      # Display logs in console for real-time viewing


# CTPinterfacelogin credentials
# The following usesSimNowdemo account info，beginners can apply onSimNowwebsite
ctp_setting: dict[str, str] = {
    "username": "888888",                       # SimNowaccount name
    "password": "123456",                         # SimNowpassword
    "broker_id": "9999",                     # SimNowbroker ID is fixed at9999
    "trading_server": "180.168.146.187:10201",    # SimNowtrading server address and port
    "market_data_server": "180.168.146.187:10211",    # SimNowmarket data server address and port
    "product_name": "simnow_client_test",         # Product name to distinguish different clients
    "auth_code": "0000000000000000"            # Auth code，SimNowdemo account uses default value
}


# List of exchanges for data recording
# Uncomment as needed to add more exchanges
recording_exchanges: list[Exchange] = [
    Exchange.CFFEX,          # China Financial Futures Exchange
    # Exchange.SHFE,         # Shanghai Futures Exchange
    # Exchange.DCE,          # Dalian Commodity Exchange
    # Exchange.CZCE,         # Zhengzhou Commodity Exchange
    # Exchange.GFEX,         # Guangzhou Futures Exchange
    # Exchange.INE,          # Shanghai International Energy Exchange
]


# Types of instruments for data recording
# Uncomment as needed to add more instrument types
recording_products: list[Product] = [
    Product.FUTURES,        # Futures
    # Product.OPTION,       # Options
]


def run_recorder() -> None:
    """
    Run the market data recording program

    This function is the main body of the program, working as follows:
    1. CreateVeighNacore components（event engine、main engine）
    2. Add trading gateway and application modules
    3. Configure data recording rules
    4. Connect to exchange and start recording data
    """
    # Create event engine, responsible for communication between modules
    event_engine: EventEngine = EventEngine()

    # Create main engine, manages system modules including gateways, applications, etc.
    main_engine: MainEngine = MainEngine(event_engine)

    # AddCTPinterface，connect tofutures market
    main_engine.add_gateway(CtpGateway)

    # AdddataRecordEngine，for recordingTickdata to database
    recorder_engine: RecorderEngine = main_engine.add_app(DataRecorderApp)

    # Define contract subscription function
    def subscribe_data(event: Event) -> None:
        """
        Process contract push and subscribe to market data

        When the system receives contract info, based on preset exchange and instrument filter conditions,
        automatically add market data recording tasks for qualifying contracts.

        Args:
            event: Event object containing contract info
        """
        # Get contract data from event object
        contract: ContractData = event.data

        # Check if contract meets recording criteria
        if (
            contract.exchange in recording_exchanges    # Check if contract exchange is in preset list
            and contract.product in recording_products  # Check if contract product type is in preset list
        ):
            # Add market data recording task for this contract，vt_symbolisVeighNais unique ID in VeighNa，format"code.exchange"
            recorder_engine.add_tick_recording(contract.vt_symbol)      # RecordTickdata
            recorder_engine.add_bar_recording(contract.vt_symbol)       # RecordminuteKline

    # Register contract event handler，when newContract infois pushed，automatically callssubscribe_datafunction
    event_engine.register(EVENT_CONTRACT, subscribe_data)

    # Get log engine and configure log handling
    log_engine: LogEngine = main_engine.get_engine("log")

    def print_log(event: Event) -> None:
        """
        Process log events from data recording module

        Output log info from data recording module to console and log files,
        facilitating monitoring of recording process and troubleshooting.

        Args:
            event: Event object containing log info
        """
        log_engine.logger.log(INFO, event.data)

    # Register log event handler，when new log is pushed，automatically callsprint_logfunction
    event_engine.register(EVENT_RECORDER_LOG, print_log)

    # ConnectCTPinterfaceand login，firstArgsisinterfacesettings，secondArgsisinterfacename
    main_engine.connect(ctp_setting, CtpGateway.default_name)

    # Wait30seconds，CTPgateway needs time to complete initialization after connection
    sleep(30)

    # Prompt user that program has started, user can exit anytime as needed
    input(">>>>>> High-frequency market data recording started, recording data. Press Enter to exit <<<<<<")

    # Close main engine for safe exit, avoid losing in-memory data not yet saved to database
    main_engine.close()


# PythonStandard Python entry point，executesrun_recorderfunction
if __name__ == "__main__":
    run_recorder()
