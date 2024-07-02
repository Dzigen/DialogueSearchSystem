from src.DocumentsReducer.utils import ReducerConfig, base_config

class ReducerModule:
    def __init__(self, config: ReducerConfig = base_config) -> None:
        self.config = config