from threading import Thread
from datetime import datetime
from typing import cast

from pandas import DataFrame
from rqdatac import (
    LiveMarketDataClient,
    init,
    all_instruments
)

from vnpy.event import EventEngine
from vnpy.trader.gateway import BaseGateway
from vnpy.trader.constant import Exchange, Product
from vnpy.trader.object import (
    SubscribeRequest,
    OrderRequest,
    CancelRequest,
    TickData,
    ContractData
)
from vnpy.trader.utility import ZoneInfo


CHINA_TZ = ZoneInfo("Asia/Shanghai")


EXCHANGE_VT2RQDATA = {
    Exchange.SSE: "XSHG",
    Exchange.SZSE: "XSHE",
    Exchange.CFFEX: "CFFEX",
    Exchange.SHFE: "SHFE",
    Exchange.DCE: "DCE",
    Exchange.CZCE: "CZCE",
    Exchange.INE: "INE",
    Exchange.GFEX: "GFEX"
}
EXCHANGE_RQDATA2VT = {v: k for k, v in EXCHANGE_VT2RQDATA.items()}


PRODUCT_MAP = {
    "CS": Product.EQUITY,
    "INDX": Product.INDEX,
    "ETF": Product.FUND,
    "LOF": Product.FUND,
    "FUND": Product.FUND,
    "Future": Product.FUTURES,
    "Option": Product.OPTION,
    "Convertible": Product.BOND,
    "Repo": Product.BOND
}


