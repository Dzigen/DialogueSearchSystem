from src.QuestionGenerator.utils import GeneratorConfig
from src.utils import DialogueState
from src.logger import Logger

class GeneratorModule:
    def __init__(self, config: GeneratorConfig, log) -> None:
        self.log = log
        self.log.info("Initiating Generator-class")
        self.config = config
        
    @Logger.cls_se_log("Генерация уточняющего вопроса")
    def create_question(self, state: DialogueState):
        
        # TODO : !!!STUB!!!
        question = 'test question'
        state.history[-1].question = question