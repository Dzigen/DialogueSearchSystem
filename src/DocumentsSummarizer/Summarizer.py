from .utils import SummarizerConfig
from ..utils import DialogueState
from ..logger import Logger
from .LLM_Local.llm_local import LLM_model

class SummarizerModule:
    '''
    Класс модуля reader.
    Подаёт на вход модели LLM запрос пользователя вместе с релевантным чанком информации.
    '''


    def __init__(self, config: SummarizerConfig, log:Logger) -> None:

        """
        Инициализация модуля reader.

        Параметры:
        -config: SummarizerConfig: Конфиг reader;
        -log:Logger: Переменная логирования.

        Возвращает: None
        """

        self.log = log
        self.log.info("Initiating Summarizer-class")
        self.config = config

        self.llm = LLM_model(self.config.tech_config, self.config.strat_config)
        
    def prepare_assistant_content(self, state: DialogueState) -> str:
        """
        Функция для отбора релевантного к запросу пользователя чанка информации.

        Параметры:
        -state: DialogueState: объект состояния диалога

        Возвращает: str
        """

        text_chunks = [doc.page_content for doc in state.base_relevant_docs]
        assist_content = '\n\n'.join(text_chunks)
        return assist_content

    @Logger.cls_se_log('''Генерация ответа на основании концентрированного набора релевантных документов''')
    def create_answer(self, state: DialogueState) -> None:
        """
        Функция для генерации ответа по запросу пользователя и чанка релевантной информации.

        Параметры:
        -state: DialogueState: объект состояния диалога

        Возвращает: str
        """

        if len(state.base_relevant_docs) > 0:
            assist_content = self.prepare_assistant_content(state)
            return self.llm.generate(assist_content, state.query)
        else:
            if self.config.strat_config.stream:
                return [{'choices': [{'delta': {'content': self.config.tech_config.stub_answer}}]}]
            else:
                return {'choices': [{'message': {'content': self.config.tech_config.stub_answer}}]}
        
        