from src.StopConditionController.utils import ControllerConfig, base_config
from src.utils import DialogueState

class ControllerModule:
    def __init__(self, config: ControllerConfig = base_config) -> None:
        self.config = config

    def is_terminal_state(state: DialogueState) -> bool:
        pass
        