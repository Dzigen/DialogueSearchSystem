from src.DocumentsReducer.utils import ReducerConfig
from src.utils import DialogueState
from src.logger import Logger

class ReducerModule:
    def __init__(self, config: ReducerConfig) -> None:
        logger = Logger(True)
        self.log = logger.get_logger(__name__)
        self.log.info("Initiating Reducer-class")
        self.config = config

    @Logger.cls_se_log('''Фильтрация документов
                       на основании уточняющего ответа''')
    def filter_documents(self, dialogue_state: DialogueState):
        pass