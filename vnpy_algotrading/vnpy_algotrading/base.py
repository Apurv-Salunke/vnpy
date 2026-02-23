from enum import Enum


EVENT_ALGO_LOG = "eAlgoLog"
EVENT_ALGO_UPDATE = "eAlgoUpdate"


APP_NAME = "AlgoTrading"


class AlgoStatus(Enum):
    """Algo Status"""

    RUNNING = "Running"
    PAUSED = "Paused"
    STOPPED = "Stopped"
    FINISHED = "Finished"
