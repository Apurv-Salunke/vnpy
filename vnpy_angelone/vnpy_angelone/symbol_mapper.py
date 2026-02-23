from dataclasses import dataclass
import csv
from pathlib import Path

from vnpy.trader.constant import Exchange, Product
from vnpy.trader.object import ContractData


@dataclass(slots=True)
class InstrumentRecord:
    """
    Minimal normalized instrument record.

    Extend as needed when wiring SmartAPI instrument master.
    """

    symbol_token: str
    trading_symbol: str
    exchange: str
    name: str
    lot_size: float
    tick_size: float
    product: Product


class InstrumentMapper:
    """Token/symbol mapper loaded from Angel One instrument master export."""

    def __init__(self) -> None:
        self.by_token: dict[str, InstrumentRecord] = {}
        self.by_trading_symbol: dict[str, InstrumentRecord] = {}

    def load_csv(self, path: str) -> int:
        """
        Load records from a CSV file path.

        Expected columns (minimum):
        - symbol_token
        - trading_symbol
        - exchange
        - name
        - lot_size
        - tick_size
        """
        file_path = Path(path)
        if not file_path.exists():
            return 0

        count: int = 0
        with file_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                token: str = str(row.get("symbol_token", "")).strip()
                trading_symbol: str = str(row.get("trading_symbol", "")).strip()
                exchange: str = str(row.get("exchange", "")).strip()
                name: str = str(row.get("name", trading_symbol)).strip()
                lot_size: float = float(row.get("lot_size", 1) or 1)
                tick_size: float = float(row.get("tick_size", 0.05) or 0.05)

                if not token or not trading_symbol:
                    continue

                record = InstrumentRecord(
                    symbol_token=token,
                    trading_symbol=trading_symbol,
                    exchange=exchange,
                    name=name,
                    lot_size=lot_size,
                    tick_size=tick_size,
                    product=Product.EQUITY,
                )
                self.by_token[token] = record
                self.by_trading_symbol[trading_symbol] = record
                count += 1

        return count

    def to_contract(self, record: InstrumentRecord, gateway_name: str) -> ContractData:
        """
        Convert normalized record to VeighNa contract.

        `Exchange.GLOBAL` is used as a placeholder in this skeleton.
        """
        return ContractData(
            symbol=record.trading_symbol,
            exchange=Exchange.GLOBAL,
            name=record.name,
            product=record.product,
            size=record.lot_size,
            pricetick=record.tick_size,
            min_volume=record.lot_size,
            gateway_name=gateway_name,
            history_data=True,
            net_position=True,
        )
