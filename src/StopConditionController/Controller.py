from src.StopConditionController.utils import ControllerConfig
from src.utils import DialogueState
from src.logger import Logger

class ControllerModule:
    def __init__(self, config: ControllerConfig) -> None:
        self.config = config
        logger = Logger(True)
        self.log = logger.get_logger(__name__)
        self.log.info("Initiating Controller-class")

    Logger.cls_se_log('''Проверка на наличие терминального состояния 
                      и прекращение генерации уточняющих вопросов''')
    def is_terminal_state(self, state: DialogueState) -> bool:
        return False if len(state.history) > 2 else True
        