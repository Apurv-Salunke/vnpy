from datetime import datetime

from vnpy.event import EventEngine
from vnpy.trader.constant import Exchange, Status
from vnpy.trader.gateway import BaseGateway
from vnpy.trader.object import (
    AccountData,
    CancelRequest,
    ContractData,
    OrderData,
    OrderRequest,
    SubscribeRequest,
)

from .paper_executor import ExternalPaperExecutor, ExternalPaperExecutorConfig
from .settings import AngelOneSettings
from .symbol_mapper import InstrumentMapper


class AngelOneGateway(BaseGateway):
    """
    Angel One SmartAPI gateway skeleton.

    Notes:
    - This is a scaffold and does not call SmartAPI yet.
    - It supports paper-mode order flow placeholders so UI behavior can be tested.
    """

    default_name: str = "ANGELONE"

    default_setting: dict = {
        "API Key": "",
        "Client Code": "",
        "PIN": "",
        "TOTP Secret": "",
        "Feed Token": "",
        "Instrument Master Path": "",
        "Paper Mode": ["True", "False"],
        "Paper Base URL": "",
        "Timeout Seconds": 10,
    }

    exchanges: list[Exchange] = [Exchange.GLOBAL]

    def __init__(self, event_engine: EventEngine, gateway_name: str) -> None:
        super().__init__(event_engine, gateway_name)
        self.settings: AngelOneSettings | None = None
        self.connected: bool = False
        self.subscriptions: set[str] = set()
        self.mapper: InstrumentMapper = InstrumentMapper()
        self.order_count: int = 0
        self.paper_executor: ExternalPaperExecutor | None = None

    def connect(self, setting: dict) -> None:
        """Load settings and initialize skeleton services."""
        self.settings = AngelOneSettings.from_setting(setting)
        valid, msg = self.settings.validate_required()
        if not valid:
            self.write_log(f"ANGELONE connect failed: {msg}")
            return

        if self.settings.instrument_master_path:
            loaded: int = self.mapper.load_csv(self.settings.instrument_master_path)
            self.write_log(f"ANGELONE instrument records loaded: {loaded}")

            for record in self.mapper.by_token.values():
                contract: ContractData = self.mapper.to_contract(record, self.gateway_name)
                self.on_contract(contract)

        if self.settings.paper_base_url:
            executor_config = ExternalPaperExecutorConfig(
                base_url=self.settings.paper_base_url,
                timeout_seconds=self.settings.timeout_seconds,
            )
            self.paper_executor = ExternalPaperExecutor(executor_config)
            self.paper_executor.connect()
            self.write_log("ANGELONE external paper executor initialized")

        # TODO: Implement SmartAPI login/session creation and websocket connection.
        self.connected = True
        self.write_log("ANGELONE connected (skeleton mode)")

    def close(self) -> None:
        """Close skeleton resources."""
        self.connected = False
        if self.paper_executor:
            self.paper_executor.close()
        self.write_log("ANGELONE closed")

    def subscribe(self, req: SubscribeRequest) -> None:
        """Record subscriptions and wire to SmartAPI websocket in future."""
        self.subscriptions.add(req.vt_symbol)
        # TODO: Send websocket subscribe message for this symbol token.
        self.write_log(f"ANGELONE subscribed: {req.vt_symbol}")

    def send_order(self, req: OrderRequest) -> str:
        """
        Send order in skeleton mode.

        - In paper mode with external executor: return external paper id.
        - Otherwise: emit rejected order because live execution is not implemented.
        """
        self.order_count += 1
        local_orderid: str = f"{datetime.now().strftime('%y%m%d%H%M%S')}{self.order_count}"
        order: OrderData = req.create_order_data(local_orderid, self.gateway_name)

        if not self.settings:
            order.status = Status.REJECTED
            self.on_order(order)
            self.write_log("ANGELONE send_order rejected: gateway not connected")
            return order.vt_orderid

        if self.settings.paper_mode and self.paper_executor:
            external_orderid: str = self.paper_executor.submit_order(req)
            order.orderid = external_orderid
            order.__post_init__()
            order.status = Status.NOTTRADED
            self.on_order(order)
            self.write_log(f"ANGELONE paper order submitted: {order.vt_orderid}")
            return order.vt_orderid

        order.status = Status.REJECTED
        self.on_order(order)
        self.write_log("ANGELONE send_order rejected: live execution TODO or no paper executor")
        return order.vt_orderid

    def cancel_order(self, req: CancelRequest) -> None:
        """Cancel order via external paper executor when available."""
        if self.paper_executor:
            self.paper_executor.cancel_order(req)
            self.write_log(f"ANGELONE paper cancel requested: {req.orderid}")
            return

        self.write_log(f"ANGELONE cancel ignored (no executor): {req.orderid}")

    def query_account(self) -> None:
        """Publish placeholder account snapshot until SmartAPI account is wired."""
        if not self.connected:
            return

        account: AccountData = AccountData(
            accountid="PAPER",
            balance=0,
            frozen=0,
            gateway_name=self.gateway_name,
        )
        self.on_account(account)

    def query_position(self) -> None:
        """Position query placeholder until holdings/positions mapping is wired."""
        if not self.connected:
            return

        # TODO: Map SmartAPI holdings/positions to PositionData and push via on_position.
        return
