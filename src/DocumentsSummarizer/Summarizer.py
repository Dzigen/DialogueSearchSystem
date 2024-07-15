from .utils import SummarizerConfig
from ..utils import DialogueState
from ..logger import Logger
from .LLM_Local.llm_local import LLM_model

import requests
import json
from llama_cpp import Llama

class SummarizerModule:
    '''
    sytem_prompt = Ты вопросно-ответная система. Все ответы генерируешь на русском языке. Отвечай коротко по вопросам.
    user_prompt = Ты вопросно-ответная система. Все ответы генерируешь на русском языке. Отвечай коротко по вопросам.
    assistant_prompt = Твоя база знаний, все ответы генерируются на основе текста ниже: \
                4.1.2 Вагон должен соответствовать климатическому исполнению УХЛ1 по ГОСТ 15150 с  \
                обеспе-чением работоспособного состояния в диапазоне рабочих температур от минус 60 °С до плюс 50 °С. 4.1.3 \
                Габарит вагона должен соответствовать требованиям ГОСТ 9238. 4.1.4 Вагон должен иметь кузов, включающий в себя \
                раму с установленными на ней отдельными емкостями (бункерами) для размещения грузов, а также иные устройства, \
                предусмотренные конструк-торской документацией, и должен быть оборудован: а) тележками по ГОСТ 9246 или иному стандарту, \
                    распространяющемуся на тележки грузовых вагонов железных дорог; 6) автосцепными устройствами по ГОСТ 33434 или иному стандарту, \
                распространяющемуся на автосцепные устройства грузовых вагонов, с контуром зацепления автосцепки по ГОСТ 21447, \
                с обо-рудованием автосцепок нижним ограничителем вертикальных перемещений и расцепным приводом с \
                блокировочной цепью и поглощающими аппаратами по ГОСТ 32913; в) автоматическим пневматическим тормозом по ГОСТ 34434; \
                г) стояночным тормозом по ГОСТ 32880. 
    '''


    def __init__(self, config: SummarizerConfig, log) -> None:
        self.log = log
        self.log.info("Initiating Summarizer-class")
        self.config = config

        self.llm = LLM_model(self.config.tech_config, self.config.strat_config)
        
    def prepare_assistant_content(self, state):
        text_chunks = [doc.page_content for doc in state.base_relevant_docs]
        assist_content = '\n\n'.join(text_chunks)
        return assist_content

    @Logger.cls_se_log('''Генерация ответа на основании концентрированного набора релевантных документов''')
    def create_answer(self, state: DialogueState) -> None:

        assist_content = self.prepare_assistant_content(state)

        return self.llm.generate(assist_content, state.query)

        
        
