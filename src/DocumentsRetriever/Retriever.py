from src.DocumentsRetriever.utils import RetrieverConfig, base_config

class RetrieverModule:
    def __init__(self, config: RetrieverConfig = base_config) -> None:
        self.config = config