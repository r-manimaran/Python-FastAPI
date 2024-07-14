import os
from typing import Optional
from fastapi import Depends, HTTPException, APIRouter, status, Request
from pydantic import BaseModel, Field
from passlib.context import CryptContext
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


SECRET_KEY = "1a2b3cd5e6f7g8h9i0j0k9l8m7n6o5p4q4rs2t1u2v5w34y8z"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/auth", # this is going to be the root of the api endpoint for auth
    tags=["auth"], # this is going to be the group of the api endpoint for auth
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

def get_password_hash(password):
    return bcrypt_context.hash(password)

class User(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    
class UserLogin(BaseModel):
    username: str
    password: str

#register the new user
@router.post("/register")
async def register_new_user(request: User, db: Session = Depends(get_db)):
    new_user = models.Users(
        username=request.username,
        hashed_password=get_password_hash(request.password),
        email=request.email,
        first_name=request.first_name,
        last_name=request.last_name,
        is_active=True,
        created_by="system"        
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#login the user
@router.post("/login")
async def login_user(request: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not bcrypt_context.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    return user