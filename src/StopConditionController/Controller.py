from src.StopConditionController.utils import ControllerConfig
from src.utils import DialogueState

class ControllerModule:
    def __init__(self, config: ControllerConfig) -> None:
        self.config = config

    def is_terminal_state(state: DialogueState) -> bool:
        pass
        