from vnpy.trader.object import OrderRequest, ContractData

from ..template import RuleTemplate


class OrderSizeRule(RuleTemplate):
    """OrderscaleCheckRisk controlRule"""

    name: str = "OrderscaleCheck"

    parameters: dict[str, str] = {
        "order_volume_limit": "Order volumeuplimit",
        "order_value_limit": "Orderpricevalueuplimit",
    }

    def on_init(self) -> None:
        """Initialize"""
        self.order_volume_limit: int = 500
        self.order_value_limit: float = 1_000_000

    def check_allowed(self, req: OrderRequest, gateway_name: str) -> bool:
        """CheckwhetherallowOrder"""
        if req.volume > self.order_volume_limit:
            self.write_log(f"Order volume{req.volume}exceedpastuplimit{self.order_volume_limit}：{req}")
            return False

        contract: ContractData | None = self.get_contract(req.vt_symbol)
        if contract and req.price:      # onlyconsiderlimit priceorder
            order_value: float = req.volume * req.price * contract.size
            if order_value > self.order_value_limit:
                self.write_log(f"Orderpricevalue{order_value}exceedpastuplimit{self.order_value_limit}：{req}")
                return False

        return True
