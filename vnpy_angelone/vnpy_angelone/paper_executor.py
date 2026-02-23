from dataclasses import dataclass
from datetime import datetime

from vnpy.trader.object import CancelRequest, OrderRequest


@dataclass(slots=True)
class ExternalPaperExecutorConfig:
    """Configuration for external paper execution endpoint."""

    base_url: str
    timeout_seconds: int = 10


class ExternalPaperExecutor:
    """
    External paper execution adapter skeleton.

    Implement these methods when you have the target paper broker API details.
    """

    def __init__(self, config: ExternalPaperExecutorConfig) -> None:
        self.config: ExternalPaperExecutorConfig = config
        self.order_seq: int = 0

    def connect(self) -> None:
        """Initialize client session/token with external paper broker."""
        # TODO: Implement HTTP/WebSocket client setup here.
        return

    def close(self) -> None:
        """Close connections/resources to paper broker."""
        return

    def submit_order(self, req: OrderRequest) -> str:
        """
        Submit order to external paper broker and return broker order id.

        Current skeleton returns a locally generated id.
        """
        # TODO: Replace local id with real API call and broker order id.
        self.order_seq += 1
        ts: str = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"PAPER{ts}{self.order_seq:06d}"

    def cancel_order(self, req: CancelRequest) -> None:
        """Cancel order by broker order id."""
        # TODO: Implement cancel API call.
        return
