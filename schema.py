from pydantic import BaseModel
from typing import Optional


class NoteSchema(BaseModel):
    action: str
    note: str

class TaskSchema(BaseModel):
    action: str
    task: str