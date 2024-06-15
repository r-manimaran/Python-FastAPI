from pydantic import BaseModel, Field
from typing import Optional
from sqlmodel import SQLModel, Session, create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
from sqlalchemy import String
#Model : Pydantic Model + Sql Model : Serialization, validation and DB

class BookModel(SQLModel):
    title: str = Field(index=True)
    author: str
    description: Optional[str]
    isbn: str = Field(min_length=4,max_length=13, default_factory="0011")

# serialization and validation
class Book(BaseModel):
    title: str
    author: str
    description: Optional[str]
    isbn: str

    class Config:
        orm_mode = True

#database
Base = declarative_base()
class BookModel(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    isbn = Column(String)