from typing import List
from pydantic import BaseModel

#create Person Schema
class PersonCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    is_active: bool = True

#create Person Base Model
class Person(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    is_active: bool = True
    
    class Config:
        orm_mode = True

class PersonResponse(BaseModel):
    data: Person
    
class PersonListResponse(BaseModel):
    data: List[Person]