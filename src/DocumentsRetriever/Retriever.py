from src.DocumentsRetriever.utils import RetrieverConfig, RawData
from src.utils import DialogueState
from src.logger import Logger

from typing import Dict
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers import BM25Retriever
from langchain_core.runnables import ConfigurableField
import pickle

class RetrieverModule:
    def __init__(self, config: RetrieverConfig, log, data: RawData = None) -> None:
        self.log = log
        self.log.info("Initiating Retriever-class")
        self.config = config

        # 
        if ('similarity' in self.config.params.keys()) or ('mmr' in self.config.params.keys()):
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.config.model_path,
                model_kwargs=self.config.model_kwargs,
                encode_kwargs=self.config.encode_kwargs
            )

            if data is None:
                self.densedb = FAISS.load_local(self.config.densedb_path, self.embeddings, 
                                                **self.config.densedb_kwargs)
            else:
                self.densedb = FAISS.from_texts(data.texts, self.embeddings, data.metadata, 
                                            **self.config.densedb_kwargs)

        #
        if 'bm25' in self.config.params.keys():
            if data is None:
                file = open(self.config.sparsedb_path,'rb')
                self.bm25_retriever = pickle.load(file)
                file.close()
            else:
                self.bm25_retriever = BM25Retriever(data.texts, data.metadata, **self.config.sparsedb_kwargs) 
                
            self.bm25_retriever.k = self.config.params['bm25']['k']

        #
        if len(self.config.params) > 1:
            tmp_retrivers = []
            for s_type in self.config.params.keys():
                if s_type == 'bm25':
                    tmp_retrivers.append(self.bm25_retriever)
                else:
                    tmp_retrivers.append(self.densedb.as_retriever(
                        search_type=s_type, search_kwargs=self.config.params[s_type]))

            self.retriever = EnsembleRetriever(retrievers=tmp_retrivers, 
                                               weights=self.config.weights)
        else:
            s_type = list(self.config.params.keys())[0]
            if s_type == 'bm25':
                self.retriever = self.bm25_retriever
            else:
                self.retriever = self.densedb.as_retriever(
                    search_type=s_type, search_kwargs=self.config.params[s_type])

    @Logger.cls_se_log('''Формирование базового набора релевантных документов''')
    def base_search(self, state: DialogueState):
        state.base_relevant_docs = self.retriever.invoke(state.query)         
