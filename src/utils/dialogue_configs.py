from dataclasses import dataclass, field
from langchain_core.documents.base import Document
from ruamel.yaml import YAML
from time import time
from typing import List

@dataclass
class DialogueTurn:
    topic: str = None
    question: str = None
    raw_info: List[str] = field(default_factory=lambda: [])
    choices: List[str] = field(default_factory=lambda: [])
    answer: int = None
    filtered_relevant_docs: List[int] = field(default_factory=lambda: [])

@dataclass
class DialogueState:
    query: str = None
    base_relevant_docs: List[Document] = None
    history: List[DialogueTurn] = field(default_factory=lambda: [])
    answer: str = None