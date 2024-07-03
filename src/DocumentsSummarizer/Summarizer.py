from src.DocumentsSummarizer.utils import SummarizerConfig
from src.utils import DialogueState
from src.logger import Logger

class SummarizerModule:
    def __init__(self, config: SummarizerConfig, log) -> None:
        self.log = log
        self.log.info("Initiating Summarizer-class")
        self.config = config

    @Logger.cls_se_log('''Генерация ответа на основании концентрированного набора релевантных документов''')
    def create_answer(self, state: DialogueState):
        
        # TODO : !!!STUB!!!
        answer = 'test_answer'
        state.answer = answer