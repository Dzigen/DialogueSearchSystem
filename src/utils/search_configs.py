from ..CriteriaSelector.utils import SelectorConfig
from ..DocumentsAggregator.utils import AggregatorConfig
from ..DocumentsReducer.utils import ReducerConfig
from ..DocumentsRetriever.utils import RetrieverConfig
from ..DocumentsSummarizer.utils import SummarizerConfig
from ..QuestionGenerator.utils import GeneratorConfig
from ..StopConditionController.utils import ControllerConfig
from ..logger import Logger
from . import DialogueState

from dataclasses import dataclass, field
from langchain_core.documents.base import Document
from ruamel.yaml import YAML
from time import time
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

def create_id(hash_len=8) -> float:
    return hash(time()) % (10 ** hash_len)

def get_hash(value: str, hash_len: int = 8) -> float:
    return hash(value) % (10 ** hash_len)

class UserHandler:
    def __init__(self, log) -> None:
        self.log = log
        self.log.info("Initiating UserHandler-class")

    @Logger.cls_se_log("Ожидаем запрос от пользователя")
    def ask(self, state: DialogueState) -> None:
        print("[BOT] Введите ваш запрос")
        query = input("[YOU] ")
        state.query = query

    @Logger.cls_se_log("Ожидаем уточняющий ответ от пользователя")
    def clarify(self, state: DialogueState) -> None:
        cur_turn = state.history[-1]
        print(f"[BOT] Уточните следующую информацию:\n{cur_turn.question}")
        for i in range(0, len(cur_turn.choices)):
            print(f"{i+1}. {cur_turn.choices[i]}")
        
        answer = input("[YOU] ")
        state.history[-1].answer = int(answer)

    @Logger.cls_se_log("Отправляет финальный ответ системы пользователяю")
    def answer(self, state: DialogueState) -> None:
        print("[BOT] По вашему запросу был найден следующий ответ:\n", state.answer)
        