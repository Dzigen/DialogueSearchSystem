from src.DocumentsSummarizer.utils import SummarizerConfig, base_config

class SummarizerModule:
    def __init__(self, config: SummarizerConfig = base_config) -> None:
        self.config = config