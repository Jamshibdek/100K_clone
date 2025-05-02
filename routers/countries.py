from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud import crud
from schemas import schemas
from models.models import User
from auth import get_current_admin
router = APIRouter()

@router.post("/countries/", response_model=schemas.CountryOut)
def create_country(
    country: schemas.CountryCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
    ):
    return crud.create_country(db=db, country=country)

@router.get("/countries/", response_model=list[schemas.CountryOut])
def read_countries(db: Session = Depends(get_db)):
    return crud.get_countries(db=db)
