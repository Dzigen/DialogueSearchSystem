from dataclasses import dataclass, field
from ruamel.yaml import YAML
from typing import List, Dict, Union

# USEFUL links
# https://python.langchain.com/v0.1/docs/modules/data_connection/retrievers/vectorstore/
# https://stackoverflow.com/questions/77217193/langchain-how-to-use-a-custom-embedding-model-locally
# https://github.com/langchain-ai/langchain/discussions/9645
# https://python.langchain.com/v0.2/docs/integrations/vectorstores/faiss/
# https://www.kaggle.com/discussions/general/509903
# https://python.langchain.com/v0.1/docs/modules/data_connection/retrievers/ensemble/
# https://api.python.langchain.com/en/latest/retrievers/langchain.retrievers.ensemble.EnsembleRetriever.html


# [threshold, fetch_ks]

@dataclass
class ThresholdRetrieverConfig:
    model_path: str
    densedb_path: str = None
    densedb_kwargs: Dict[str, object] = field(default_factory=lambda: {'allow_dangerous_deserialization':True})

    encode_kwargs: Dict[str, object] = field(default_factory=lambda: {'normalize_embeddings': True, 'prompt': 'query: '})
    model_kwargs: Dict[str, object] = field(default_factory=lambda: {'device': 'cuda'})
    
    params: Dict[str, object] = field(default_factory=lambda: {'fetch_k': 50, 'threshold': 0.9})

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
class BaselineRetrieverConfig: 
    model_path: str
    densedb_path: str = None
    sparsedb_path: str = None

    densedb_kwargs: Dict[str, object] = field(default_factory=lambda: {'allow_dangerous_deserialization':True})
    sparsedb_kwargs: Dict[str, object] = field(default_factory=lambda: {})
    
    encode_kwargs: Dict[str, object] = field(default_factory=lambda: {'normalize_embeddings': True, 'prompt': 'query: '})
    model_kwargs: Dict[str, object] = field(default_factory=lambda: {'device': 'cuda'})
    
    params: Dict[str, Dict[str, object]] = field(default_factory=lambda: {
        'similarity': {'k': 3},
        'bm25': {'k': 3}
        })
    
    weights: List[float] = field(default_factory=lambda: [0.5, 0.5])

@dataclass
class RetrieverConfig:
    mode: str  # custom | baseline
    custom_args: Union[ThresholdRetrieverConfig, BaselineRetrieverConfig] 

    @classmethod
    def load(cls, config_path: str = 'config.yaml'):
        yaml = YAML(typ='safe')
        with open(config_path, 'r', encoding='utf-8') as fd:
            data = yaml.load(fd.read())['retriever']

        if data['mode'] == 'baseline':
            args = BaselineRetrieverConfig(**data['custom_args'])
        elif data['mode'] == 'threshold':
            args = ThresholdRetrieverConfig(**data['custom_args'])
        else:
            raise ValueError

        return cls(mode=data['mode'], custom_args=args)
    
@dataclass
class RawData:
    texts: List[str]
    metadata: List[Dict[str, object]]
