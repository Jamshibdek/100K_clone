from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.schemas import OrderCreate, OrderOut
from crud.crud import create_order, get_orders
from auth import get_current_user
from models.models import User

router = APIRouter()

@router.post("/orders/", response_model=OrderOut)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_order(db=db, order=order, user_id=current_user.id)

@router.get("/orders/", response_model=list[OrderOut])
def read_my_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_orders(db=db, user_id=current_user.id)
