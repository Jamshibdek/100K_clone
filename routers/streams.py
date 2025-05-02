from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.models import User
from schemas.schemas import StreamCreate, StreamOut
from crud import crud
from auth import get_current_seller

router = APIRouter()

@router.post("/streams/", response_model=StreamOut)
def create_stream(stream: StreamCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_seller)):
    return crud.create_stream(db=db, stream=stream, seller_id=current_user.id)
