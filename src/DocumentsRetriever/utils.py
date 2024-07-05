from dataclasses import dataclass
from ruamel.yaml import YAML

@dataclass
class RetrieverConfig:
    model: str
    N_docs: int

    @staticmethod
    def load(cls, config_path: str = 'config.yaml'):
        yaml = YAML(typ='safe')
        with open(config_path, 'r', encoding='utf-8') as fd:
            data = yaml.load(fd.read())
        return cls(**data['retriever'])