from src.DocumentsRetriever.utils import RetrieverConfig

class RetrieverModule:
    def __init__(self, config: RetrieverConfig) -> None:
        self.config = config