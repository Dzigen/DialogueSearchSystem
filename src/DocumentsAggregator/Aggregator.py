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
        
        # TODO : !!!STUB!!!
        raw_info = ['info1', 'info2', 'info3', 'info4', 'info5', 'info6']
        state.history[-1].raw_info = raw_info

    @Logger.cls_se_log('''Формирование общих тем из документов
                       по заданному критерию''')
    def generalize_info(self, state: DialogueState):
        
        # TODO : !!!STUB!!!
        choices = ['topic1', 'topic2', 'topic3', 'topic3']
        state.history[-1].choices = choices