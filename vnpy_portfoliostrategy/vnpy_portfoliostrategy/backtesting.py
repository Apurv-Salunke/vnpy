from collections import defaultdict
from datetime import date, datetime, timedelta
from functools import lru_cache, partial
from copy import copy
import traceback

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pandas import DataFrame
from collections.abc import Callable

from vnpy.trader.constant import Direction, Offset, Interval, Status
from vnpy.trader.database import get_database, BaseDatabase
from vnpy.trader.object import OrderData, TradeData, BarData
from vnpy.trader.utility import round_to, extract_vt_symbol
from vnpy.trader.optimize import (
    OptimizationSetting,
    check_optimization_setting,
    run_bf_optimization,
    run_ga_optimization
)

from .base import EngineType
from .locale import _
from .template import StrategyTemplate


INTERVAL_DELTA_MAP: dict[Interval, timedelta] = {
    Interval.MINUTE: timedelta(minutes=1),
    Interval.HOUR: timedelta(hours=1),
    Interval.DAILY: timedelta(days=1),
}


class BacktestingEngine:
    """PortfolioStrategyBacktestEngine"""

    engine_type: EngineType = EngineType.BACKTESTING
    gateway_name: str = "BACKTESTING"

    def __init__(self) -> None:
        """Constructor"""
        self.vt_symbols: list[str] = []
        self.start: datetime
        self.end: datetime

        self.rates: dict[str, float]
        self.slippages: dict[str, float]
        self.sizes: dict[str, float]
        self.priceticks: dict[str, float]

        self.capital: float = 1_000_000
        self.risk_free: float = 0
        self.annual_days: int = 240

        self.strategy_class: type[StrategyTemplate]
        self.strategy: StrategyTemplate
        self.bars: dict[str, BarData] = {}
        self.datetime: datetime = datetime(1970, 1, 1)

        self.interval: Interval
        self.days: int = 0
        self.history_data: dict[tuple, BarData] = {}
        self.dts: set[datetime] = set()

        self.limit_order_count: int = 0
        self.limit_orders: dict[str, OrderData] = {}
        self.active_limit_orders: dict[str, OrderData] = {}

        self.trade_count: int = 0
        self.trades: dict[str, TradeData] = {}

        self.logs: list = []

        self.daily_results: dict[date, PortfolioDailyResult] = {}
        self.daily_df: DataFrame = None

    def clear_data(self) -> None:
        """cleanupuptimesBacktestcacheData"""
        self.limit_order_count = 0
        self.limit_orders.clear()
        self.active_limit_orders.clear()

        self.trade_count = 0
        self.trades.clear()

        self.logs.clear()
        self.daily_results.clear()
        self.daily_df = None

    def set_parameters(
        self,
        vt_symbols: list[str],
        interval: Interval,
        start: datetime,
        rates: dict[str, float],
        slippages: dict[str, float],
        sizes: dict[str, float],
        priceticks: dict[str, float],
        capital: float = 0,
        end: datetime | None = None,
        risk_free: float = 0,
        annual_days: int = 240
    ) -> None:
        """setParameter"""
        self.vt_symbols = vt_symbols
        self.interval = interval

        self.rates = rates
        self.slippages = slippages
        self.sizes = sizes
        self.priceticks = priceticks

        self.start = start
        if not end:
            self.end = datetime.now()
        else:
            self.end = end.replace(hour=23, minute=59, second=59)

        self.capital = capital
        self.risk_free = risk_free
        self.annual_days = annual_days

    def add_strategy(self, strategy_class: type[StrategyTemplate], setting: dict) -> None:
        """increaseStrategy"""
        self.strategy_class = strategy_class
        self.strategy = strategy_class(
            self, strategy_class.__name__, copy(self.vt_symbols), setting
        )

    def load_data(self) -> None:
        """LoadHistoricalData"""
        self.output(_("StartLoadHistoricalData"))

        if not self.end:
            self.end = datetime.now()

        if self.start >= self.end:
            self.output(_("startdaysperiodMustsmallatFinisheddaysperiod"))
            return

        # cleanupuptimesLoadHistoricalData
        self.history_data.clear()
        self.dts.clear()

        # eachtimesLoad30dayHistoricalData
        progress_delta: timedelta = timedelta(days=30)
        total_delta: timedelta = self.end - self.start
        interval_delta: timedelta = INTERVAL_DELTA_MAP[self.interval]

        for vt_symbol in self.vt_symbols:
            if self.interval == Interval.MINUTE:
                start: datetime = self.start
                end: datetime = self.start + progress_delta
                progress: float = 0

                data_count = 0
                while start < self.end:
                    end = min(end, self.end)

                    data: list[BarData] = load_bar_data(
                        vt_symbol,
                        self.interval,
                        start,
                        end
                    )

                    for bar in data:
                        self.dts.add(bar.datetime)
                        self.history_data[(bar.datetime, vt_symbol)] = bar
                        data_count += 1

                    progress += progress_delta / total_delta
                    progress = min(progress, 1)
                    progress_bar = "#" * int(progress * 10)
                    self.output(_("{}Loadintodegree：{} [{:.0%}]").format(
                        vt_symbol, progress_bar, progress
                    ))

                    start = end + interval_delta
                    end += (progress_delta + interval_delta)
            else:
                data = load_bar_data(
                    vt_symbol,
                    self.interval,
                    self.start,
                    self.end
                )

                for bar in data:
                    self.dts.add(bar.datetime)
                    self.history_data[(bar.datetime, vt_symbol)] = bar

                data_count = len(data)

            self.output(_("{}HistoricalDataLoadCompleted，Datavolume：{}").format(vt_symbol, data_count))

        self.output(_("allHistoricalDataLoadCompleted"))

    def run_backtesting(self) -> None:
        """StartBacktest"""
        self.strategy.on_init()

        dts: list = list(self.dts)
        dts.sort()

        # usespecifiedTimeHistoricalDataInitializeStrategy
        day_count: int = 0
        _ix: int = 0

        for _ix, dt in enumerate(dts):
            if self.datetime and dt.day != self.datetime.day:
                day_count += 1
                if day_count >= self.days:
                    break

            try:
                self.new_bars(dt)
            except Exception:
                self.output(_("triggerException，Backtestterminate"))
                self.output(traceback.format_exc())
                return

        self.strategy.inited = True
        self.output(_("StrategyInitializeCompleted"))

        self.strategy.on_start()
        self.strategy.trading = True
        self.output(_("StartreturnputHistoricalData"))

        # useremainingHistoricalDataintorowStrategyBacktest
        for dt in dts[_ix:]:
            try:
                self.new_bars(dt)
            except Exception:
                self.output(_("triggerException，Backtestterminate"))
                self.output(traceback.format_exc())
                return

        self.output(_("HistoricalDatareturnputFinished"))

    def calculate_result(self) -> DataFrame:
        """Calculateone by onedayswatchmarketPnL"""
        self.output(_("StartCalculateone by onedayswatchmarketPnL"))

        if not self.trades:
            self.output(_("TradelogIs empty，unableCalculate"))
            return

        for trade in self.trades.values():
            d: date = trade.datetime.date()
            daily_result: PortfolioDailyResult = self.daily_results[d]
            daily_result.add_trade(trade)

        pre_closes: dict = {}
        start_poses: dict = {}

        for daily_result in self.daily_results.values():
            daily_result.calculate_pnl(
                pre_closes,
                start_poses,
                self.sizes,
                self.rates,
                self.slippages,
            )

            pre_closes = daily_result.close_prices
            start_poses = daily_result.end_poses

        results: dict = defaultdict(list)

        for daily_result in self.daily_results.values():
            fields: list = [
                "date", "trade_count", "turnover",
                "commission", "slippage", "trading_pnl",
                "holding_pnl", "total_pnl", "net_pnl"
            ]
            for key in fields:
                value = getattr(daily_result, key)
                results[key].append(value)

        if results:
            self.daily_df = DataFrame.from_dict(results).set_index("date")

        self.output(_("one by onedayswatchmarketPnLCalculateCompleted"))
        return self.daily_df

    def calculate_statistics(self, df: DataFrame = None, output: bool = True) -> dict:
        """CalculateStrategystatisticsindicator"""
        self.output(_("StartCalculateStrategystatisticsindicator"))

        if df is None:
            df = self.daily_df

        # Initializestatisticsindicator
        start_date: str = ""
        end_date: str = ""
        total_days: int = 0
        profit_days: int = 0
        loss_days: int = 0
        end_balance: float = 0
        max_drawdown: float = 0
        max_ddpercent: float = 0
        max_drawdown_duration: int = 0
        total_net_pnl: float = 0
        daily_net_pnl: float = 0
        total_commission: float = 0
        daily_commission: float = 0
        total_slippage: float = 0
        daily_slippage: float = 0
        total_turnover: float = 0
        daily_turnover: float = 0
        total_trade_count: int = 0
        daily_trade_count: float = 0
        total_return: float = 0
        annual_return: float = 0
        daily_return: float = 0
        return_std: float = 0
        sharpe_ratio: float = 0
        return_drawdown_ratio: float = 0

        # Checkwhetheroccurpastliquidation
        positive_balance: bool = False

        # CalculateAccountrelatedindicator
        if df is not None:
            df["balance"] = df["net_pnl"].cumsum() + self.capital
            df["return"] = np.log(df["balance"] / df["balance"].shift(1)).fillna(0)
            df["highlevel"] = df["balance"].rolling(min_periods=1, window=len(df), center=False).max()
            df["drawdown"] = df["balance"] - df["highlevel"]
            df["ddpercent"] = df["drawdown"] / df["highlevel"] * 100

            # Checkwhetheroccurpastliquidation
            positive_balance = (df["balance"] > 0).all()
            if not positive_balance:
                self.output(_("Backtestinoutappearliquidation（Accountsmallatetcat0），unableCalculateStrategystatisticsindicator"))

        # Calculatestatisticsindicator
        if positive_balance:
            start_date = df.index[0]
            end_date = df.index[-1]

            total_days = len(df)
            profit_days = len(df[df["net_pnl"] > 0])
            loss_days= len(df[df["net_pnl"] < 0])

            end_balance = df["balance"].iloc[-1]
            max_drawdown = df["drawdown"].min()
            max_ddpercent = df["ddpercent"].min()
            max_drawdown_end = df["drawdown"].idxmin()

            if isinstance(max_drawdown_end, date):
                max_drawdown_start = df["balance"][:max_drawdown_end].idxmax()          # type: ignore
                max_drawdown_duration = (max_drawdown_end - max_drawdown_start).days
            else:
                max_drawdown_duration = 0

            total_net_pnl = df["net_pnl"].sum()
            daily_net_pnl = total_net_pnl / total_days

            total_commission = df["commission"].sum()
            daily_commission = total_commission / total_days

            total_slippage = df["slippage"].sum()
            daily_slippage = total_slippage / total_days

            total_turnover = df["turnover"].sum()
            daily_turnover = total_turnover / total_days

            total_trade_count = df["trade_count"].sum()
            daily_trade_count = total_trade_count / total_days

            total_return = (end_balance / self.capital - 1) * 100
            annual_return = total_return / total_days * self.annual_days
            daily_return = df["return"].mean() * 100
            return_std = df["return"].std() * 100

            if return_std:
                daily_risk_free: float = self.risk_free / np.sqrt(self.annual_days)
                sharpe_ratio = (daily_return - daily_risk_free) / return_std * np.sqrt(self.annual_days)
            else:
                sharpe_ratio = 0

            return_drawdown_ratio = -total_net_pnl / max_drawdown

        # Outputresult
        if output:
            self.output("-" * 30)
            self.output(_("firstTradingdays：\t{}").format(start_date))
            self.output(_("mostafterTradingdays：\t{}").format(end_date))

            self.output(_("TotalTradingdays：\t{}").format(total_days))
            self.output(_("profitTradingdays：\t{}").format(profit_days))
            self.output(_("lossTradingdays：\t{}").format(loss_days))

            self.output(_("startAccount：\t{:,.2f}").format(self.capital))
            self.output(_("FinishedAccount：\t{:,.2f}").format(end_balance))

            self.output(_("Totalreturn rate：\t{:,.2f}%").format(total_return))
            self.output(_("yearizereturn：\t{:,.2f}%").format(annual_return))
            self.output(_("max drawdown: \t{:,.2f}").format(max_drawdown))
            self.output(_("hundredminuteratiomax drawdown: {:,.2f}%").format(max_ddpercent))
            self.output(_("max lengthdrawdowndaynumber: \t{}").format(max_drawdown_duration))

            self.output(_("Total PnL：\t{:,.2f}").format(total_net_pnl))
            self.output(_("Totalfee：\t{:,.2f}").format(total_commission))
            self.output(_("Totalslippage：\t{:,.2f}").format(total_slippage))
            self.output(_("TotalTradeamount：\t{:,.2f}").format(total_turnover))
            self.output(_("TotalTradecount：\t{}").format(total_trade_count))

            self.output(_("daysavgPnL：\t{:,.2f}").format(daily_net_pnl))
            self.output(_("daysavgfee：\t{:,.2f}").format(daily_commission))
            self.output(_("daysavgslippage：\t{:,.2f}").format(daily_slippage))
            self.output(_("daysavgTradeamount：\t{:,.2f}").format(daily_turnover))
            self.output(_("daysavgTradecount：\t{}").format(daily_trade_count))

            self.output(_("daysavgreturn rate：\t{:,.2f}%").format(daily_return))
            self.output(_("returnstandarddiff：\t{:,.2f}%").format(return_std))
            self.output(f"Sharpe Ratio：\t{sharpe_ratio:,.2f}")
            self.output(_("returndrawdownratio：\t{:,.2f}").format(return_drawdown_ratio))

        statistics: dict = {
            "start_date": start_date,
            "end_date": end_date,
            "total_days": total_days,
            "profit_days": profit_days,
            "loss_days": loss_days,
            "capital": self.capital,
            "end_balance": end_balance,
            "max_drawdown": max_drawdown,
            "max_ddpercent": max_ddpercent,
            "max_drawdown_duration": max_drawdown_duration,
            "total_net_pnl": total_net_pnl,
            "daily_net_pnl": daily_net_pnl,
            "total_commission": total_commission,
            "daily_commission": daily_commission,
            "total_slippage": total_slippage,
            "daily_slippage": daily_slippage,
            "total_turnover": total_turnover,
            "daily_turnover": daily_turnover,
            "total_trade_count": total_trade_count,
            "daily_trade_count": daily_trade_count,
            "total_return": total_return,
            "annual_return": annual_return,
            "daily_return": daily_return,
            "return_std": return_std,
            "sharpe_ratio": sharpe_ratio,
            "return_drawdown_ratio": return_drawdown_ratio,
        }

        # Filterextremevalue
        for key, value in statistics.items():
            if value in (np.inf, -np.inf):
                value = 0
            statistics[key] = np.nan_to_num(value)

        self.output(_("StrategystatisticsindicatorCalculateCompleted"))
        return statistics

    def show_chart(self, df: DataFrame = None) -> None:
        """Displaychart"""
        if df is None:
            df = self.daily_df

        if df is None:
            return

        fig = make_subplots(
            rows=4,
            cols=1,
            subplot_titles=["Balance", "Drawdown", "Daily Pnl", "Pnl Distribution"],
            vertical_spacing=0.06
        )

        balance_line = go.Scatter(
            x=df.index,
            y=df["balance"],
            mode="lines",
            name="Balance"
        )
        drawdown_scatter = go.Scatter(
            x=df.index,
            y=df["drawdown"],
            fillcolor="red",
            fill='tozeroy',
            mode="lines",
            name="Drawdown"
        )
        pnl_bar = go.Bar(y=df["net_pnl"], name="Daily Pnl")
        pnl_histogram = go.Histogram(x=df["net_pnl"], nbinsx=100, name="Days")

        fig.add_trace(balance_line, row=1, col=1)
        fig.add_trace(drawdown_scatter, row=2, col=1)
        fig.add_trace(pnl_bar, row=3, col=1)
        fig.add_trace(pnl_histogram, row=4, col=1)

        fig.update_layout(height=1000, width=1000)
        fig.show()

    def run_bf_optimization(
        self,
        optimization_setting: OptimizationSetting,
        output: bool = True,
        max_workers: int | None = None
    ) -> list:
        """violentforceexhaustiveOptimization"""
        if not check_optimization_setting(optimization_setting):
            return []

        evaluate_func: Callable = wrap_evaluate(self, optimization_setting.target_name)
        results: list = run_bf_optimization(
            evaluate_func,
            optimization_setting,
            get_target_value,
            max_workers=max_workers,
            output=self.output,
        )

        if output:
            for result in results:
                msg: str = _("Parameter：{}, target：{}").format(result[0], result[1])
                self.output(msg)

        return results

    run_optimization = run_bf_optimization

    def run_ga_optimization(
        self,
        optimization_setting: OptimizationSetting,
        max_workers: int | None = None,
        ngen: int = 30,
        output: bool = True
    ) -> list:
        """inheritAlgoOptimization"""
        if not check_optimization_setting(optimization_setting):
            return []

        evaluate_func: Callable = wrap_evaluate(self, optimization_setting.target_name)
        results: list = run_ga_optimization(
            evaluate_func,
            optimization_setting,
            get_target_value,
            max_workers=max_workers,
            ngen=ngen,
            output=self.output
        )

        if output:
            for result in results:
                msg: str = _("Parameter：{}, target：{}").format(result[0], result[1])
                self.output(msg)

        return results

    def update_daily_close(self, bars: dict[str, BarData], dt: datetime) -> None:
        """Updateeachdaysclose price"""
        d: date = dt.date()

        close_prices: dict = {}
        for bar in bars.values():
            close_prices[bar.vt_symbol] = bar.close_price

        daily_result: PortfolioDailyResult | None = self.daily_results.get(d, None)

        if daily_result:
            daily_result.update_close_prices(close_prices)
        else:
            self.daily_results[d] = PortfolioDailyResult(d, close_prices)

    def new_bars(self, dt: datetime) -> None:
        """HistoricalDataPush"""
        self.datetime = dt

        bars: dict[str, BarData] = {}
        for vt_symbol in self.vt_symbols:
            bar: BarData | None = self.history_data.get((dt, vt_symbol), None)

            # checkwhetherGetTothisContractspecifiedTimeHistoricalData
            if bar:
                # UpdateKlinetoprovideOrdermatch
                self.bars[vt_symbol] = bar
                # cacheKlineDatatoprovidestrategy.on_barsUpdate
                bars[vt_symbol] = bar
            # IfGetnotTo，butself.barsDictinalreadyhaveContractDatacache, useBeforeDatapadding
            elif vt_symbol in self.bars:
                old_bar: BarData = self.bars[vt_symbol]

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
                self.bars[vt_symbol] = bar

        self.cross_limit_order()
        self.strategy.on_bars(bars)

        if self.strategy.inited:
            self.update_daily_close(self.bars, dt)

    def cross_limit_order(self) -> None:
        """matchlimit priceOrder"""
        for order in list(self.active_limit_orders.values()):
            bar: BarData = self.bars[order.vt_symbol]

            long_cross_price: float = bar.low_price
            short_cross_price: float = bar.high_price
            long_best_price: float = bar.open_price
            short_best_price: float = bar.open_price

            # PushOrdernotTradeStatusUpdate
            if order.status == Status.SUBMITTING:
                order.status = Status.NOTTRADED
                self.strategy.update_order(order)

            # CheckCanbymatchlimit priceOrder
            long_cross: bool = (
                order.direction == Direction.LONG
                and order.price >= long_cross_price
                and long_cross_price > 0
            )

            short_cross: bool = (
                order.direction == Direction.SHORT
                and order.price <= short_cross_price
                and short_cross_price > 0
            )

            if not long_cross and not short_cross:
                continue

            # PushOrder TradeStatusUpdate
            order.traded = order.volume
            order.status = Status.ALLTRADED
            self.strategy.update_order(order)

            if order.vt_orderid in self.active_limit_orders:
                self.active_limit_orders.pop(order.vt_orderid)

            # PushTradeInfo
            self.trade_count += 1

            if long_cross:
                trade_price = min(order.price, long_best_price)
            else:
                trade_price = max(order.price, short_best_price)

            trade: TradeData = TradeData(
                symbol=order.symbol,
                exchange=order.exchange,
                orderid=order.orderid,
                tradeid=str(self.trade_count),
                direction=order.direction,
                offset=order.offset,
                price=trade_price,
                volume=order.volume,
                datetime=self.datetime,
                gateway_name=self.gateway_name,
            )

            self.strategy.update_trade(trade)
            self.trades[trade.vt_tradeid] = trade

    def load_bars(
        self,
        strategy: StrategyTemplate,
        days: int,
        interval: Interval
    ) -> None:
        """LoadHistoricalData"""
        self.days = days

    def send_order(
        self,
        strategy: StrategyTemplate,
        vt_symbol: str,
        direction: Direction,
        offset: Offset,
        price: float,
        volume: float,
        lock: bool,
        net: bool
    ) -> list[str]:
        """SendOrder"""
        price = round_to(price, self.priceticks[vt_symbol])
        symbol, exchange = extract_vt_symbol(vt_symbol)

        self.limit_order_count += 1

        order: OrderData = OrderData(
            symbol=symbol,
            exchange=exchange,
            orderid=str(self.limit_order_count),
            direction=direction,
            offset=offset,
            price=price,
            volume=volume,
            status=Status.SUBMITTING,
            datetime=self.datetime,
            gateway_name=self.gateway_name,
        )

        self.active_limit_orders[order.vt_orderid] = order
        self.limit_orders[order.vt_orderid] = order

        return [order.vt_orderid]

    def cancel_order(self, strategy: StrategyTemplate, vt_orderid: str) -> None:
        """Ordercancel order"""
        if vt_orderid not in self.active_limit_orders:
            return
        order: OrderData = self.active_limit_orders.pop(vt_orderid)

        order.status = Status.CANCELLED
        self.strategy.update_order(order)

    def write_log(self, msg: str, strategy: StrategyTemplate | None = None) -> None:
        """OutputLog"""
        msg = f"{self.datetime}\t{msg}"
        self.logs.append(msg)

    def send_email(self, msg: str, strategy: StrategyTemplate | None = None) -> None:
        """SendEmail"""
        pass

    def sync_strategy_data(self, strategy: StrategyTemplate) -> None:
        """SaveStrategyDataTofile"""
        pass

    def get_engine_type(self) -> EngineType:
        """GetEngineClasstype"""
        return self.engine_type

    def get_pricetick(self, strategy: StrategyTemplate, vt_symbol: str) -> float:
        """GetContractPricetick"""
        return self.priceticks[vt_symbol]

    def get_size(self, strategy: StrategyTemplate, vt_symbol: str) -> float:
        """GetContractmultiplier"""
        return self.sizes[vt_symbol]

    def put_strategy_event(self, strategy: StrategyTemplate) -> None:
        """PushEventUpdateStrategyinterface"""
        pass

    def output(self, msg: str) -> None:
        """OutputBacktestEngineInfo"""
        print(f"{datetime.now()}\t{msg}")

    def get_all_trades(self) -> list[TradeData]:
        """GetallTradeInfo"""
        return list(self.trades.values())

    def get_all_orders(self) -> list[OrderData]:
        """GetallOrderInfo"""
        return list(self.limit_orders.values())

    def get_all_daily_results(self) -> list["PortfolioDailyResult"]:
        """GetalleachdaysPnLInfo"""
        return list(self.daily_results.values())


