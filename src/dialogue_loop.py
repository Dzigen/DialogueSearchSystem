from .CriteriaSelector.Selector import SelectorModule
from .DocumentsAggregator.Aggregator import AggregatorModule
from .DocumentsReducer.Reducer import ReducerModule
from .DocumentsRetriever.Retriever import RetrieverModule
from .DocumentsSummarizer.Summarizer import SummarizerModule
from .QuestionGenerator.Generator import GeneratorModule
from .StopConditionController.Controller import ControllerModule
from .utils import DialogueState, UserHandler, DialogueSearchConfig
from .logger import Logger

class DialogueSearch:
    def __init__(self, config: DialogueSearchConfig, show_log=True):
        logger = Logger(show_log)
        self.log = logger.get_logger(__name__)
        self.log.info("Initiating DialogueSearch-class")

        self.selector = SelectorModule(config.selector, self.log)
        self.aggregator = AggregatorModule(config.aggregator, self.log)
        self.reducer = ReducerModule(config.reducer, self.log)
        self.retriever = RetrieverModule(config.retriever, self.log)
        self.summarizer = SummarizerModule(config.summarizer, self.log)
        self.generator = GeneratorModule(config.generator, self.log)
        self.controller = ControllerModule(config.controller, self.log)
        self.user_handler = UserHandler(self.log)

    @Logger.cls_se_log(info="Start dialogue session")
    def start(self, query: str, dialogue_format: str = 'single-turn'):
        dialogue_state = DialogueState(query=query)

        # Этап 1 
        #self.user_handler.ask(dialogue_state)
        self.retriever.base_search(dialogue_state)

        if dialogue_format == 'multi-turn':
            # Этап 2
            self.selector.find_criteria(dialogue_state)

            # Этап 3        
            while self.controller.is_terminal_state(dialogue_state):
                # Этап 4
                self.aggregator.extract_info(dialogue_state)
                self.aggregator.generalize_info(dialogue_state)
                # Этап 5
                self.generator.create_question(dialogue_state)
                # Этап 6
                #self.user_handler.clarify(dialogue_state)
                self.reducer.filter_documents(dialogue_state)
                # Этап 2
                self.selector.find_criteria(dialogue_state)

        # Этап 7
        self.summarizer.create_answer(dialogue_state)
        #self.user_handler.answer(dialogue_state)
        self.log.info(dialogue_state)

        return dialogue_state