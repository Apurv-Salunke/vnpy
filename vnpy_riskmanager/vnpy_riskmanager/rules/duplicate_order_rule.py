from collections import defaultdict

from vnpy.trader.object import OrderRequest

from ..template import RuleTemplate


class DuplicateOrderRule(RuleTemplate):
    """DuplicateorderCheckRisk controlRule"""

    name: str = "DuplicateorderCheck"

    parameters: dict[str, str] = {
        "duplicate_order_limit": "Duplicateorderuplimit",
    }

    variables: dict[str, str] = {
        "duplicate_order_count": "Duplicateordercount"
    }

    def on_init(self) -> None:
        """Initialize"""
        # DefaultParameter
        self.duplicate_order_limit: int = 10

        # Duplicateorderstatistics
        self.duplicate_order_count: dict[str, int] = defaultdict(int)

    def check_allowed(self, req: OrderRequest, gateway_name: str) -> bool:
        """CheckwhetherallowOrder"""
        req_str: str = self.format_req(req)
        self.duplicate_order_count[req_str] += 1
        self.put_event()

        duplicate_order_count: int = self.duplicate_order_count[req_str]
        if duplicate_order_count >= self.duplicate_order_limit:
            self.write_log(f"Duplicateordercount{duplicate_order_count}reachTouplimit{self.duplicate_order_limit}：{req}")
            return False

        return True

    def format_req(self, req: OrderRequest) -> str:
        """willOrderRequestturnasString"""
        return f"{req.vt_symbol}|{req.type.value}|{req.direction.value}|{req.offset.value}|{req.volume}@{req.price}"