class ContractDailyResult:
    """ContracteachdaysPnLresult"""

    def __init__(self, result_date: date, close_price: float) -> None:
        """Constructor"""
        self.date: date = result_date
        self.close_price: float = close_price
        self.pre_close: float = 0

        self.trades: list[TradeData] = []
        self.trade_count: int = 0

        self.start_pos: float = 0
        self.end_pos: float = 0

        self.turnover: float = 0
        self.commission: float = 0
        self.slippage: float = 0

        self.trading_pnl: float = 0
        self.holding_pnl: float = 0
        self.total_pnl: float = 0
        self.net_pnl: float = 0

    def add_trade(self, trade: TradeData) -> None:
        """AddTradeInfo"""
        self.trades.append(trade)

    def calculate_pnl(
        self,
        pre_close: float,
        start_pos: float,
        size: float,
        rate: float,
        slippage: float
    ) -> None:
        """CalculatePnL"""
        # logyesterdayclose price
        self.pre_close = pre_close

        # CalculatePosition PnL
        self.start_pos = start_pos
        self.end_pos = start_pos

        self.holding_pnl = self.start_pos * (self.close_price - self.pre_close) * size

        # CalculateTrading PnL
        self.trade_count = len(self.trades)

        for trade in self.trades:
            if trade.direction == Direction.LONG:
                pos_change = trade.volume
            else:
                pos_change = -trade.volume

            self.end_pos += pos_change

            turnover: float = trade.volume * size * trade.price

            self.trading_pnl += pos_change * (self.close_price - trade.price) * size
            self.slippage += trade.volume * size * slippage
            self.turnover += turnover
            self.commission += turnover * rate

        # CalculateeachdaysPnL
        self.total_pnl = self.trading_pnl + self.holding_pnl
        self.net_pnl = self.total_pnl - self.commission - self.slippage

    def update_close_price(self, close_price: float) -> None:
        """Updateeachdaysclose price"""
        self.close_price = close_price


