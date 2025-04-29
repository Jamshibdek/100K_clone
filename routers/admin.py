from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_admin
from models.models import User
from schemas.schemas import UserOut

router = APIRouter()

@router.put("/admin/make-seller/{user_id}", response_model=UserOut)
def make_user_seller(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)  # faqat admin
):
    # ❌ O‘ZINI O‘ZI SELLER QILA OLMAYDI
    if user_id == current_admin.id:
        raise HTTPException(status_code=403, detail="Siz o‘zingizni seller qila olmaysiz")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User topilmadi")
    
    if user.role == "seller":
        raise HTTPException(status_code=400, detail="Bu user allaqachon seller")

    user.role = "seller"
    db.commit()
    db.refresh(user)
    return user

