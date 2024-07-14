import os
from typing import Optional
from fastapi import Depends, HTTPException, APIRouter, status, Request, Form
from pydantic import BaseModel, Field

from logging_config import setup_logging
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

#Added Logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
setup_logging()

router = APIRouter(
    prefix="/api", # this will be the prefix for all routes
    tags=["todos"], # this will be the group of all routes
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not found"
        }
    }
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
models.Base.metadata.create_all(bind=engine)

class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description='Priority must be between 1-5')
    complete: bool = False
    

# add new Todo item
@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(todos: Todo, db: Session = Depends(get_db)):
    logging.debug("Entering the Create_todo method with {todos}")
    todo_model = models.Todos()
    todo_model.title = todos.title
    todo_model.description = todos.description
    todo_model.priority = todos.priority
    todo_model.complete = todos.complete
    todo_model.owner_id = 1
    todo_model.created_by = "system"
    todo_model.modified_by = "system"
    db.add(todo_model)
    db.commit()
    logging.info("Todo item created successfully")
    return {"status": status.HTTP_201_CREATED, "transaction": "Successful"}

# Get all todos
@router.get('/todo', status_code=status.HTTP_200_OK)
async def get_all_todos(db: Session = Depends(get_db)):
    logging.debug("Entering the get_all_todos method")
    # return all todos from the database
    return db.query(models.Todos).all()