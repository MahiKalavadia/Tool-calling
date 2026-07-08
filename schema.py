from pydantic import BaseModel
from typing import Optional


class NoteSchema(BaseModel):
    note: Optional[str] = None

class TaskSchema(BaseModel):
    task: str