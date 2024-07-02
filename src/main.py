from src.CriteriaSelector.Selector import SelectorModule
from src.DocumentsAggregator.Aggregator import AggregatorModule
from src.DocumentsReducer.Reducer import ReducerModule
from src.DocumentsRetriever.Retriever import RetrieverModule
from src.DocumentsSummarizer.Summarizer import SummarizerModule
from src.QuestionGenerator.Generator import GeneratorModule
from src.StopConditionController.Controller import ControllerModule
from src.utils import DialogueState, UserHandler


class DialogueSearch:
    def __init__(self):
        self.selector = SelectorModule()
        self.aggregator = AggregatorModule()
        self.reducer = ReducerModule()
        self.retriever = RetrieverModule()
        self.summarizer = SummarizerModule()
        self.generator = GeneratorModule()
        self.controller = ControllerModule()
        self.user_handler = UserHandler()

    def start(self):
        dialogue_state = DialogueState()

        # Этап 1 
        self.user_handler.ask(dialogue_state)
        self.retriever.search(dialogue_state)

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


