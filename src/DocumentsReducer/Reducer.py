from src.DocumentsReducer.utils import ReducerConfig
from src.utils import DialogueState
from src.logger import Logger

class ReducerModule:
    def __init__(self, config: ReducerConfig, log) -> None:
        self.log = log
        self.log.info("Initiating Reducer-class")
        self.config = config

    @Logger.cls_se_log('''Фильтрация документов на основании уточняющего ответа''')
    def filter_documents(self, state: DialogueState):
        
        # TODO : !!!STUB!!!
        filtered_docs = [1, 3]
        state.history[-1].filtered_relevant_docs = filtered_docs