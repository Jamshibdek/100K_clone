from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import crud
from schemas import schemas

from database import get_db
from models.models import User
from auth import get_current_admin

router = APIRouter()



# @router.post("/users/", response_model=schemas.UserOut)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     return crud.create_user(db=db, user=user)

@router.get("/users/", response_model=list[schemas.UserOut])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    return crud.get_users(db=db, skip=skip, limit=limit)


