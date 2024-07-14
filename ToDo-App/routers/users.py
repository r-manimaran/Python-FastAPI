import os
from typing import Optional
from fastapi import Depends, HTTPException, APIRouter, status, Request, Form
from pydantic import BaseModel, Field

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter(
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