class PortfolioDailyResult:
    """PortfolioeachdaysPnLresult"""

    def __init__(self, result_date: date, close_prices: dict[str, float]) -> None:
        """"""
        self.date: date = result_date
        self.close_prices: dict[str, float] = close_prices
        self.pre_closes: dict[str, float] = {}
        self.start_poses: dict[str, float] = {}
        self.end_poses: dict[str, float] = {}

        self.contract_results: dict[str, ContractDailyResult] = {}

        for vt_symbol, close_price in close_prices.items():
            self.contract_results[vt_symbol] = ContractDailyResult(result_date, close_price)

        self.trade_count: int = 0
        self.turnover: float = 0
        self.commission: float = 0
        self.slippage: float = 0
        self.trading_pnl: float = 0
        self.holding_pnl: float = 0
        self.total_pnl: float = 0
        self.net_pnl: float = 0

    def add_trade(self, trade: TradeData) -> None:
        """AddTradeInfo"""
        contract_result: ContractDailyResult = self.contract_results[trade.vt_symbol]
        contract_result.add_trade(trade)

    def calculate_pnl(
        self,
        pre_closes: dict[str, float],
        start_poses: dict[str, float],
        sizes: dict[str, float],
        rates: dict[str, float],
        slippages: dict[str, float],
    ) -> None:
        """CalculatePnL"""
        self.pre_closes = pre_closes
        self.start_poses = start_poses

        for vt_symbol, contract_result in self.contract_results.items():
            contract_result.calculate_pnl(
                pre_closes.get(vt_symbol, 0),
                start_poses.get(vt_symbol, 0),
                sizes[vt_symbol],
                rates[vt_symbol],
                slippages[vt_symbol]
            )

            self.trade_count += contract_result.trade_count
            self.turnover += contract_result.turnover
            self.commission += contract_result.commission
            self.slippage += contract_result.slippage
            self.trading_pnl += contract_result.trading_pnl
            self.holding_pnl += contract_result.holding_pnl
            self.total_pnl += contract_result.total_pnl
            self.net_pnl += contract_result.net_pnl

            self.end_poses[vt_symbol] = contract_result.end_pos

    def update_close_prices(self, close_prices: dict[str, float]) -> None:
        """Updateeachdaysclose price"""
        self.close_prices.update(close_prices)

        for vt_symbol, close_price in close_prices.items():
            contract_result: ContractDailyResult | None = self.contract_results.get(vt_symbol, None)
            if contract_result:
                contract_result.update_close_price(close_price)
            else:
                self.contract_results[vt_symbol] = ContractDailyResult(self.date, close_price)


