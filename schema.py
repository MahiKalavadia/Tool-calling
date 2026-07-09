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

class Note(BaseModel):
    id: int
    note: str

class NoteViewSchema(BaseModel):
    note: List[Note]

class Task(BaseModel):
    id: int
    task: str
    status: str

class TaskViewSchema(BaseModel):
    task: List[Task]