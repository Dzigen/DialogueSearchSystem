from src.DocumentsRetriever.utils import RetrieverConfig
from src.utils import DialogueState
from src.logger import Logger

from typing import Dict
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.retrievers import EnsembleRetriever
from langchain_core.runnables import ConfigurableField

class RetrieverModule:
    def __init__(self, config: RetrieverConfig, log) -> None:
        self.log = log
        self.log.info("Initiating Retriever-class")
        self.config = config

        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.config.model_path,
            model_kwargs=self.config.model_kwargs,
            encode_kwargs=self.config.encode_kwargs
        )
        self.vectordb = FAISS.load_local(self.config.vectordb_path, self.embeddings)

    @Logger.cls_se_log('''Извлечение релевантного набора документов из базы знаний''')
    def retrieve(self, query: str, s_type: str, s_config: Dict[str,object]):
        retriever = self.vectordb.as_retriever(search_type=s_type, search_kwargs=s_config)
        return retriever.invoke(query)

    @Logger.cls_se_log('''Формирование базового набора релевантных документов''')
    def base_search(self, state: DialogueState, s_type=None, s_config=None):
        if s_type is None and s_config is None:
            s_type, s_config = self.config.base_search_type, self.config.base_search_config

        state.base_relevant_docs = self.retrieve(state.query, s_type, s_config)
        
