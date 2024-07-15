from dataclasses import dataclass
from typing import DefaultDict
from ruamel.yaml import YAML

from .LLM_Local import LLM_Hardw_Conf, LLM_Hyper_Conf

configs = {
    'tech_config': LLM_Hardw_Conf,
    'strat_config': LLM_Hyper_Conf
}

@dataclass
class SummarizerConfig:

    tech_config: LLM_Hardw_Conf = None
    strat_config: LLM_Hyper_Conf = None

    @classmethod
    def load(cls, config_path: str = 'config.yaml'):
        yaml = YAML(typ='safe')
        with open(config_path, 'r', encoding='utf-8') as fd:
            data = yaml.load(fd.read())
        return cls(
            **{key: configs[key](**value) 
               for key, value in data['summarizer'].items()}
        )