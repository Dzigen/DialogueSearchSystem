from dataclasses import dataclass, field
from src.CriteriaSelector.utils import SelectorConfig
from src.DocumentsAggregator.utils import AggregatorConfig
from src.DocumentsReducer.utils import ReducerConfig
from src.DocumentsRetriever.utils import RetrieverConfig
from src.DocumentsSummarizer.utils import SummarizerConfig
from src.QuestionGenerator.utils import GeneratorConfig
from src.StopConditionController.utils import ControllerConfig

from ruamel.yaml import YAML
from typing import List

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
    topic: str = None
    question: str = None
    raw_info: List[str] = field(default_factory=lambda: [])
    choices: List[str] = field(default_factory=lambda: [])
    answer: int = None
    filtered_relevant_docs: List[int] = field(default_factory=lambda: [])

@dataclass
class DialogueState:
    query: str = None
    base_relevant_docs: List[str] = None
    history: List[DialogueTurn] = field(default_factory=lambda: [])
    answer: str = None

@dataclass
class DialogueSearchConfig: 
    selector: SelectorConfig = None
    aggregator: AggregatorConfig = None
    reducer: ReducerConfig = None
    retriever: RetrieverConfig = None
    summarizer: SummarizerConfig = None
    generator: GeneratorConfig = None
    controller: ControllerConfig = None

    @classmethod
    def load(cls, config_path: str = 'config.yaml'):
        yaml = YAML(typ='safe')
        with open(config_path, 'r', encoding='utf-8') as fd:
            data = yaml.load(fd.read())
        return cls(
            **{key: configs[key](**value) 
               for key, value in data.items()}
        )


class UserHandler:
    def __init__(self) -> None:
        pass

    def ask(self, state: DialogueState) -> None:
        print("[BOT] Введите ваш запрос")
        query = input("[YOU] ")
        state.query = query

    def clarify(self, state: DialogueState) -> None:
        cur_turn = state.history[-1]
        print(f"[BOT] Уточните следующую информацию:\n{cur_turn.question}")
        for i in range(0, len(cur_turn.choices)):
            print(f"{i+1}. {cur_turn.choices[i]}")
        
        answer = input("[YOU] ")
        state.history[-1].answer = int(answer)

    def answer(self, state: DialogueState) -> None:
        print("[BOT] По вашему запросу был найден следующий ответ:\n", state.answer)
        