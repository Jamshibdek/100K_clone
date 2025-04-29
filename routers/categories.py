from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud import crud
from schemas import schemas
from auth import get_current_admin  # 🔐 faqat adminlar uchun
from models.models import User

router = APIRouter()

# ✅ Faqat ADMIN kiritishi mumkin
@router.post("/categories/", response_model=schemas.CategoryOut)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)  # 🔐 admin check
):
    return crud.create_category(db=db, category=category)

# 🟢 Har kim ko‘ra oladi (public)
@router.get("/categories/", response_model=list[schemas.CategoryOut])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_categories(db=db, skip=skip, limit=limit)
