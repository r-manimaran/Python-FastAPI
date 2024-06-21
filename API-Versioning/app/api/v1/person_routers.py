from fastapi import APIRouter, Depends, HTTPException
from app.database import SessionLocal
from sqlalchemy.orm import Session

from models.v1 import person as person_model_v1
from schemas.v1 import person_schema as person_schema_v1
from starlette import status

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/v1/persons",
    tags=["Person"],
    responses={404: {"description": "Not found"}},
)

@router.get("", response_model=person_schema_v1.PersonListResponse, status_code=status.HTTP_200_OK)
def get_persons(db: Session = Depends(get_db)):
    persons_list = db.query(person_model_v1.Person).all()
    return {"data": persons_list}

@router.post("", response_model=person_schema_v1.PersonResponse, status_code=status.HTTP_201_CREATED)
def create_person(person: person_schema_v1.Person, db: Session = Depends(get_db)):
    new_person = person_model_v1.Person(first_name=person.first_name, 
                                        last_name=person.last_name,
                                        email=person.email)
    
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return {"data":new_person}

@router.get("/{id}", response_model=person_schema_v1.PersonResponse, status_code=status.HTTP_200_OK)
def get_person(id: int, db: Session = Depends(get_db)):
    person = db.query(person_model_v1.Person).filter(person_model_v1.Person.id == id).first()
    if not person:
        raise HTTPException(status_code=404, detail=f"Person with id {id} not found")
    return {"data": person}

@router.put("/{id}", response_model=person_schema_v1.PersonResponse, status_code=status.HTTP_200_OK)
def update_person(id: int, person: person_schema_v1.Person, db: Session = Depends(get_db)):
    existing_person = db.query(person_model_v1.Person).filter(person_model_v1.Person.id == id).first()
    if not existing_person:
        raise HTTPException(status_code=404, detail=f"Person with id {id} not found")

    existing_person.first_name = person.first_name
    existing_person.last_name = person.last_name
    existing_person.email = person.email

    db.commit()
    db.refresh(existing_person)

    return {"data": existing_person}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(id: int, db: Session = Depends(get_db)):
    person = db.query(person_model_v1.Person).filter(person_model_v1.Person.id == id).first()
    if not person:
        raise HTTPException(status_code=404, detail=f"Person with id {id} not found")

    db.delete(person)
    db.commit()

    return {"data": None}