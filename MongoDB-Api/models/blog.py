import datetime
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    author: str
    tags: list[str] = []
    published: bool = False
    