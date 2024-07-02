from src.CriteriaSelector.DynamicSelector import DynamicSelector
from src.CriteriaSelector.StaticSelector import StaticSelector
from src.CriteriaSelector.utils import SelectorConfig

class SelectorModule:
    def __init__(self, config: SelectorConfig) -> None:
        self.config = config