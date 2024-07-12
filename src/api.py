from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

from src.utils import DialogueSearchConfig
from src.dialogue_loop import DialogueSearch

dialogue_config = DialogueSearchConfig.load()
dialogue_system = DialogueSearch(dialogue_config)
app = FastAPI()

class RequestBody(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/question_answering_service")
def read_item(body: RequestBody):

    final_state = dialogue_system.start(query=body.query)

    return {
        'answer': final_state.answer, 
        'context': final_state.base_relevant_docs
        }