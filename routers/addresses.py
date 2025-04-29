from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from models.models import User
from crud import crud
from schemas import schemas

router = APIRouter()

@router.post("/addresses/", response_model=schemas.UserAddressOut)
def add_address(data: schemas.UserAddressCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_user_address(db=db, user_id=current_user.id, data=data)

@router.get("/my-addresses/", response_model=list[schemas.UserAddressOut])
def get_my_addresses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_user_addresses(db=db, user_id=current_user.id)
