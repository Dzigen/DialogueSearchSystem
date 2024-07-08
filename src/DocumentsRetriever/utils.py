from dataclasses import dataclass
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

@dataclass
class RetrieverConfig:
    model_path: str
    model_kwargs: dict
    encode_kwargs: dict
    vectordb_path: str
    base_search_type: str # similarity | similarity_score_threshold
    base_search_config: Dict[str, object] # score_threshold | score_threshold | k

    @staticmethod
    def load(cls, config_path: str = 'config.yaml'):
        yaml = YAML(typ='safe')
        with open(config_path, 'r', encoding='utf-8') as fd:
            data = yaml.load(fd.read())
        return cls(**data['retriever'])
    
@dataclass
class RawData:
    texts: List[str]
    metadata: List[dict]
