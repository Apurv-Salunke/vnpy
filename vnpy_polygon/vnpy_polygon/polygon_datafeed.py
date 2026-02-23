from datetime import datetime
from typing import Any
from collections.abc import Iterator, Callable

from polygon import RESTClient
from polygon.rest.aggs import Agg

from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.object import BarData, TickData, HistoryRequest
from vnpy.trader.datafeed import BaseDatafeed
from vnpy.trader.setting import SETTINGS
from vnpy.trader.database import DB_TZ


INTERVAL_VT2POLYGON = {
    Interval.MINUTE: "minute",
    Interval.HOUR: "hour",
    Interval.DAILY: "day",
}


class PolygonDatafeed(BaseDatafeed):
    """Polygon.ioDataServiceGateway"""

    def __init__(self) -> None:
        """"""
        self.api_key: str = SETTINGS["datafeed.password"]

        self.client: RESTClient
        self.inited: bool = False

    def init(self, output: Callable[[str], Any] = print) -> bool:
        """Initialize"""
        if self.inited:
            return True

        if not self.api_key:
            output("Polygon.ioDataServiceInitializeFailed：APIkeyIs empty！")
            return False

        try:
            self.client = RESTClient(self.api_key)

            self.client.get_exchanges(asset_class='options')
        except Exception as e:
            output(f"Polygon.ioDataServiceInitializeFailed：{e}")
            return False

        self.inited = True
        return True

    def query_bar_history(self, req: HistoryRequest, output: Callable[[str], Any] = print) -> list[BarData]:
        """QueryKlineData"""
        if not self.inited:
            n: bool = self.init(output)
            if not n:
                return []

        symbol: str = req.symbol
        exchange: Exchange = req.exchange
        interval: Interval = req.interval
        start: datetime = req.start
        end: datetime = req.end

        polygon_interval: str | None = INTERVAL_VT2POLYGON.get(interval)
        if not polygon_interval:
            output(f"Polygon.ioQueryKlineDataFailed：Not supportedTimecycle{interval.value}")
            return []

        if len(symbol) > 10:
            symbol = "O:" + symbol  # PolygonneedrequestOptionCodebeforeaddO:beforesuffix

        # polygonClientlist_aggsMethodReturnoneProcessminutepageIterationer
        aggs: Iterator[Agg] = self.client.list_aggs(
            ticker=symbol,
            multiplier=1,
            timespan=polygon_interval,
            from_=start,
            to=end,
            limit=5000      # eachtimescheck5000strip
        )

        bars: list[BarData] = []
        for agg in aggs:
            # PolygonTimestampismilliseconds，convertasdatetime
            dt: datetime = datetime.fromtimestamp(agg.timestamp / 1000)

            # list_aggscanableReturnexceedoutRequestrangeData，toneedneedFilter
            if not (start <= dt <= end):
                continue

            bar: BarData = BarData(
                symbol=req.symbol,
                exchange=exchange,
                datetime=dt.replace(tzinfo=DB_TZ),
                interval=interval,
                volume=agg.volume,
                open_price=agg.open,
                high_price=agg.high,
                low_price=agg.low,
                close_price=agg.close,
                turnover=agg.vwap * agg.volume,
                gateway_name="POLYGON"
            )
            bars.append(bar)

        return bars

    def query_tick_history(self, req: HistoryRequest, output: Callable[[str], Any] = print) -> list[TickData]:
        """QueryTickData"""
        return []
