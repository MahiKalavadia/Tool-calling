from pydantic import BaseModel, Field
from typing import Optional, List, Any


class NoteSchema(BaseModel):
    note: Optional[str] = None

class TaskSchema(BaseModel):
    task: str

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: Any
