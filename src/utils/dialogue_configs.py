from dataclasses import dataclass, field
from langchain_core.documents.base import Document
from typing import List
import enum

class DialogueStatus(enum.Enum):
    created = 0
    base_retrieval = 1
    dialogue_continue_ask = 2

    criteria_selection = 3
    documents_aggregation = 4
    mcq_generation = 5

    clarifying_awaiting = 6
    documents_reduction = 7
    
    documents_summarization = 8



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
    status: DialogueStatus = DialogueStatus.created