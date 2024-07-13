from sqlalchemy import String, Boolean, DateTime, Integer, Double, ForeignKey, Column,func
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import func

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(225))
    is_active = Column(Boolean, default=True)
    created_by = Column(String(100),nullable=False)
    created_on = Column(DateTime, nullable=False, default=func.now())

    todos = relationship("Todos", back_populates="owner")

    def __repr__(self):
        return f"<User {self.username}>"

class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(225), nullable=False)
    description = Column(String(225), nullable=False)
    priority = Column(Integer, nullable=False)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_on = Column(DateTime, nullable=False, default=func.now())
    created_by = Column(String(100), nullable=False)
    modified_on = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    modified_by = Column(String(100), nullable=False)

    owner = relationship("Users", back_populates="todos")

    def __repr__(self):
        return f"<Todo {self.title}>"
