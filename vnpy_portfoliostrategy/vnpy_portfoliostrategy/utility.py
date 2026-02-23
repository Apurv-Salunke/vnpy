from datetime import datetime, time
from collections.abc import Callable

from vnpy.trader.object import BarData, TickData, Interval


class PortfolioBarGenerator:
    """PortfolioKlinelifecompleteer"""

    def __init__(
        self,
        on_bars: Callable,
        window: int = 0,
        on_window_bars: Callable | None = None,
        interval: Interval = Interval.MINUTE,
        daily_end: time | None = None
    ) -> None:
        """Constructor"""
        self.on_bars: Callable = on_bars

        self.interval: Interval = interval
        self.interval_count: int = 0

        self.bars: dict[str, BarData] = {}
        self.last_ticks: dict[str, TickData] = {}

        self.hour_bars: dict[str, BarData] = {}
        self.finished_hour_bars: dict[str, BarData] = {}

        self.daily_bars: dict[str, BarData] = {}
        self.finished_daily_bars: dict[str, BarData] = {}

        self.window: int = window
        self.window_bars: dict[str, BarData] = {}
        self.on_window_bars: Callable | None = on_window_bars

        self.last_dt: datetime | None = None

        self.daily_end: time | None = daily_end
        if self.interval == Interval.DAILY and not self.daily_end:
            raise RuntimeError("SyntheticdaysKlineMustpassineachdayscollectdiskTime")

    def update_tick(self, tick: TickData) -> None:
        """UpdateMarket datasliceData"""
        if not tick.last_price:
            return

        if self.last_dt and self.last_dt.minute != tick.datetime.minute:
            for bar in self.bars.values():
                bar.datetime = bar.datetime.replace(second=0, microsecond=0)

            self.on_bars(self.bars)
            self.bars = {}

        bar = self.bars.get(tick.vt_symbol, None)
        if not bar:
            bar = BarData(
                symbol=tick.symbol,
                exchange=tick.exchange,
                interval=Interval.MINUTE,
                datetime=tick.datetime,
                gateway_name=tick.gateway_name,
                open_price=tick.last_price,
                high_price=tick.last_price,
                low_price=tick.last_price,
                close_price=tick.last_price,
                open_interest=tick.open_interest
            )
            self.bars[bar.vt_symbol] = bar
        else:
            bar.high_price = max(bar.high_price, tick.last_price)
            bar.low_price = min(bar.low_price, tick.last_price)
            bar.close_price = tick.last_price
            bar.open_interest = tick.open_interest
            bar.datetime = tick.datetime

        last_tick: TickData | None = self.last_ticks.get(tick.vt_symbol, None)
        if last_tick:
            bar.volume += max(tick.volume - last_tick.volume, 0)
            bar.turnover += max(tick.turnover - last_tick.turnover, 0)

        self.last_ticks[tick.vt_symbol] = tick
        self.last_dt = tick.datetime

    def update_bars(self, bars: dict[str, BarData]) -> None:
        """UpdateoneminuteclockKline"""
        if self.interval == Interval.MINUTE:
            self.update_bar_minute_window(bars)
        elif self.interval == Interval.HOUR:
            self.update_bar_hour_window(bars)
        else:
            self.update_bar_daily_window(bars)

    def update_bar_minute_window(self, bars: dict[str, BarData]) -> None:
        """UpdateNminuteclockKline"""
        for vt_symbol, bar in bars.items():
            window_bar: BarData | None = self.window_bars.get(vt_symbol, None)

            # IfnoNminuteclockKlinethenCreate
            if not window_bar:
                dt: datetime = bar.datetime.replace(second=0, microsecond=0)
                window_bar = BarData(
                    symbol=bar.symbol,
                    exchange=bar.exchange,
                    datetime=dt,
                    gateway_name=bar.gateway_name,
                    open_price=bar.open_price,
                    high_price=bar.high_price,
                    low_price=bar.low_price
                )
                self.window_bars[vt_symbol] = window_bar

            # UpdateKlineinhigh priceandlow price
            else:
                window_bar.high_price = max(
                    window_bar.high_price,
                    bar.high_price
                )
                window_bar.low_price = min(
                    window_bar.low_price,
                    bar.low_price
                )

            # UpdateKlineinclose price、Volume、Turnover、Positionvolume
            window_bar.close_price = bar.close_price
            window_bar.volume += bar.volume
            window_bar.turnover += bar.turnover
            window_bar.open_interest = bar.open_interest

        # CheckKlinewhetherSyntheticcompletecomplete
        if not (bar.datetime.minute + 1) % self.window:
            if self.on_window_bars:
                self.on_window_bars(self.window_bars)
            self.window_bars = {}

    def update_bar_hour_window(self, bars: dict[str, BarData]) -> None:
        """UpdatesmalltimeKline"""
        for vt_symbol, bar in bars.items():
            hour_bar: BarData | None = self.hour_bars.get(vt_symbol, None)

            # IfnosmalltimeKlinethenCreate
            if not hour_bar:
                dt: datetime = bar.datetime.replace(minute=0, second=0, microsecond=0)
                hour_bar = BarData(
                    symbol=bar.symbol,
                    exchange=bar.exchange,
                    datetime=dt,
                    gateway_name=bar.gateway_name,
                    open_price=bar.open_price,
                    high_price=bar.high_price,
                    low_price=bar.low_price,
                    close_price=bar.close_price,
                    volume=bar.volume,
                    turnover=bar.turnover,
                    open_interest=bar.open_interest
                )
                self.hour_bars[vt_symbol] = hour_bar

            else:
                # IfcollectTo59minuteminuteclockKline，UpdatesmalltimeKlineandPush
                if bar.datetime.minute == 59:
                    hour_bar.high_price = max(
                        hour_bar.high_price,
                        bar.high_price
                    )
                    hour_bar.low_price = min(
                        hour_bar.low_price,
                        bar.low_price
                    )

                    hour_bar.close_price = bar.close_price
                    hour_bar.volume += bar.volume
                    hour_bar.turnover += bar.turnover
                    hour_bar.open_interest = bar.open_interest

                    self.finished_hour_bars[vt_symbol] = hour_bar
                    self.hour_bars[vt_symbol] = None

                # IfcollectToNewsmalltimeminuteclockKline，directlyPushCurrentsmalltimeKline
                elif bar.datetime.hour != hour_bar.datetime.hour:
                    self.finished_hour_bars[vt_symbol] = hour_bar

                    dt = bar.datetime.replace(minute=0, second=0, microsecond=0)
                    hour_bar = BarData(
                        symbol=bar.symbol,
                        exchange=bar.exchange,
                        datetime=dt,
                        gateway_name=bar.gateway_name,
                        open_price=bar.open_price,
                        high_price=bar.high_price,
                        low_price=bar.low_price,
                        close_price=bar.close_price,
                        volume=bar.volume,
                        turnover=bar.turnover,
                        open_interest=bar.open_interest
                    )
                    self.hour_bars[vt_symbol] = hour_bar

                # ElsedirectlyUpdatesmalltimeKline
                else:
                    hour_bar.high_price = max(
                        hour_bar.high_price,
                        bar.high_price
                    )
                    hour_bar.low_price = min(
                        hour_bar.low_price,
                        bar.low_price
                    )

                    hour_bar.close_price = bar.close_price
                    hour_bar.volume += bar.volume
                    hour_bar.turnover += bar.turnover
                    hour_bar.open_interest = bar.open_interest

        # PushSyntheticcompletecomplete smalltimeKline
        if self.finished_hour_bars:
            self.on_hour_bars(self.finished_hour_bars)
            self.finished_hour_bars = {}

    def update_bar_daily_window(self, bars: dict[str, BarData]) -> None:
        """UpdatedaysKline"""
        for vt_symbol, bar in bars.items():
            daily_bar: BarData | None = self.daily_bars.get(vt_symbol, None)

            # IfnodaysKlinethenCreate
            if not daily_bar:
                daily_bar = BarData(
                    symbol=bar.symbol,
                    exchange=bar.exchange,
                    datetime=bar.datetime,
                    gateway_name=bar.gateway_name,
                    open_price=bar.open_price,
                    high_price=bar.high_price,
                    low_price=bar.low_price
                )
                self.daily_bars[vt_symbol] = daily_bar
            # ElseUpdatehigh priceandlow price
            else:
                daily_bar.high_price = max(
                    daily_bar.high_price,
                    bar.high_price
                )
                daily_bar.low_price = min(
                    daily_bar.low_price,
                    bar.low_price
                )

            # Updateclose price、Tradevolume、Turnover、Positionvolume
            daily_bar.close_price = bar.close_price
            daily_bar.volume += bar.volume
            daily_bar.turnover += bar.turnover
            daily_bar.open_interest = bar.open_interest

            # CheckdaysKlinewhetherSyntheticcompletecomplete
            if bar.datetime.time() == self.daily_end:
                daily_bar.datetime = bar.datetime.replace(
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0
                )

                self.finished_daily_bars[vt_symbol] = daily_bar
                self.daily_bars[vt_symbol] = None

        # PushSyntheticcompletecompletedaysKline
        if self.finished_daily_bars:
            if self.on_window_bars:
                self.on_window_bars(self.finished_daily_bars)
            self.finished_daily_bars = {}

    def on_hour_bars(self, bars: dict[str, BarData]) -> None:
        """PushsmalltimeKline"""
        if self.window == 1:
            if self.on_window_bars:
                self.on_window_bars(bars)
        else:
            for vt_symbol, bar in bars.items():
                window_bar: BarData | None = self.window_bars.get(vt_symbol, None)
                if not window_bar:
                    window_bar = BarData(
                        symbol=bar.symbol,
                        exchange=bar.exchange,
                        datetime=bar.datetime,
                        gateway_name=bar.gateway_name,
                        open_price=bar.open_price,
                        high_price=bar.high_price,
                        low_price=bar.low_price
                    )
                    self.window_bars[vt_symbol] = window_bar
                else:
                    window_bar.high_price = max(
                        window_bar.high_price,
                        bar.high_price
                    )
                    window_bar.low_price = min(
                        window_bar.low_price,
                        bar.low_price
                    )

                window_bar.close_price = bar.close_price
                window_bar.volume += bar.volume
                window_bar.turnover += bar.turnover
                window_bar.open_interest = bar.open_interest

            self.interval_count += 1
            if not self.interval_count % self.window:
                self.interval_count = 0
                if self.on_window_bars:
                    self.on_window_bars(self.window_bars)
                self.window_bars = {}
