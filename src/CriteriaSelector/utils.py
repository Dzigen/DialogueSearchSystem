from dataclasses import dataclass
from ruamel.yaml import YAML

@dataclass
class SelectorConfig:
    enable_static: bool
    enable_dunamic: bool
    N_clusters: int
    K_keywords: int

    @classmethod
    def load(cls, config_path: str = 'config.yaml'):
        yaml = YAML(typ='safe')
        with open(config_path, 'r', encoding='utf-8') as fd:
            data = yaml.load(fd.read())
        return cls(**data['selector'])