class RqdataGateway(BaseGateway):
    """
    VeighNaframeworkuseatforreceiveRQDataReal-timeMarket dataGateway。
    """

    default_name: str = "RQDATA"

    default_setting: dict[str, str] = {
        "Username": "",
        "Password": ""
    }

    exchanges: list[str] = list(EXCHANGE_VT2RQDATA.keys())

    def __init__(self, event_engine: EventEngine, gateway_name: str) -> None:
        super().__init__(event_engine, gateway_name)

        self.client: LiveMarketDataClient | None = None
        self.thread: Thread | None = None

        self.subscribed: set[str] = set()
        self.futures_map: dict[str, tuple[str, Exchange]] = {}      # FuturesCodeExchangemapInfo
        self.symbol_map: dict[str, str] = {}

    def connect(self, setting: dict) -> None:
        """ConnectTradingGateway"""
        if self.client:
            return

        # Initializerqdatac
        username: str = setting["Username"]
        password: str = setting["Password"]

        try:
            init(username, password)
        except Exception as ex:
            self.write_log(f"RQDataGatewayInitializeFailed：{ex}")
            return

        # QueryContractInfo
        self.query_contract()

        # CreateReal-timeMarket dataClient
        self.client = LiveMarketDataClient()

        # StartRunningthread
        self.thread = self.client.listen(handler=self.handle_msg)

        # SubscribeBeforeMarket data
        for rq_channel in self.subscribed:
            self.client.subscribe(rq_channel)

        self.write_log("RQDataGatewayInitializeSuccess")

    def subscribe(self, req: SubscribeRequest) -> None:
        """Subscribe market data"""
        # security
        if req.exchange in {Exchange.SSE, Exchange.SZSE}:
            rq_exchange: str = EXCHANGE_VT2RQDATA[req.exchange]
            rq_channel: str = f"tick_{req.symbol}.{rq_exchange}"
        # Futures
        else:
            rq_symbol = req.symbol.upper()
            rq_channel = f"tick_{rq_symbol}"

            self.futures_map[rq_symbol] = (req.symbol, req.exchange)

        self.subscribed.add(rq_channel)

        if self.client:
            self.client.subscribe(rq_channel)

    def send_order(self, req: OrderRequest) -> str:
        """Orderplace order"""
        return ""

    def cancel_order(self, req: CancelRequest) -> None:
        """Ordercancel order"""
        pass

    def query_account(self) -> None:
        """QueryAccount"""
        pass

    def query_position(self) -> None:
        """QueryPosition"""
        pass

    def close(self) -> None:
        """CloseGateway"""
        if self.client:
            self.client.close()

        if self.thread:
            self.thread.join()

    def query_contract(self) -> None:
        """QueryContract"""
        for t in ["CS", "INDX", "ETF", "Future"]:
            df: DataFrame = all_instruments(type=t)

            for tp in df.itertuples():
                if t == "INDX":
                    symbol, rq_exchange = cast(str, tp.order_book_id).split(".")
                    exchange: Exchange | None = EXCHANGE_RQDATA2VT.get(rq_exchange, None)
                else:
                    symbol = cast(str, tp.trading_code)
                    exchange = EXCHANGE_RQDATA2VT.get(cast(str, tp.exchange), None)

                if not exchange:
                    continue

                min_volume: float = cast(float, tp.round_lot)

                product: Product = PRODUCT_MAP[cast(str, tp.type)]
                if product == Product.EQUITY:
                    size: int = 1
                    pricetick: float = 0.01
                    product_name: str = "Stock"
                elif product == Product.FUND:
                    size = 1
                    pricetick = 0.001
                    product_name = "fund"
                elif product == Product.INDEX:
                    size = 1
                    pricetick = 0.01
                    product_name = "index"
                elif product == Product.FUTURES:
                    size = cast(int, tp.contract_multiplier)
                    pricetick = 0.01
                    product_name = "Futures"

                contract = ContractData(
                    symbol=symbol,
                    exchange=exchange,
                    name=tp.symbol,
                    product=product,
                    size=size,
                    pricetick=pricetick,
                    min_volume=min_volume,
                    gateway_name=self.gateway_name
                )
                self.on_contract(contract)

                self.symbol_map[cast(str, tp.order_book_id)] = contract

            self.write_log(f"{product_name}ContractInfoQuerySuccess")

    def handle_msg(self, data: dict) -> None:
        """ProcessMarket dataPush"""
        contract: ContractData = self.symbol_map.get(data["order_book_id"], None)
        if not contract:
            self.write_log(f"collectToNot supportedContract{data['order_book_id']}Market dataPush")
            return

        dt: datetime = datetime.strptime(str(data["datetime"]), "%Y%m%d%H%M%S%f")
        dt = dt.replace(tzinfo=CHINA_TZ)
        tick: TickData = TickData(
            symbol=contract.symbol,
            exchange=contract.exchange,
            name=contract.name,
            datetime=dt,
            volume=data["volume"],
            turnover=data["total_turnover"],
            open_interest=data.get("open_interest", 0),
            last_price=data["last"],
            limit_up=data.get("limit_up", 0),
            limit_down=data.get("limit_down", 0),
            open_price=data["open"],
            high_price=data["high"],
            low_price=data["low"],
            pre_close=data["prev_close"],
            gateway_name=self.gateway_name
        )

        if "bid" in data:
            bp: list[float] = data["bid"]
            ap: list[float] = data["ask"]
            bv: list[float] = data["bid_vol"]
            av: list[float] = data["ask_vol"]

            tick.bid_price_1 = bp[0]
            tick.bid_price_2 = bp[1]
            tick.bid_price_3 = bp[2]
            tick.bid_price_4 = bp[3]
            tick.bid_price_5 = bp[4]

            tick.ask_price_1 = ap[0]
            tick.ask_price_2 = ap[1]
            tick.ask_price_3 = ap[2]
            tick.ask_price_4 = ap[3]
            tick.ask_price_5 = ap[4]

            tick.bid_volume_1 = bv[0]
            tick.bid_volume_2 = bv[1]
            tick.bid_volume_3 = bv[2]
            tick.bid_volume_4 = bv[3]
            tick.bid_volume_5 = bv[4]

            tick.ask_volume_1 = av[0]
            tick.ask_volume_2 = av[1]
            tick.ask_volume_3 = av[2]
            tick.ask_volume_4 = av[3]
            tick.ask_volume_5 = av[4]

        self.on_tick(tick)
