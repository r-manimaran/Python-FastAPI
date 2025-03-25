
from fastapi import APIRouter, status
from requests import Session
from database import SessionLocal
import logging_config
import crud, models, schemas

import schemas
from fastapi import Depends
from fastapi import HTTPException

router = APIRouter(
    prefix="/todos",
    responses={404: {"description": "Not found"}}
)

# setup logging
logger = logging_config.setup_logging()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        logger.info("Database connection closed")

@router.post("", response_model=schemas.Todo, status_code = status.HTTP_201_CREATED)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)

@router.get("/", status_code=status.HTTP_200_OK)
def read_todos(db:Session = Depends(get_db)):
    return crud.get_todos(db=db)
    

@router.get("/{todo_id}",status_code=status.HTTP_200_OK)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    return crud.get_todo_by_id(db=db, todo_id=todo_id)

@router.put("/{todo_id}", status_code=status.HTTP_202_ACCEPTED)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    todo = crud.update_todo(db=db, todo_id=todo_id, todo=todo)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.patch("/{todo_id}/complete",status_code=status.HTTP_202_ACCEPTED)
def complete_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    todo = crud.update_todo_Status(db=db, todo_id=todo_id,todo = todo)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    res = crud.delete_todo(db=db, todo_id=todo_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return {"message": "Todo deleted successfully"}
    