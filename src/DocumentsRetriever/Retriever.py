from .utils import RetrieverConfig, RawData
from .BaselineRetriever import BaselineRetriever
from .ThresholdRetriever import ThresholdRetriever
from ..utils import DialogueState
from ..logger import Logger

from typing import Dict
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import pickle

class RetrieverModule:
    def __init__(self, config: RetrieverConfig, log, data: RawData = None) -> None:
        self.log = log
        self.log.info("Initiating Retriever-class")
        self.config = config

        if self.config.mode == 'baseline':
            self.retriever = BaselineRetriever(self.config.custom_args, log, data)
        elif self.config.mode == 'threshold':
            self.retriever = ThresholdRetriever(self.config.custom_args, log, data)
        else:
            raise ValueError
    
    @Logger.cls_se_log('''Формирование базового набора релевантных документов''')
    def base_search(self, state: DialogueState, **kwargs):
        state.base_relevant_docs = self.retriever.invoke(state.query, **kwargs)     
