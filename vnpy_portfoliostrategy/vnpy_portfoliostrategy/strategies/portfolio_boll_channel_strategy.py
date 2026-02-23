from datetime import datetime

from vnpy.trader.utility import ArrayManager, Interval
from vnpy.trader.object import TickData, BarData

from vnpy_portfoliostrategy import StrategyTemplate, StrategyEngine
from vnpy_portfoliostrategy.utility import PortfolioBarGenerator


class PortfolioBollChannelStrategy(StrategyTemplate):
    """PortfolioBollingerchannelStrategy"""

    author = "usePythonTradinger"

    boll_window = 18
    boll_dev = 3.4
    cci_window = 10
    atr_window = 30
    sl_multiplier = 5.2
    fixed_size = 1
    price_add = 5

    parameters = [
        "boll_window",
        "boll_dev",
        "cci_window",
        "atr_window",
        "sl_multiplier",
        "fixed_size",
        "price_add"
    ]
    variables = []

    def __init__(
        self,
        strategy_engine: StrategyEngine,
        strategy_name: str,
        vt_symbols: list[str],
        setting: dict
    ) -> None:
        """Constructor"""
        super().__init__(strategy_engine, strategy_name, vt_symbols, setting)

        self.boll_up: dict[str, float] = {}
        self.boll_down: dict[str, float] = {}
        self.cci_value: dict[str, float] = {}
        self.atr_value: dict[str, float] = {}
        self.intra_trade_high: dict[str, float] = {}
        self.intra_trade_low: dict[str, float] = {}

        self.targets: dict[str, int] = {}
        self.last_tick_time: datetime | None = None

        # GetContractInfo
        self.ams: dict[str, ArrayManager] = {}
        for vt_symbol in self.vt_symbols:
            self.ams[vt_symbol] = ArrayManager()
            self.targets[vt_symbol] = 0

        self.pbg = PortfolioBarGenerator(self.on_bars, 2, self.on_2hour_bars, Interval.HOUR)

    def on_init(self) -> None:
        """StrategyInitializeCallback"""
        self.write_log("StrategyInitialize")

        self.load_bars(10)

    def on_start(self) -> None:
        """StrategyStartCallback"""
        self.write_log("StrategyStart")

    def on_stop(self) -> None:
        """StrategyStopCallback"""
        self.write_log("StrategyStop")

    def on_tick(self, tick: TickData) -> None:
        """Market dataPushCallback"""
        self.pbg.update_tick(tick)

    def on_bars(self, bars: dict[str, BarData]) -> None:
        """KlinesliceCallback"""
        self.pbg.update_bars(bars)

    def on_2hour_bars(self, bars: dict[str, BarData]) -> None:
        """2smalltimeKlineCallback"""
        self.cancel_all()

        # UpdateTocacheordercolumn
        for vt_symbol, bar in bars.items():
            am: ArrayManager = self.ams[vt_symbol]
            am.update_bar(bar)

        for vt_symbol, bar in bars.items():
            am = self.ams[vt_symbol]
            if not am.inited:
                return

            self.boll_up[vt_symbol], self.boll_down[vt_symbol] = am.boll(self.boll_window, self.boll_dev)
            self.cci_value[vt_symbol] = am.cci(self.cci_window)
            self.atr_value[vt_symbol] = am.atr(self.atr_window)

            # Calculatetargetposition
            current_pos = self.get_pos(vt_symbol)
            if current_pos == 0:
                self.intra_trade_high[vt_symbol] = bar.high_price
                self.intra_trade_low[vt_symbol] = bar.low_price

                if self.cci_value[vt_symbol] > 0:
                    self.targets[vt_symbol] = self.fixed_size
                elif self.cci_value[vt_symbol] < 0:
                    self.targets[vt_symbol] = -self.fixed_size

            elif current_pos > 0:
                self.intra_trade_high[vt_symbol] = max(self.intra_trade_high[vt_symbol], bar.high_price)
                self.intra_trade_low[vt_symbol] = bar.low_price

                long_stop = self.intra_trade_high[vt_symbol] - self.atr_value[vt_symbol] * self.sl_multiplier

                if bar.close_price <= long_stop:
                    self.targets[vt_symbol] = 0

            elif current_pos < 0:
                self.intra_trade_low[vt_symbol] = min(self.intra_trade_low[vt_symbol], bar.low_price)
                self.intra_trade_high[vt_symbol] = bar.high_price

                short_stop = self.intra_trade_low[vt_symbol] + self.atr_value[vt_symbol] * self.sl_multiplier

                if bar.close_price >= short_stop:
                    self.targets[vt_symbol] = 0

        # Based ontargetpositionintorowOrder
        for vt_symbol in self.vt_symbols:
            target_pos = self.targets[vt_symbol]
            current_pos = self.get_pos(vt_symbol)

            pos_diff = target_pos - current_pos
            volume = abs(pos_diff)
            bar = bars[vt_symbol]
            boll_up = self.boll_up[vt_symbol]
            boll_down = self.boll_down[vt_symbol]

            if pos_diff > 0:
                price = bar.close_price + self.price_add

                if current_pos < 0:
                    self.cover(vt_symbol, price, volume)
                else:
                    self.buy(vt_symbol, boll_up, volume)

            elif pos_diff < 0:
                price = bar.close_price - self.price_add

                if current_pos > 0:
                    self.sell(vt_symbol, price, volume)
                else:
                    self.short(vt_symbol, boll_down, volume)

        # PushinterfaceUpdate
        self.put_event()
