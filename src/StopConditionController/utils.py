from dataclasses import dataclass
from ruamel.yaml import YAML

@dataclass
class ControllerConfig:
    enable_static: bool
    enable_dynamic: bool


    @staticmethod
    def load(cls):
        yaml = YAML(typ='safe')
        data = yaml.load('../config.yaml')
        return cls(**data['controller'])