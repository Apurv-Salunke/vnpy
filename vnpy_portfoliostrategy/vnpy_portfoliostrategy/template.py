from abc import ABC, abstractmethod
from copy import copy
from collections import defaultdict
from typing import Any, cast

from vnpy.trader.constant import Interval, Direction, Offset
from vnpy.trader.object import BarData, TickData, OrderData, TradeData

from .base import EngineType


class StrategyTemplate(ABC):
    """PortfolioStrategytemplate"""

    author: str = ""
    parameters: list = []
    variables: list = []

    def __init__(
        self,
        strategy_engine: Any,
        strategy_name: str,
        vt_symbols: list[str],
        setting: dict
    ) -> None:
        """Constructor"""
        self.strategy_engine: Any = strategy_engine
        self.strategy_name: str = strategy_name
        self.vt_symbols: list[str] = vt_symbols

        # StatuscontrolVariable
        self.inited: bool = False
        self.trading: bool = False

        # PositionDataDict
        self.pos_data: dict[str, int] = defaultdict(int)        # ActualPosition
        self.target_data: dict[str, int] = defaultdict(int)     # targetPosition

        # Ordercachecontainerer
        self.orders: dict[str, OrderData] = {}
        self.active_orderids: set[str] = set()

        # copyVariablenameList，insertDefaultVariableincontainer
        self.variables: list = copy(self.variables)
        self.variables.insert(0, "inited")
        self.variables.insert(1, "trading")
        self.variables.insert(2, "pos_data")
        self.variables.insert(3, "target_data")

        # setStrategyParameter
        self.update_setting(setting)

    def update_setting(self, setting: dict) -> None:
        """setStrategyParameter"""
        for name in self.parameters:
            if name in setting:
                setattr(self, name, setting[name])

    @classmethod
    def get_class_parameters(cls) -> dict:
        """checkgetStrategyDefaultParameter"""
        class_parameters: dict = {}
        for name in cls.parameters:
            class_parameters[name] = getattr(cls, name)
        return class_parameters

    def get_parameters(self) -> dict:
        """QueryStrategyParameter"""
        strategy_parameters: dict = {}
        for name in self.parameters:
            strategy_parameters[name] = getattr(self, name)
        return strategy_parameters

    def get_variables(self) -> dict:
        """QueryStrategyVariable"""
        strategy_variables: dict = {}
        for name in self.variables:
            strategy_variables[name] = getattr(self, name)
        return strategy_variables

    def get_data(self) -> dict:
        """QueryStrategyStatusData"""
        strategy_data: dict = {
            "strategy_name": self.strategy_name,
            "vt_symbols": self.vt_symbols,
            "class_name": self.__class__.__name__,
            "author": self.author,
            "parameters": self.get_parameters(),
            "variables": self.get_variables(),
        }
        return strategy_data

    @abstractmethod
    def on_init(self) -> None:
        """StrategyInitializeCallback"""
        return

    def on_start(self) -> None:
        """StrategyStartCallback"""
        return

    def on_stop(self) -> None:
        """StrategyStopCallback"""
        return

    def on_tick(self, tick: TickData) -> None:
        """Market dataPushCallback"""
        return

    @abstractmethod
    def on_bars(self, bars: dict[str, BarData]) -> None:
        """KlinesliceCallback"""
        return

    def update_trade(self, trade: TradeData) -> None:
        """Trade dataUpdate"""
        if trade.direction == Direction.LONG:
            self.pos_data[trade.vt_symbol] += trade.volume
        else:
            self.pos_data[trade.vt_symbol] -= trade.volume

    def update_order(self, order: OrderData) -> None:
        """OrderDataUpdate"""
        self.orders[order.vt_orderid] = order

        if not order.is_active() and order.vt_orderid in self.active_orderids:
            self.active_orderids.remove(order.vt_orderid)

    def buy(self, vt_symbol: str, price: float, volume: float, lock: bool = False, net: bool = False) -> list[str]:
        """BuyOpen"""
        return self.send_order(vt_symbol, Direction.LONG, Offset.OPEN, price, volume, lock, net)

    def sell(self, vt_symbol: str, price: float, volume: float, lock: bool = False, net: bool = False) -> list[str]:
        """SellClose"""
        return self.send_order(vt_symbol, Direction.SHORT, Offset.CLOSE, price, volume, lock, net)

    def short(self, vt_symbol: str, price: float, volume: float, lock: bool = False, net: bool = False) -> list[str]:
        """SellOpen"""
        return self.send_order(vt_symbol, Direction.SHORT, Offset.OPEN, price, volume, lock, net)

    def cover(self, vt_symbol: str, price: float, volume: float, lock: bool = False, net: bool = False) -> list[str]:
        """BuyClose"""
        return self.send_order(vt_symbol, Direction.LONG, Offset.CLOSE, price, volume, lock, net)

    def send_order(
        self,
        vt_symbol: str,
        direction: Direction,
        offset: Offset,
        price: float,
        volume: float,
        lock: bool = False,
        net: bool = False,
    ) -> list[str]:
        """SendOrder"""
        if self.trading:
            vt_orderids: list = self.strategy_engine.send_order(
                self, vt_symbol, direction, offset, price, volume, lock, net
            )

            for vt_orderid in vt_orderids:
                self.active_orderids.add(vt_orderid)

            return vt_orderids
        else:
            return []

    def cancel_order(self, vt_orderid: str) -> None:
        """CancelOrder"""
        if self.trading:
            self.strategy_engine.cancel_order(self, vt_orderid)

    def cancel_all(self) -> None:
        """Cancel AllactiveOrder"""
        for vt_orderid in list(self.active_orderids):
            self.cancel_order(vt_orderid)

    def get_pos(self, vt_symbol: str) -> int:
        """QueryCurrentPosition"""
        return self.pos_data.get(vt_symbol, 0)

    def get_target(self, vt_symbol: str) -> int:
        """Querytargetposition"""
        return self.target_data[vt_symbol]

    def set_target(self, vt_symbol: str, target: int) -> None:
        """settargetposition"""
        self.target_data[vt_symbol] = target

    def rebalance_portfolio(self, bars: dict[str, BarData]) -> None:
        """Based ontargetexecuteadjustpositionTrading"""
        self.cancel_all()

        # onlysendoutCurrentKlineslicehaveMarket dataContractOrder
        for vt_symbol, bar in bars.items():
            # Calculateposition change
            target: int = self.get_target(vt_symbol)
            pos: int = self.get_pos(vt_symbol)
            diff: int = target - pos

            # Long
            if diff > 0:
                # CalculateLongOrderprice
                order_price: float = self.calculate_price(
                    vt_symbol,
                    Direction.LONG,
                    bar.close_price
                )

                # CalculatebidflatandbidopenVolume
                cover_volume: int = 0
                buy_volume: int = 0

                if pos < 0:
                    cover_volume = min(diff, abs(pos))
                    buy_volume = diff - cover_volume
                else:
                    buy_volume = diff

                # sendoutCorrespondingOrder
                if cover_volume:
                    self.cover(vt_symbol, order_price, cover_volume)

                if buy_volume:
                    self.buy(vt_symbol, order_price, buy_volume)
            # Short
            elif diff < 0:
                # CalculateShortOrderprice
                order_price = self.calculate_price(
                    vt_symbol,
                    Direction.SHORT,
                    bar.close_price
                )

                # CalculateaskflatandaskopenVolume
                sell_volume: int = 0
                short_volume: int = 0

                if pos > 0:
                    sell_volume = min(abs(diff), pos)
                    short_volume = abs(diff) - sell_volume
                else:
                    short_volume = abs(diff)

                # sendoutCorrespondingOrder
                if sell_volume:
                    self.sell(vt_symbol, order_price, sell_volume)

                if short_volume:
                    self.short(vt_symbol, order_price, short_volume)

    def calculate_price(
        self,
        vt_symbol: str,
        direction: Direction,
        reference: float
    ) -> float:
        """CalculateadjustpositionOrderPrice（supportpressneedreloadimplement）"""
        return reference

    def get_order(self, vt_orderid: str) -> OrderData | None:
        """QueryOrderData"""
        return self.orders.get(vt_orderid, None)

    def get_all_active_orderids(self) -> list[OrderData]:
        """GetAllactiveStatusOrder ID"""
        return list(self.active_orderids)

    def write_log(self, msg: str) -> None:
        """logLog"""
        self.strategy_engine.write_log(msg, self)

    def get_engine_type(self) -> EngineType:
        """QueryEngineClasstype"""
        return cast(EngineType, self.strategy_engine.get_engine_type())

    def get_pricetick(self, vt_symbol: str) -> float:
        """QueryContractminPricetick"""
        return cast(float, self.strategy_engine.get_pricetick(self, vt_symbol))

    def get_size(self, vt_symbol: str) -> int:
        """QueryContractmultiplier"""
        return cast(int, self.strategy_engine.get_size(self, vt_symbol))

    def load_bars(self, days: int, interval: Interval = Interval.MINUTE) -> None:
        """LoadHistoricalKlineDatatoexecuteInitialize"""
        self.strategy_engine.load_bars(self, days, interval)

    def put_event(self) -> None:
        """PushStrategyDataUpdateEvent"""
        if self.inited:
            self.strategy_engine.put_strategy_event(self)

    def send_email(self, msg: str) -> None:
        """SendEmailInfo"""
        if self.inited:
            self.strategy_engine.send_email(msg, self)

    def sync_data(self) -> None:
        """synchronousStrategyStatusDataTofile"""
        if self.trading:
            self.strategy_engine.sync_strategy_data(self)
