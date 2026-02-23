from datetime import datetime

import numpy as np

from vnpy.trader.utility import BarGenerator
from vnpy.trader.object import TickData, BarData
from vnpy.trader.constant import Direction

from vnpy_portfoliostrategy import StrategyTemplate, StrategyEngine


class PairTradingStrategy(StrategyTemplate):
    """configforTradingStrategy"""

    author = "usePythonTradinger"

    tick_add = 1
    boll_window = 20
    boll_dev = 2
    fixed_size = 1
    leg1_ratio = 1
    leg2_ratio = 1

    leg1_symbol = ""
    leg2_symbol = ""
    current_spread = 0.0
    boll_mid = 0.0
    boll_down = 0.0
    boll_up = 0.0

    parameters = [
        "tick_add",
        "boll_window",
        "boll_dev",
        "fixed_size",
        "leg1_ratio",
        "leg2_ratio",
    ]
    variables = [
        "leg1_symbol",
        "leg2_symbol",
        "current_spread",
        "boll_mid",
        "boll_down",
        "boll_up",
    ]

    def __init__(
        self,
        strategy_engine: StrategyEngine,
        strategy_name: str,
        vt_symbols: list[str],
        setting: dict
    ) -> None:
        """Constructor"""
        super().__init__(strategy_engine, strategy_name, vt_symbols, setting)

        self.bgs: dict[str, BarGenerator] = {}
        self.last_tick_time: datetime | None = None

        self.spread_count: int = 0
        self.spread_data: np.ndarray = np.zeros(100)

        # Obtain contract info
        self.leg1_symbol, self.leg2_symbol = vt_symbols

        def on_bar(bar: BarData) -> None:
            """"""
            pass

        for vt_symbol in self.vt_symbols:
            self.bgs[vt_symbol] = BarGenerator(on_bar)

    def on_init(self) -> None:
        """StrategyInitializeCallback"""
        self.write_log("StrategyInitialize")

        self.load_bars(1)

    def on_start(self) -> None:
        """StrategyStartCallback"""
        self.write_log("StrategyStart")

    def on_stop(self) -> None:
        """StrategyStopCallback"""
        self.write_log("StrategyStop")

    def on_tick(self, tick: TickData) -> None:
        """Market dataPushCallback"""
        if (
            self.last_tick_time
            and self.last_tick_time.minute != tick.datetime.minute
        ):
            bars = {}
            for vt_symbol, bg in self.bgs.items():
                bars[vt_symbol] = bg.generate()
            self.on_bars(bars)

        bg = self.bgs[tick.vt_symbol]
        bg.update_tick(tick)

        self.last_tick_time = tick.datetime

    def on_bars(self, bars: dict[str, BarData]) -> None:
        """KlinesliceCallback"""
        # GetOptionlegKline
        leg1_bar = bars.get(self.leg1_symbol, None)
        leg2_bar = bars.get(self.leg2_symbol, None)

        # MusttwoOptionlegMarket dataallExist
        if not leg1_bar or not leg2_bar:
            return

        # each5minuteclockRunningonce
        if (leg1_bar.datetime.minute + 1) % 5:
            return

        # CalculateCurrentSpread
        self.current_spread = leg1_bar.close_price * self.leg1_ratio - leg2_bar.close_price * self.leg2_ratio

        # UpdateToSpreadordercolumn
        self.spread_data[:-1] = self.spread_data[1:]
        self.spread_data[-1] = self.current_spread

        self.spread_count += 1
        if self.spread_count <= self.boll_window:
            return

        # CalculateBollinger
        buf: np.ndarray = self.spread_data[-self.boll_window:]

        std = buf.std()
        self.boll_mid = buf.mean()
        self.boll_up = self.boll_mid + self.boll_dev * std
        self.boll_down = self.boll_mid - self.boll_dev * std

        # CalculatetargetPosition
        leg1_pos = self.get_pos(self.leg1_symbol)

        if not leg1_pos:
            if self.current_spread >= self.boll_up:
                self.set_target(self.leg1_symbol, -self.fixed_size)
                self.set_target(self.leg2_symbol, self.fixed_size)
            elif self.current_spread <= self.boll_down:
                self.set_target(self.leg1_symbol, self.fixed_size)
                self.set_target(self.leg2_symbol, -self.fixed_size)
        elif leg1_pos > 0:
            if self.current_spread >= self.boll_mid:
                self.set_target(self.leg1_symbol, 0)
                self.set_target(self.leg2_symbol, 0)
        else:
            if self.current_spread <= self.boll_mid:
                self.set_target(self.leg1_symbol, 0)
                self.set_target(self.leg2_symbol, 0)

        # executeadjustpositionTrading
        self.rebalance_portfolio(bars)

        # PushUpdateEvent
        self.put_event()

    def calculate_price(self, vt_symbol: str, direction: Direction, reference: float) -> float:
        """CalculateadjustpositionOrderPrice（supportpressneedreloadimplement）"""
        pricetick: float = self.get_pricetick(vt_symbol)

        if direction == Direction.LONG:
            price: float = reference + self.tick_add * pricetick
        else:
            price = reference - self.tick_add * pricetick

        return price
