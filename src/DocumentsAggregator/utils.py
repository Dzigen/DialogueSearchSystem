from dataclasses import dataclass
from ruamel.yaml import YAML

@dataclass
class AggregatorConfig:
    extractor_model: str
    generalizer_model: str
    K_topics: int
   
    @classmethod
    def load(cls, config_path: str = 'config.yaml'):
        yaml = YAML(typ='safe')
        with open(config_path, 'r', encoding='utf-8') as fd:
            data = yaml.load(fd.read())
        return cls(**data['aggregator'])