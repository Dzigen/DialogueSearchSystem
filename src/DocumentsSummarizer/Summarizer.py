from src.DocumentsSummarizer.utils import SummarizerConfig, base_config
from src.utils import DialogueState
from src.logger import Logger

class SummarizerModule:
    def __init__(self, config: SummarizerConfig = base_config) -> None:
        logger = Logger(True)
        self.log = logger.get_logger(__name__)
        self.log.info("Initiating Summarizer-class")
        self.config = config

    @Logger.cls_se_log('''Генерация ответа на основании концентрированного
                       набора релевантных документов''')
    def create_answer(self, state: DialogueState):
        pass