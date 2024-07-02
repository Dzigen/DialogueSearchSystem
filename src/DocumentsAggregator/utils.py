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
        data = yaml.load('../config.yaml')
        return cls(**data['aggregator'])