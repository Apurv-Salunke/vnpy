from collections.abc import Callable
from time import time

from vnpy_ctastrategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData
)


class TestStrategy(CtaTemplate):
    """"""
    author = "usePythonTradinger"

    test_trigger: int = 10

    tick_count: int = 0
    test_all_done: bool = False

    parameters = ["test_trigger"]
    variables = ["tick_count", "test_all_done"]

    def on_init(self) -> None:
        """
        Callback when strategy is inited.
        """
        self.write_log("StrategyInitialize")

        self.test_funcs: list[Callable[[], None]] = [
            self.test_market_order,
            self.test_limit_order,
            self.test_cancel_all,
            self.test_stop_order
        ]

        self.last_tick: TickData | None = None

    def on_start(self) -> None:
        """
        Callback when strategy is started.
        """
        self.write_log("StrategyStart")

    def on_stop(self) -> None:
        """
        Callback when strategy is stopped.
        """
        self.write_log("StrategyStop")

    def on_tick(self, tick: TickData) -> None:
        """
        Callback of new tick data update.
        """
        if self.test_all_done:
            return

        self.last_tick = tick

        self.tick_count += 1
        if self.tick_count >= self.test_trigger:
            self.tick_count = 0

            if self.test_funcs:
                test_func: Callable[[], None] = self.test_funcs.pop(0)

                start: float = time()
                test_func()
                time_cost: float = (time() - start) * 1000
                self.write_log(f"consumetime{time_cost}milliseconds")
            else:
                self.write_log("TestalreadyAllCompleted")
                self.test_all_done = True

        self.put_event()

    def on_bar(self, bar: BarData) -> None:
        """
        Callback of new bar data update.
        """
        pass

    def on_order(self, order: OrderData) -> None:
        """
        Callback of new order data update.
        """
        self.put_event()

    def on_trade(self, trade: TradeData) -> None:
        """
        Callback of new trade data update.
        """
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder) -> None:
        """
        Callback of stop order update.
        """
        self.put_event()

    def test_market_order(self) -> None:
        """"""
        if not self.last_tick:
            self.write_log("nomostNewtickData")
            return

        self.buy(self.last_tick.limit_up, 1)
        self.write_log("executemarket priceorderTest")

    def test_limit_order(self) -> None:
        """"""
        if not self.last_tick:
            self.write_log("nomostNewtickData")
            return

        self.buy(self.last_tick.limit_down, 1)
        self.write_log("executelimit priceorderTest")

    def test_stop_order(self) -> None:
        """"""
        if not self.last_tick:
            self.write_log("nomostNewtickData")
            return

        self.buy(self.last_tick.ask_price_1, 1, True)
        self.write_log("executeStoporderTest")

    def test_cancel_all(self) -> None:
        """"""
        self.cancel_all()
        self.write_log("executeAllcancel orderTest")
