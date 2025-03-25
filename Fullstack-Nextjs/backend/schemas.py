from typing import Optional
from pydantic import BaseModel, ConfigDict


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int
    complete: bool = False

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    complete: Optional[bool] = None

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: int
    complete: bool = False

    model_config = ConfigDict(from_attributes=True)