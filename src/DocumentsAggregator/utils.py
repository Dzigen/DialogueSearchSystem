from dataclasses import dataclass
from ruamel.yaml import YAML

@dataclass
class AggregatorConfig:
    extractor_model: str
    generalizer_model: str
    K_topics: int
   
    @staticmethod
    def load(cls):
        yaml = YAML(typ='safe')
        with open("../config.yaml", 'r', encoding='utf-8') as fd:
            data = yaml.load(fd.read())
        return cls(**data['aggregator'])