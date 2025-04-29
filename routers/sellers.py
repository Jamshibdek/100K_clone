from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud import crud
from schemas import schemas

router = APIRouter()

@router.post("/sellers/", response_model=schemas.SellerOut)
def create_seller(seller: schemas.SellerCreate, db: Session = Depends(get_db)):
    return crud.create_seller(db=db, seller=seller)

@router.get("/sellers/", response_model=list[schemas.SellerOut])
def read_sellers(db: Session = Depends(get_db)):
    return crud.get_sellers(db=db)
