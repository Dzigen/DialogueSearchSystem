from src.CriteriaSelector.DynamicSelector import DynamicSelector
from src.CriteriaSelector.StaticSelector import StaticSelector
from src.CriteriaSelector.utils import SelectorConfig, base_config

class SelectorModule:
    def __init__(self, config: SelectorConfig = base_config) -> None:
        self.config = SelectorConfig