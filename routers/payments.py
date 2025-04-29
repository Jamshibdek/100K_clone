from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import crud
from schemas import schemas
from database import get_db
router = APIRouter()



@router.post("/payments/", response_model=schemas.PaymentOut)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    return crud.create_payment(db=db, payment=payment)

@router.get("/payments/", response_model=list[schemas.PaymentOut])
def read_payments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_payments(db=db, skip=skip, limit=limit)
