from src.DocumentsRetriever.utils import RetrieverConfig
from src.utils import DialogueState
from src.logger import Logger

class RetrieverModule:
    def __init__(self, config: RetrieverConfig) -> None:
        logger = Logger(True)
        self.log = logger.get_logger(__name__)
        self.log.info("Initiating Retriever-class")
        self.config = config
    
    @Logger.cls_se_log('''Формирование базового набора 
                       релевантных документов''')
    def search(self, state: DialogueState):
        
        # TODO : !!!STUB!!!
        docs = ['doc1', 'doc2', 'doc3']
        state.base_relevant_docs = docs