@lru_cache(maxsize=999)
def load_bar_data(
    vt_symbol: str,
    interval: Interval,
    start: datetime,
    end: datetime
) -> list[BarData]:
    """throughpastDatabaseGetHistoricalData"""
    symbol, exchange = extract_vt_symbol(vt_symbol)

    database: BaseDatabase = get_database()

    bars: list[BarData] = database.load_bar_data(
        symbol, exchange, interval, start, end
    )

    return bars


def evaluate(
    target_name: str,
    strategy_class: type[StrategyTemplate],
    vt_symbols: list[str],
    interval: Interval,
    start: datetime,
    rates: dict[str, float],
    slippages: dict[str, float],
    sizes: dict[str, float],
    priceticks: dict[str, float],
    capital: float,
    end: datetime,
    setting: dict
) -> tuple:
    """packageinstallBacktestrelatedFunctiontoprovideprocesspoolinRunning"""
    engine: BacktestingEngine = BacktestingEngine()

    engine.set_parameters(
        vt_symbols=vt_symbols,
        interval=interval,
        start=start,
        rates=rates,
        slippages=slippages,
        sizes=sizes,
        priceticks=priceticks,
        capital=capital,
        end=end,
    )

    engine.add_strategy(strategy_class, setting)
    engine.load_data()
    engine.run_backtesting()
    engine.calculate_result()
    statistics: dict = engine.calculate_statistics(output=False)

    target_value: float = statistics[target_name]
    return (str(setting), target_value, statistics)


def wrap_evaluate(engine: BacktestingEngine, target_name: str) -> Callable:
    """packageinstallBacktestConfigFunctiontoprovideprocesspoolinRunning"""
    func: Callable = partial(
        evaluate,
        target_name,
        engine.strategy_class,
        engine.vt_symbols,
        engine.interval,
        engine.start,
        engine.rates,
        engine.slippages,
        engine.sizes,
        engine.priceticks,
        engine.capital,
        engine.end
    )
    return func


def get_target_value(result: list) -> float:
    """GetOptimizationtarget"""
    target_value: float = result[1]
    return target_value
