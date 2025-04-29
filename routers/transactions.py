from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import crud
from schemas import schemas
from database import get_db
router = APIRouter()


@router.post("/transactions/", response_model=schemas.TransactionOut)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db=db, transaction=transaction)

@router.get("/transactions/", response_model=list[schemas.TransactionOut])
def read_transactions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_transactions(db=db, skip=skip, limit=limit)
