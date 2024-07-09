from dataclasses import dataclass, field
from ruamel.yaml import YAML
from typing import List, Dict

# USEFUL links
# https://python.langchain.com/v0.1/docs/modules/data_connection/retrievers/vectorstore/
# https://stackoverflow.com/questions/77217193/langchain-how-to-use-a-custom-embedding-model-locally
# https://github.com/langchain-ai/langchain/discussions/9645
# https://python.langchain.com/v0.2/docs/integrations/vectorstores/faiss/
# https://www.kaggle.com/discussions/general/509903
# https://python.langchain.com/v0.1/docs/modules/data_connection/retrievers/ensemble/
# https://api.python.langchain.com/en/latest/retrievers/langchain.retrievers.ensemble.EnsembleRetriever.html

# Есть 5 возможных конфигураций алгоритма поиска релевантных фрагментов в базе документов
# 1. simmilarity + mmr + bm25
# 2. simmilarity + mmr
# 3. simmilarity
# 4. mmr
# 5. bm25

#k: Amount of documents to return (Default: 4)
#score_threshold: Minimum relevance threshold for similarity_score_threshold
#fetch_k: Amount of documents to pass to MMR algorithm (Default: 20) 
#lambda_mult: Diversity of results returned by MMR; 1 for minimum diversity and 0 for maximum. (Default: 0.5)

# Настраиваемые параметры у каждого из алгоритмов
# similarity - [k]
# mmr - [k, fetch_k, lambda_mult]
# bm25 - [k]

@dataclass
class RetrieverConfig:
    model_path: str

    densedb_path: str
    sparsedb_path: str

    densedb_kwargs: Dict[str, object] = field(default_factory=lambda: {'allow_dangerous_deserialization':True})
    sparsedb_kwargs: Dict[str, object] = field(default_factory=lambda: {})
    
    encode_kwargs: Dict[str, object] = field(default_factory=lambda: {'normalize_embeddings': False, 'prompt': 'query: '})
    model_kwargs: Dict[str, object] = field(default_factory=lambda: {'device': 'cuda'})
    
    params: Dict[str, Dict[str, object]] = field(default_factory=lambda: {
        'similarity': {'k': 4}
        #'mmr': {'lambda_mult': 0.5, 'fetch_k': 20, 'k': 4}, 
        #'bm25': {'k': 4}
        })
    
    weights: List[float] = field(default_factory=lambda: [0.6, 0.4])

    @staticmethod
    def load(cls, config_path: str = 'config.yaml'):
        yaml = YAML(typ='safe')
        with open(config_path, 'r', encoding='utf-8') as fd:
            data = yaml.load(fd.read())
        return cls(**data['retriever'])
    
@dataclass
class RawData:
    texts: List[str]
    metadata: List[Dict[str, object]]
