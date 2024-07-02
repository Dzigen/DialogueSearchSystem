from src.DocumentsAggregator.utils import AggregatorConfig, base_config

class AggregatorModule:
    def __init__(self, config: AggregatorConfig = base_config) -> None:
        self.config = config