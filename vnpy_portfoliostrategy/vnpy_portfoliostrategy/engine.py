import importlib
import glob
import traceback
from collections import defaultdict
from pathlib import Path
from types import ModuleType
from collections.abc import Callable
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

from vnpy.event import Event, EventEngine
from vnpy.trader.engine import BaseEngine, MainEngine, LogEngine
from vnpy.trader.object import (
    OrderRequest,
    CancelRequest,
    SubscribeRequest,
    HistoryRequest,
    LogData,
    TickData,
    OrderData,
    TradeData,
    BarData,
    ContractData
)
from vnpy.trader.event import (
    EVENT_TICK,
    EVENT_ORDER,
    EVENT_TRADE
)
from vnpy.trader.constant import (
    Direction,
    OrderType,
    Interval,
    Exchange,
    Offset
)
from vnpy.trader.utility import load_json, save_json, extract_vt_symbol, round_to
from vnpy.trader.datafeed import BaseDatafeed, get_datafeed
from vnpy.trader.database import BaseDatabase, get_database, DB_TZ

from .base import (
    APP_NAME,
    EVENT_PORTFOLIO_LOG,
    EVENT_PORTFOLIO_STRATEGY,
    EngineType
)
from .locale import _
from .template import StrategyTemplate


class StrategyEngine(BaseEngine):
    """PortfolioStrategyEngine"""

    engine_type: EngineType = EngineType.LIVE

    setting_filename: str = "portfolio_strategy_setting.json"
    data_filename: str = "portfolio_strategy_data.json"

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine) -> None:
        """"""
        super().__init__(main_engine, event_engine, APP_NAME)

        self.strategy_data: dict[str, dict] = {}

        self.classes: dict[str, type[StrategyTemplate]] = {}
        self.strategies: dict[str, StrategyTemplate] = {}

        self.symbol_strategy_map: dict[str, list[StrategyTemplate]] = defaultdict(list)
        self.orderid_strategy_map: dict[str, StrategyTemplate] = {}

        self.init_executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)

        self.vt_tradeids: set[str] = set()

        # DatabaseandDataService
        self.database: BaseDatabase = get_database()
        self.datafeed: BaseDatafeed = get_datafeed()

    def init_engine(self) -> None:
        """InitializeEngine"""
        self.init_datafeed()
        self.load_strategy_class()
        self.load_strategy_setting()
        self.load_strategy_data()
        self.register_event()
        self.write_log(_("PortfolioStrategyEngineInitializeSuccess"))

    def close(self) -> None:
        """Close"""
        self.stop_all_strategies()

    def register_event(self) -> None:
        """RegisterEventEngine"""
        self.event_engine.register(EVENT_TICK, self.process_tick_event)
        self.event_engine.register(EVENT_ORDER, self.process_order_event)
        self.event_engine.register(EVENT_TRADE, self.process_trade_event)

        log_engine: LogEngine = self.main_engine.get_engine("log")
        log_engine.register_log(EVENT_PORTFOLIO_LOG)

    def init_datafeed(self) -> None:
        """InitializeDataService"""
        result: bool = self.datafeed.init(self.write_log)
        if result:
            self.write_log(_("DataServiceInitializeSuccess"))

    def query_bar_from_datafeed(
        self, symbol: str, exchange: Exchange, interval: Interval, start: datetime, end: datetime
    ) -> list[BarData]:
        """throughpastDataServiceGetHistoricalData"""
        req: HistoryRequest = HistoryRequest(
            symbol=symbol,
            exchange=exchange,
            interval=interval,
            start=start,
            end=end
        )
        data: list[BarData] = self.datafeed.query_bar_history(req, self.write_log)
        return data

    def process_tick_event(self, event: Event) -> None:
        """Market dataDataPush"""
        tick: TickData = event.data

        strategies: list = self.symbol_strategy_map[tick.vt_symbol]
        if not strategies:
            return

        for strategy in strategies:
            if strategy.inited:
                self.call_strategy_func(strategy, strategy.on_tick, tick)

    def process_order_event(self, event: Event) -> None:
        """OrderDataPush"""
        order: OrderData = event.data

        strategy: StrategyTemplate | None = self.orderid_strategy_map.get(order.vt_orderid, None)
        if not strategy:
            return

        self.call_strategy_func(strategy, strategy.update_order, order)

    def process_trade_event(self, event: Event) -> None:
        """Trade dataPush"""
        trade: TradeData = event.data

        # FilterDuplicateTradePush
        if trade.vt_tradeid in self.vt_tradeids:
            return
        self.vt_tradeids.add(trade.vt_tradeid)

        # PushtoStrategy
        strategy: StrategyTemplate | None = self.orderid_strategy_map.get(trade.vt_orderid, None)
        if not strategy:
            return

        self.call_strategy_func(strategy, strategy.update_trade, trade)

    def send_order(
        self,
        strategy: StrategyTemplate,
        vt_symbol: str,
        direction: Direction,
        offset: Offset,
        price: float,
        volume: float,
        lock: bool,
        net: bool,
    ) -> list:
        """SendOrder"""
        contract: ContractData | None = self.main_engine.get_contract(vt_symbol)
        if not contract:
            self.write_log(_("OrderFailed，Not found contract：{}").format(vt_symbol), strategy)
            return []

        price = round_to(price, contract.pricetick)
        volume = round_to(volume, contract.min_volume)

        original_req: OrderRequest = OrderRequest(
            symbol=contract.symbol,
            exchange=contract.exchange,
            direction=direction,
            offset=offset,
            type=OrderType.LIMIT,
            price=price,
            volume=volume,
            reference=f"{APP_NAME}_{strategy.strategy_name}"
        )

        req_list: list[OrderRequest] = self.main_engine.convert_order_request(
            original_req,
            contract.gateway_name,
            lock,
            net
        )

        vt_orderids: list = []

        for req in req_list:
            vt_orderid: str = self.main_engine.send_order(
                req, contract.gateway_name)

            if not vt_orderid:
                continue

            vt_orderids.append(vt_orderid)

            self.main_engine.update_order_request(req, vt_orderid, contract.gateway_name)

            self.orderid_strategy_map[vt_orderid] = strategy

        return vt_orderids

    def cancel_order(self, strategy: StrategyTemplate, vt_orderid: str) -> None:
        """Ordercancel order"""
        order: OrderData | None = self.main_engine.get_order(vt_orderid)
        if not order:
            self.write_log(f"cancel orderFailed，Not found order{vt_orderid}", strategy)
            return

        req: CancelRequest = order.create_cancel_request()
        self.main_engine.cancel_order(req, order.gateway_name)

    def cancel_all(self, strategy: StrategyTemplate) -> None:
        """Ordercancel order"""
        for vt_orderid in list(strategy.active_orderids):
            self.cancel_order(strategy, vt_orderid)

    def get_engine_type(self) -> EngineType:
        """GetEngineClasstype"""
        return self.engine_type

    def get_pricetick(self, strategy: StrategyTemplate, vt_symbol: str) -> float | None:
        """GetContractPricetick"""
        contract: ContractData | None = self.main_engine.get_contract(vt_symbol)

        if contract:
            pricetick: float = contract.pricetick
            return pricetick
        else:
            return None

    def get_size(self, strategy: StrategyTemplate, vt_symbol: str) -> int | None:
        """GetContractmultiplier"""
        contract: ContractData | None = self.main_engine.get_contract(vt_symbol)

        if contract:
            size: int = contract.size
            return size
        else:
            return None

    def load_bars(self, strategy: StrategyTemplate, days: int, interval: Interval) -> None:
        """LoadHistoricalData"""
        vt_symbols: list = strategy.vt_symbols
        dts_set: set[datetime] = set()
        history_data: dict[tuple, BarData] = {}

        # throughpastGateway、DataService、DatabaseGetHistoricalData
        for vt_symbol in vt_symbols:
            data: list[BarData] = self.load_bar(vt_symbol, days, interval)

            for bar in data:
                dts_set.add(bar.datetime)
                history_data[(bar.datetime, vt_symbol)] = bar

        dts: list[datetime] = list(dts_set)
        dts.sort()

        bars: dict = {}

        for dt in dts:
            for vt_symbol in vt_symbols:
                bar = history_data.get((dt, vt_symbol), None)

                # IfGetToContractspecifiedTimeHistoricalData，cacheintobarsDict
                if bar:
                    bars[vt_symbol] = bar
                # IfGetnotTo，butbarsDictinalreadyhaveContractDatacache, useBeforeDatapadding
                elif vt_symbol in bars:
                    old_bar: BarData = bars[vt_symbol]

                    bar = BarData(
                        symbol=old_bar.symbol,
                        exchange=old_bar.exchange,
                        datetime=dt,
                        open_price=old_bar.close_price,
                        high_price=old_bar.close_price,
                        low_price=old_bar.close_price,
                        close_price=old_bar.close_price,
                        gateway_name=old_bar.gateway_name
                    )
                    bars[vt_symbol] = bar

            self.call_strategy_func(strategy, strategy.on_bars, bars)

    def load_bar(self, vt_symbol: str, days: int, interval: Interval) -> list[BarData]:
        """LoadSingleContractHistoricalData"""
        symbol, exchange = extract_vt_symbol(vt_symbol)
        end: datetime = datetime.now(DB_TZ)
        start: datetime = end - timedelta(days)
        contract: ContractData | None = self.main_engine.get_contract(vt_symbol)
        data: list[BarData]

        # throughpastGatewayGetHistoricalData
        if contract and contract.history_data:
            req: HistoryRequest = HistoryRequest(
                symbol=symbol,
                exchange=exchange,
                interval=interval,
                start=start,
                end=end
            )
            data = self.main_engine.query_history(req, contract.gateway_name)

        # throughpastDataServiceGetHistoricalData
        else:
            data = self.query_bar_from_datafeed(symbol, exchange, interval, start, end)

        # throughpastDatabaseGetData
        if not data:
            data = self.database.load_bar_data(
                symbol=symbol,
                exchange=exchange,
                interval=interval,
                start=start,
                end=end,
            )

        return data

    def call_strategy_func(self, strategy: StrategyTemplate, func: Callable, params: object = None) -> None:
        """SecuritycallStrategyFunction"""
        try:
            if params:
                func(params)
            else:
                func()
        except Exception:
            strategy.trading = False
            strategy.inited = False

            msg: str = _("triggerExceptionalreadyStop\n{}").format(traceback.format_exc())
            self.write_log(msg, strategy)

    def add_strategy(
        self, class_name: str, strategy_name: str, vt_symbols: list, setting: dict
    ) -> None:
        """AddStrategyInstance"""
        if strategy_name in self.strategies:
            self.write_log(_("CreateStrategyFailed，Existduplicate name{}").format(strategy_name))
            return

        strategy_class: type[StrategyTemplate] | None = self.classes.get(class_name, None)
        if not strategy_class:
            self.write_log(_("CreateStrategyFailed，Not foundStrategyClass{}").format(class_name))
            return

        strategy: StrategyTemplate = strategy_class(self, strategy_name, vt_symbols, setting)
        self.strategies[strategy_name] = strategy

        for vt_symbol in vt_symbols:
            strategies: list = self.symbol_strategy_map[vt_symbol]
            strategies.append(strategy)

        self.save_strategy_setting()
        self.put_strategy_event(strategy)

    def init_strategy(self, strategy_name: str) -> None:
        """InitializeStrategy"""
        self.init_executor.submit(self._init_strategy, strategy_name)

    def _init_strategy(self, strategy_name: str) -> None:
        """InitializeStrategy"""
        strategy: StrategyTemplate = self.strategies[strategy_name]

        if strategy.inited:
            self.write_log(_("{}alreadyCompletedInitialize，forbidDuplicateoperate").format(strategy_name))
            return

        self.write_log(_("{}StartexecuteInitialize").format(strategy_name))

        # callStrategyon_initFunction
        self.call_strategy_func(strategy, strategy.on_init)

        # ResumeStrategyStatus
        data: dict | None = self.strategy_data.get(strategy_name, None)
        if data:
            for name in strategy.variables:
                value: object | None = data.get(name, None)
                if value is None:
                    continue

                # ForPositionandtargetDataDict，needneedusedict.updateUpdatedefaultdict
                if name in {"pos_data", "target_data"}:
                    strategy_data = getattr(strategy, name)
                    strategy_data.update(value)
                # ForOthersint/float/str/boolfieldthenCandirectlyassignvalue
                else:
                    setattr(strategy, name, value)

        # Subscribe market data
        for vt_symbol in strategy.vt_symbols:
            contract: ContractData | None = self.main_engine.get_contract(vt_symbol)
            if contract:
                req: SubscribeRequest = SubscribeRequest(
                    symbol=contract.symbol, exchange=contract.exchange)
                self.main_engine.subscribe(req, contract.gateway_name)
            else:
                self.write_log(_("Market dataSubscribeFailed，Not found contract{}").format(vt_symbol), strategy)

        # PushStrategyEventnotificationInitializeCompletedStatus
        strategy.inited = True
        self.put_strategy_event(strategy)
        self.write_log(_("{}InitializeCompleted").format(strategy_name))

    def start_strategy(self, strategy_name: str) -> None:
        """StartStrategy"""
        strategy: StrategyTemplate = self.strategies[strategy_name]
        if not strategy.inited:
            self.write_log(_("Strategy{}StartFailed，pleasefirstInitialize").format(strategy.strategy_name))
            return

        if strategy.trading:
            self.write_log(_("{}alreadyStart，do notDuplicateoperate").format(strategy_name))
            return

        # callStrategyon_startFunction
        self.call_strategy_func(strategy, strategy.on_start)

        # PushStrategyEventnotificationStartCompletedStatus
        strategy.trading = True
        self.put_strategy_event(strategy)

    def stop_strategy(self, strategy_name: str) -> None:
        """StopStrategy"""
        strategy: StrategyTemplate = self.strategies[strategy_name]
        if not strategy.trading:
            return

        # callStrategyon_stopFunction
        self.call_strategy_func(strategy, strategy.on_stop)

        # willTradingStatussetasFalse
        strategy.trading = False

        # CancelAllOrder
        self.cancel_all(strategy)

        # synchronousDataStatus
        self.sync_strategy_data(strategy)

        # PushStrategyEventnotificationStopCompletedStatus
        self.put_strategy_event(strategy)

    def edit_strategy(self, strategy_name: str, setting: dict) -> None:
        """editStrategyParameter"""
        strategy: StrategyTemplate = self.strategies[strategy_name]
        strategy.update_setting(setting)

        self.save_strategy_setting()
        self.put_strategy_event(strategy)

    def remove_strategy(self, strategy_name: str) -> bool:
        """removeStrategyInstance"""
        strategy: StrategyTemplate = self.strategies[strategy_name]
        if strategy.trading:
            self.write_log(_("Strategy{}removeFailed，pleasefirstStop").format(strategy.strategy_name))
            return False

        for vt_symbol in strategy.vt_symbols:
            strategies: list = self.symbol_strategy_map[vt_symbol]
            strategies.remove(strategy)

        for vt_orderid in strategy.active_orderids:
            if vt_orderid in self.orderid_strategy_map:
                self.orderid_strategy_map.pop(vt_orderid)

        self.strategies.pop(strategy_name)
        self.save_strategy_setting()

        self.strategy_data.pop(strategy_name, None)
        save_json(self.data_filename, self.strategy_data)

        return True

    def load_strategy_class(self) -> None:
        """LoadStrategyClass"""
        path1: Path = Path(__file__).parent.joinpath("strategies")
        self.load_strategy_class_from_folder(path1, "vnpy_portfoliostrategy.strategies")

        path2: Path = Path.cwd().joinpath("strategies")
        self.load_strategy_class_from_folder(path2, "strategies")

    def load_strategy_class_from_folder(self, path: Path, module_name: str = "") -> None:
        """throughpastspecifiedfolderLoadStrategyClass"""
        for suffix in ["py", "pyd", "so"]:
            pathname: str = str(path.joinpath(f"*.{suffix}"))
            for filepath in glob.glob(pathname):
                stem: str = Path(filepath).stem
                strategy_module_name: str = f"{module_name}.{stem}"
                self.load_strategy_class_from_module(strategy_module_name)

    def load_strategy_class_from_module(self, module_name: str) -> None:
        """throughpastStrategyfileLoadStrategyClass"""
        try:
            module: ModuleType = importlib.import_module(module_name)

            for name in dir(module):
                value = getattr(module, name)
                if (isinstance(value, type) and issubclass(value, StrategyTemplate) and value is not StrategyTemplate):
                    self.classes[value.__name__] = value
        except:  # noqa
            msg: str = _("Strategyfile{}LoadFailed，triggerException：\n{}").format(module_name, traceback.format_exc())
            self.write_log(msg)

    def load_strategy_data(self) -> None:
        """LoadStrategyData"""
        self.strategy_data = load_json(self.data_filename)

    def sync_strategy_data(self, strategy: StrategyTemplate) -> None:
        """SaveStrategyDataTofile"""
        data: dict = strategy.get_variables()
        data.pop("inited")      # notSaveStrategyStatusInfo
        data.pop("trading")

        self.strategy_data[strategy.strategy_name] = data
        save_json(self.data_filename, self.strategy_data)

    def get_all_strategy_class_names(self) -> list:
        """GetallLoadStrategyClassname"""
        return list(self.classes.keys())

    def get_strategy_class_parameters(self, class_name: str) -> dict:
        """GetStrategyClassParameter"""
        strategy_class: type[StrategyTemplate] = self.classes[class_name]

        parameters: dict = {}
        for name in strategy_class.parameters:
            parameters[name] = getattr(strategy_class, name)

        return parameters

    def get_strategy_parameters(self, strategy_name: str) -> dict:
        """GetStrategyParameter"""
        strategy: StrategyTemplate = self.strategies[strategy_name]
        return strategy.get_parameters()

    def init_all_strategies(self) -> None:
        """InitializeallStrategy"""
        for strategy_name in self.strategies.keys():
            self.init_strategy(strategy_name)

    def start_all_strategies(self) -> None:
        """StartallStrategy"""
        for strategy_name in self.strategies.keys():
            self.start_strategy(strategy_name)

    def stop_all_strategies(self) -> None:
        """StopallStrategy"""
        for strategy_name in self.strategies.keys():
            self.stop_strategy(strategy_name)

    def load_strategy_setting(self) -> None:
        """LoadStrategyConfig"""
        strategy_setting: dict = load_json(self.setting_filename)

        for strategy_name, strategy_config in strategy_setting.items():
            self.add_strategy(
                strategy_config["class_name"],
                strategy_name,
                strategy_config["vt_symbols"],
                strategy_config["setting"]
            )

    def save_strategy_setting(self) -> None:
        """SaveStrategyConfig"""
        strategy_setting: dict = {}

        for name, strategy in self.strategies.items():
            strategy_setting[name] = {
                "class_name": strategy.__class__.__name__,
                "vt_symbols": strategy.vt_symbols,
                "setting": strategy.get_parameters()
            }

        save_json(self.setting_filename, strategy_setting)

    def put_strategy_event(self, strategy: StrategyTemplate) -> None:
        """PushEventUpdateStrategyinterface"""
        data: dict = strategy.get_data()
        event: Event = Event(EVENT_PORTFOLIO_STRATEGY, data)
        self.event_engine.put(event)

    def write_log(self, msg: str, strategy: StrategyTemplate | None = None) -> None:
        """OutputLog"""
        if strategy:
            msg = f"{strategy.strategy_name}: {msg}"

        log: LogData = LogData(msg=msg, gateway_name=APP_NAME)
        event: Event = Event(type=EVENT_PORTFOLIO_LOG, data=log)
        self.event_engine.put(event)

    def send_email(self, msg: str, strategy: StrategyTemplate | None = None) -> None:
        """SendEmail"""
        if strategy:
            subject: str = f"{strategy.strategy_name}"
        else:
            subject = _("PortfolioStrategyEngine")

        self.main_engine.send_email(subject, msg)
