from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

import models

app = FastAPI()

#CORS Origin
origins = [
    "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create pydantic models
class UserInput(BaseModel):
    username: str
    email: str
    password: str

class UserBase(BaseModel):
    username: str
    email: str
    hashed_password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str
    is_income: bool
    date: str

class TransactionModel(TransactionBase):
    id: int

    class Config:
        orm_mode = True

# database session which can be used in DI
def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        print("DB connection closed")
# DI
db_dependency = Annotated[Session, Depends(get_db)]
#create the tables
models.Base.metadata.create_all(bind=engine)

@app.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserInput, db: db_dependency):
    #hash password 
    newUser =  UserBase(username=user.username,
                                    email=user.email,
                                     hashed_password=user.password + "notreallyhashed")
    db_user = models.User(**newUser.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", status_code=status.HTTP_200_OK)
def read_users(db: db_dependency):
    users = db.query(models.User).all()
    return users

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def read_user(user_id: int, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/transactions/", status_code=status.HTTP_201_CREATED)
def create_transaction(user_id: int, transaction: TransactionBase, db: db_dependency):
    db_transaction = models.Transaction(**transaction.dict(), owner_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction