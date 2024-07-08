from dataclasses import dataclass

@dataclass
class llmConfig:
   stream: bool = True
   temperature: float = 0.8
   max_tokens: int = 300