from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from routers.users import get_db
from models.models import User
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from crud.crud import create_user
from schemas.schemas import UserCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "dtfctft"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    return db.query(User).filter(User.username == username).first()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username)
    if user is None:
        raise credentials_exception
    return user


@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username}



@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # 🔐 Parolni hash qilish
    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        username=user.username,
        phone_number=user.phone_number,
        address=user.address,
        hashed_password=hashed_password,
        role="user"  # 👈 Faqat user bo‘lishi kerak
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User created successfully", "username": new_user.username}

def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Adminlar uchun ruxsat bor holos")
    return current_user

def get_current_seller(current_user: User = Depends(get_current_user)):
    if current_user.role != "seller":
        raise HTTPException(status_code=403, detail="Faqat sellerlar kirishi mumkin")
    return current_user

def get_current_user_only(current_user: User = Depends(get_current_user)):
    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Faqat oddiy foydalanuvchilar uchun")
    return current_user


















