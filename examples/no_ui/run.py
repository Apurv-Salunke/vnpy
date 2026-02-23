import multiprocessing
import sys
from time import sleep
from datetime import datetime, time

from vnpy.event import EventEngine
from vnpy.trader.setting import SETTINGS
from vnpy.trader.engine import MainEngine, LogEngine
from vnpy.trader.logger import INFO, logger

from vnpy_ctp import CtpGateway
from vnpy_ctastrategy import CtaStrategyApp, CtaEngine
from vnpy_ctastrategy.base import EVENT_CTA_LOG


SETTINGS["log.active"] = True
SETTINGS["log.level"] = INFO
SETTINGS["log.console"] = True


ctp_setting = {
    "username": "",
    "password": "",
    "broker_id": "",
    "trading_server": "",
    "market_data_server": "",
    "product_name": "",
    "auth_code": "",
    "product_info": ""
}


# Chinese futures market trading period (day/night)
DAY_START = time(8, 45)
DAY_END = time(15, 0)

NIGHT_START = time(20, 45)
NIGHT_END = time(2, 45)


def check_trading_period() -> bool:
    """"""
    current_time = datetime.now().time()

    trading = False
    if (
        (current_time >= DAY_START and current_time <= DAY_END)
        or (current_time >= NIGHT_START)
        or (current_time <= NIGHT_END)
    ):
        trading = True

    return trading


def run_child() -> None:
    """
    Running in the child process.
    """
    SETTINGS["log.file"] = True

    event_engine: EventEngine = EventEngine()
    main_engine: MainEngine = MainEngine(event_engine)
    main_engine.add_gateway(CtpGateway)
    cta_engine: CtaEngine = main_engine.add_app(CtaStrategyApp)
    logger.info("Main engine created successfully")

    log_engine: LogEngine = main_engine.get_engine("log")       # type: ignore
    event_engine.register(EVENT_CTA_LOG, log_engine.process_log_event)
    logger.info("Registered log event listener")

    main_engine.connect(ctp_setting, "CTP")
    logger.info("ConnectCTPinterface")

    sleep(10)

    cta_engine.init_engine()
    logger.info("CTAStrategyInitializeCompleted")

    cta_engine.init_all_strategies()
    sleep(60)   # Leave enough time to complete strategy initialization
    logger.info("CTAStrategyAllInitialize")

    cta_engine.start_all_strategies()
    logger.info("CTAStrategyAllStart")

    while True:
        sleep(10)

        trading = check_trading_period()
        if not trading:
            logger.info("Closing child process")
            main_engine.close()
            sys.exit(0)


def run_parent() -> None:
    """
    Running in the parent process.
    """
    print("StartCTAStrategydaemon parentprocess")

    child_process = None

    while True:
        trading = check_trading_period()

        # Start child process in trading period
        if trading and child_process is None:
            print("Starting child process")
            child_process = multiprocessing.Process(target=run_child)
            child_process.start()
            print("Child process started successfully")

        # Exit child process outside recording hours
        if not trading and child_process is not None:
            if not child_process.is_alive():
                child_process = None
                print("Child process closed successfully")

        sleep(5)


if __name__ == "__main__":
    run_parent()
