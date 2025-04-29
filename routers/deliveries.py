from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import schemas
from crud import crud
from models import models
from auth import get_current_seller  # 🔐 seller role-check
from models.models import User

router = APIRouter()

# 🟢 Faqat SELLER o'zining delivery qo‘sha oladi
@router.post("/deliveries/", response_model=schemas.DeliveryOut)
def create_delivery(
    delivery: schemas.DeliveryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_seller)  # 🔒 faqat sellerlar
):
    return crud.create_delivery(db=db, delivery=delivery, seller_id=current_user.id)

# 🟢 Faqat SELLER o‘zining delivery’larini ko‘radi
@router.get("/my-deliveries/", response_model=list[schemas.DeliveryOut])
def read_my_deliveries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_seller)
):
    return db.query(models.Delivery).filter(models.Delivery.seller_id == current_user.id).all()
