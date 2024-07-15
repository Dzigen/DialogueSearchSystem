from dataclasses import dataclass
from ruamel.yaml import YAML

@dataclass
class ControllerConfig:
    enable_static: bool
    enable_dynamic: bool


    @classmethod
    def load(cls, config_path: str = 'config.yaml'):
        yaml = YAML(typ='safe')
        with open(config_path, 'r', encoding='utf-8') as fd:
            data = yaml.load(fd.read())
        return cls(**data['controller'])