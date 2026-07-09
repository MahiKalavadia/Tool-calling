from pydantic import BaseModel, Field
from typing import Optional, List


class NoteSchema(BaseModel):
    note: Optional[str] = None

class TaskSchema(BaseModel):
    task: str

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

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

class abc(BaseModel):
    id: Optional[int] = Field(None, description="The ID of the item")
    note: Optional[str] = Field(None, description="The note content")
    task: Optional[str] = Field(None, description="The task content")
    status: Optional[str] = Field(None, description="The status of the task")