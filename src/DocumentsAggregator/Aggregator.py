from src.DocumentsAggregator.utils import AggregatorConfig
from src.utils import DialogueState
from src.logger import Logger

class AggregatorModule:
    def __init__(self, config: AggregatorConfig) -> None:
        logger = Logger(True)
        self.log = logger.get_logger(__name__)
        self.log.info("Initiating Aggregator-class")
        self.config = config

    @Logger.cls_se_log('''Извлечение информации из документов 
                       по заданному критерию''')
    def extract_info(self, state: DialogueState):
        pass

    @Logger.cls_se_log('''Формирование общих тем из документов
                       по заданному критерию''')
    def generalize_info(self, state: DialogueState):
        pass