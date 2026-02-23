from vnpy.trader.object import OrderRequest, OrderData

from ..template import RuleTemplate


class ActiveOrderRule(RuleTemplate):
    """activeOrder volumeCheckRisk controlRule"""

    name: str = "activeOrderCheck"

    parameters: dict[str, str] = {
        "active_order_limit": "activeOrderuplimit"
    }

    variables: dict[str, str] = {
        "active_order_count": "activeOrder volume"
    }

    def on_init(self) -> None:
        """Initialize"""
        # DefaultParameter
        self.active_order_limit: int = 50

        # activeOrder
        self.active_orders: dict[str, OrderData] = {}

        # Volumestatistics
        self.active_order_count: int = 0

    def check_allowed(self, req: OrderRequest, gateway_name: str) -> bool:
        """CheckwhetherallowOrder"""
        if self.active_order_count >= self.active_order_limit:
            self.write_log(f"activeOrder volume{self.active_order_count}reachTouplimit{self.active_order_limit}：{req}")
            return False

        return True

    def on_order(self, order: OrderData) -> None:
        """OrderPush"""
        if order.is_active():
            self.active_orders[order.vt_orderid] = order
        elif order.vt_orderid in self.active_orders:
            self.active_orders.pop(order.vt_orderid)

        self.active_order_count = len(self.active_orders)

        self.put_event()
