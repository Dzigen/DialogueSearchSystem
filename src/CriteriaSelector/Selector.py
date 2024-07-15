from .DynamicSelector import DynamicSelector
from .StaticSelector import StaticSelector
from .utils import SelectorConfig
from ..utils import DialogueState
from ..logger import Logger

class SelectorModule:
    def __init__(self, config: SelectorConfig, log) -> None:
        self.log = log
        self.log.info("Initiating Selector-class")
        self.config = config

    @Logger.cls_se_log('''Поиск критерия для аггрегации документов''')
    def find_criteria(self, state: DialogueState):
        
        # TODO : !!!STUB!!!
        state.history.append(DialogueTurn())
        topic = 'test_criteria'
        state.history[-1].topic = topic