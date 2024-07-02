from dataclasses import dataclass
from ruamel.yaml import YAML

@dataclass
class RetrieverConfig:
    model: str
    N_docs: int

    @staticmethod
    def load(cls):
        yaml = YAML(typ='safe')
        data = yaml.load('../config.yaml')
        return cls(**data['retriever'])