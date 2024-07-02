from dataclasses import dataclass
from src.CriteriaSelector.utils import SelectorConfig
from src.DocumentsAggregator.utils import AggregatorConfig
from src.DocumentsReducer.utils import ReducerConfig
from src.DocumentsRetriever.utils import RetrieverConfig
from src.DocumentsSummarizer.utils import SummarizerConfig
from src.QuestionGenerator.utils import GeneratorConfig
from src.StopConditionController.utils import ControllerConfig

from ruamel.yaml import YAML

configs = {
    'selector': SelectorConfig,
    'aggregator': AggregatorConfig,
    'reducer': ReducerConfig,
    'retriever': RetrieverConfig,
    'summarizer': SummarizerConfig,
    'generator': GeneratorConfig,
    'controller': ControllerConfig
}

@dataclass
class DialogueState:
    pass

@dataclass
class DialogueSearchConfig:
    selector: SelectorConfig
    aggregator: AggregatorConfig
    reducer: ReducerConfig
    retriever: RetrieverConfig
    summarizer: SummarizerConfig
    generator: GeneratorConfig
    controller: ControllerConfig

    @staticmethod
    def load(cls):
        yaml = YAML(typ='safe')
        data = yaml.load('./config.yaml')
        return cls(
            **{key: configs[key](**value) 
               for key, value in data.items()}
        )


class UserHandler:
    def __init__(self) -> None:
        pass

    def ask(self, state: DialogueState) -> None:
        query = input("Введите ваш запрос: ")

    def clarify(self, state: DialogueState) -> None:
        pass

    def answer(self, state: DialogueState) -> None:
        print("Ваш ответ: ", state['answer'])
        