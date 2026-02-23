from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

from vnpy_angelone import AngelOneGateway
from vnpy_datamanager import DataManagerApp
from vnpy_paperaccount import PaperAccountApp


def main() -> None:
    """Run VeighNa Trader with Angel One gateway skeleton and paper account."""
    qapp = create_qapp()

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    main_engine.add_gateway(AngelOneGateway)

    main_engine.add_app(PaperAccountApp)
    main_engine.add_app(DataManagerApp)

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()


if __name__ == "__main__":
    main()
