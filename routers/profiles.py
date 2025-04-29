from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import crud
from schemas import schemas
from database import get_db
from database import get_db
from auth import get_current_user
from models.models import Profile, User, Delivery, Order
router = APIRouter()



@router.post("/profiles/", response_model=schemas.ProfileOut)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    return crud.create_profile(db=db, profile=profile)

@router.get("/profiles/", response_model=list[schemas.ProfileOut])
def read_profiles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_profiles(db=db, skip=skip, limit=limit)



# routers/profiles.py





@router.get("/my-profile", response_model=schemas.ProfileOut)
def read_own_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile topilmadi")
    return profile


@router.get("/my-deliveries", response_model=list[schemas.DeliveryOut])
def read_own_deliveries(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Delivery).filter(Delivery.seller_id == current_user.id).all()


@router.get("/my-orders", response_model=list[schemas.OrderOut])
def read_own_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Order).filter(Order.user_id == current_user.id).all()
