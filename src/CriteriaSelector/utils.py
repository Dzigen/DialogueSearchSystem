from dataclasses import dataclass
from ruamel.yaml import YAML

@dataclass
class SelectorConfig:
    enable_static: bool
    enable_dunamic: bool
    N_clusters: int
    K_keywords: int

    @staticmethod
    def load(cls):
        yaml = YAML(typ='safe')
        data = yaml.load('../config.yaml')
        return cls(**data['selector'])