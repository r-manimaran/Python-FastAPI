from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional, List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app= FastAPI()
models.Base.metadata.create_all(bind=engine)

# create connection to the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChoiseBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiseBase]

# create dependency injection
db_dependency = Annotated[Session, Depends(get_db)]

## API Endpoints
@app.get("/")
async def home():
    return {"App": "Quiz App with choices"}

@app.post("/questions/")
async def create_question(question: QuestionBase, db: db_dependency):
    # create a question model
    question_model = models.Questions(question_text=question.question_text)
    db.add(question_model)
    db.commit()
    db.refresh(question_model)

    # create choices for the question
    for choice in question.choices:
        choice_model = models.Choices(choice_text=choice.choice_text, 
                                      is_correct=choice.is_correct, 
                                      question_id=question_model.id)
        db.add(choice_model)
    db.commit()

    return {"message": "Question created successfully"}

# Get questions from the DB
@app.get("/questions/", status_code=status.HTTP_200_OK)
async def get_questions(db: db_dependency):
    questions = db.query(models.Questions).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    return {"questions": questions}


# get question by id along with choices
@app.get("/questions/{question_id}", status_code=status.HTTP_200_OK)
async def get_question(question_id: int, db: db_dependency):
    question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    choices = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    return {"question": question, "choices": choices}