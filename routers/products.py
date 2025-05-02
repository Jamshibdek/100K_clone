from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import crud
from schemas import schemas
from database import get_db
from models.models import User
from auth import get_current_seller
router = APIRouter()


@router.post("/products/", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_seller)):
    return crud.create_product(db=db, product=product)

@router.get("/products/", response_model=list[schemas.ProductOut])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_products(db=db, skip=skip, limit=limit)
