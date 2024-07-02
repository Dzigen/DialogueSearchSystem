from dataclasses import dataclass
from src.CriteriaSelector.utils import SelectorConfig
from src.DocumentsAggregator.utils import AggregatorConfig
from src.DocumentsReducer.utils import ReducerConfig
from src.DocumentsRetriever.utils import RetrieverConfig
from src.DocumentsSummarizer.utils import SummarizerConfig
from src.QuestionGenerator.utils import GeneratorConfig
from src.StopConditionController.utils import ControllerConfig

from ruamel.yaml import YAML
from typing import List, Dict

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
class DialogueTurn:
    topic: str
    question: str
    choices: List[str]
    answer: int
    filtered_relevant_docs: List[int]

@dataclass
class DialogueState:
    query: str
    base_relevant_docs: List[str]
    history: List[DialogueTurn]
    answer: str

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
        query = input("[BOT] Введите ваш запрос\n[YOU] ")
        state['query'] = query

    def clarify(self, state: DialogueState) -> None:
        cur_turn = state['history'][-1]
        print(f"[BOT] Уточните следующую информацию:\n{cur_turn['question']}")
        for i in range(0, cur_turn['choices']):
            print(f"{i+1}. {cur_turn['choices'][i]}")
        
        answer = input("[YOU] ")
        state['history'][-1]['answer'] = int(answer)

    def answer(self, state: DialogueState) -> None:
        print("[BOT] По вашему запросу был найден следующий ответ:\n", 
              state['answer'])
        