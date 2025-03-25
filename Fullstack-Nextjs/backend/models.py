from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    priority = Column(Integer, nullable=False)
    complete = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False)
