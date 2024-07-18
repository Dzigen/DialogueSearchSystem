from .utils import ThresholdRetrieverConfig, RawData
from ..utils import DialogueState
from ..logger import Logger

from typing import Dict
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import ConfigurableField
import pickle

class ThresholdRetriever:
    def __init__(self, config: ThresholdRetrieverConfig, log, data: RawData = None) -> None:
        self.log = log
        self.log.info("Initiating ThresholdRetriever")
        self.config = config

        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.config.model_path,
            model_kwargs=self.config.model_kwargs,
            encode_kwargs=self.config.encode_kwargs
        )

        if data is None:
            self.densedb = FAISS.load_local(
                self.config.densedb_path, self.embeddings, 
                **self.config.densedb_kwargs)
        else:
            self.densedb = FAISS.from_texts(
                data.texts, self.embeddings, data.metadata,
                **self.config.densedb_kwargs)
        
    def invoke(self, query: str):
        docs_with_scores = self.densedb.similarity_search_with_score(query, k=self.config.params['fetch_k'])
        filtered_docs_with_scores = list(filter(lambda item: item[1] > self.config.params['threshold'], docs_with_scores))
        relevant_docs = list(map(lambda item: item[0], filtered_docs_with_scores))[:self.config.params['max_k']]

        return relevant_docs   