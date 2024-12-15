from abc import ABC
from types import ModuleType
from typing import Optional, List, Callable
from importlib import import_module

from .object import HistoryRequest, TickData, BarData
from .setting import SETTINGS
from .locale import _


class BaseDatafeed(ABC):
    """
    Abstract datafeed class for connecting to different datafeed.
    """

    def init(self, output: Callable = print) -> bool:
        """
        Initialize datafeed service connection.
        """
        pass

    def query_bar_history(self, req: HistoryRequest, output: Callable = print) -> Optional[List[BarData]]:
        """
        Query history bar data.
        """
        output(_("Failed to query K-line data: Data service is not correctly configured"))

    def query_tick_history(self, req: HistoryRequest, output: Callable = print) -> Optional[List[TickData]]:
        """
        Query history tick data.
        """
        output(_("Failed to query Tick data: Data service is not correctly configured"))


datafeed: BaseDatafeed = None


def get_datafeed() -> BaseDatafeed:
    """"""
    # Return datafeed object if already inited
    global datafeed
    if datafeed:
        return datafeed

    # Read datafeed related global setting
    datafeed_name: str = SETTINGS["datafeed.name"]

    if not datafeed_name:
        datafeed = BaseDatafeed()

        print(_("No data service configured, please modify the datafeed related content in the global configuration"))
    else:
        module_name: str = f"vnpy_{datafeed_name}"

        # Try to import datafeed module
        try:
            module: ModuleType = import_module(module_name)

            # Create datafeed object from module
            datafeed = module.Datafeed()
        # Use base class if failed
        except ModuleNotFoundError:
            datafeed = BaseDatafeed()

            print(_("Failed to load data service module, please run pip install {} to try installing").format(module_name))

    return datafeed
