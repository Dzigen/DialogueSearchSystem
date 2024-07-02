from dataclasses import dataclass
from ruamel.yaml import YAML

@dataclass
class ReducerConfig:
    model: str

    @staticmethod
    def load(cls):
        yaml = YAML(typ='safe')
        data = yaml.load('../config.yaml')
        return cls(**data['reducer'])