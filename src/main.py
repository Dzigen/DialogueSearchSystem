from src.CriteriaSelector.Selector import SelectorModule
from src.DocumentsAggregator.Aggregator import AggregatorModule
from src.DocumentsReducer.Reducer import ReducerModule
from src.DocumentsRetriever.Retriever import RetrieverModule
from src.DocumentsSummarizer.Summarizer import SummarizerModule
from src.QuestionGenerator.Generator import GeneratorModule
from src.StopConditionController.Controller import ControllerModule
from src.utils import DialogueState, UserHandler, DialogueSearchConfig
from src.logger import Logger

class DialogueSearch:
    def __init__(self, config: DialogueSearchConfig):
        logger = Logger(True)
        self.log = logger.get_logger(__name__)
        self.log.info("Initiating DialogueSearch-class")

        self.selector = SelectorModule(config['selector'])
        self.aggregator = AggregatorModule(config['aggregator'])
        self.reducer = ReducerModule(config['reducer'])
        self.retriever = RetrieverModule(config['retriever'])
        self.summarizer = SummarizerModule(config['summarizer'])
        self.generator = GeneratorModule(config['generator'])
        self.controller = ControllerModule(config['controller'])
        self.user_handler = UserHandler()

    @Logger.cls_se_log(info="Start dialogue session")
    def start(self, dialogue_format: str = 'single-turn'):
        dialogue_state = DialogueState()

        # Этап 1 
        self.user_handler.ask(dialogue_state)
        self.retriever.search(dialogue_state)

        if dialogue_format == 'multi-turn':
            # Этап 2
            self.selector.find_criteria(dialogue_state)

            # Этап 3        
            while self.controller.is_terminal_state(dialogue_state):
                # Этап 4
                self.aggregator.extract_info(dialogue_state)
                self.aggregator.generalize_info(dialogue_state)
                # ЭТап 5
                self.generator.create_question(dialogue_state)
                # Этап 6
                self.user_handler.clarify(dialogue_state)
                self.reducer.filter_documents(dialogue_state)
                # Этап 2
                self.selector.find_criteria(dialogue_state)

        # Этап 7
        self.summarizer.create_answer(dialogue_state)
        self.user_handler.answer(dialogue_state)


