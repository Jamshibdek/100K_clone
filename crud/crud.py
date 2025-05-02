from sqlalchemy.orm import Session
from models.models import User, Profile, Category, Product, Transaction, Payment, Order, Region, District, Delivery, Seller, Country, UserAddress,Stream
from schemas.schemas import UserCreate, UserOut, ProfileCreate, CategoryCreate, CategoryOut, ProductCreate, TransactionCreate, PaymentCreate, OrderCreate, RegionCreate, DistrictCreate, DeliveryCreate, SellerCreate, CountryCreate, UserAddressCreate
from fastapi import HTTPException, Depends
from crud import crud
from schemas import schemas
from routers import transactions
from passlib.context import CryptContext
from database import get_db
from schemas.schemas import StreamCreate, StreamOut

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        phone_number=user.phone_number,
        address=user.address,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()



# profiles start //////////////////////////////////////



def create_profile(db: Session, profile: ProfileCreate):
    user = db.query(User).filter(User.id == profile.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User topilmadi")

    region = db.query(Region).filter(Region.id == profile.region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="Viloyat topilmadi")
    district = db.query(Region).filter(Region.id == profile.district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail="Tuman topilmadi")
    product = db.query(Product).filter(Product.id == profile.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product topilmadi")
    
    db_profile = Profile(
        name=profile.name,
        product_id=profile.product_id,
        lastname=profile.lastname,
        region_id=profile.region_id,
        district_id=profile.district_id,
        image=profile.image,
        user_id=profile.user_id
    )

    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_profiles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Profile).offset(skip).limit(limit).all()


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Category).offset(skip).limit(limit).all()


def create_product(db: Session, product: ProductCreate):

    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category topilmadi")
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()

# transaction start ///////////////////////////////////////////////////

def create_transaction(transaction: TransactionCreate, db: Session = Depends(transactions.get_db)):
    # ❗ Profile mavjudligini tekshirish
    profile = db.query(Profile).filter(Profile.id == transaction.profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile topilmadi")
    # total_price = db.query(Profile).filter(Profile.id == transaction.t).first()
    # if type(total_price) == str() :
    #     raise HTTPException(status_code=404, detail="Son kritishin kerak")

    # ❗ Product mavjudligini tekshirish
    product = db.query(Product).filter(Product.id == transaction.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product topilmadi")

    # ✅ Hamma narsa joyida bo‘lsa, Transaction yaratiladi
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Transaction).offset(skip).limit(limit).all()





# payment ///////////////////////////////////////////

def create_payment(db: Session, payment: PaymentCreate):
    transaction = db.query(Transaction).filter(Transaction.id == payment.transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction topilmadi")
    db_payment = Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Payment).offset(skip).limit(limit).all()





# order ///////////////////////////

def create_order(db: Session, order: OrderCreate, user_id: int):
    region = db.query(Region).filter(Region.id == order.region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="Viloyat topilmadi")
    payment = db.query(Payment).filter(Payment.id == order.payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="To‘lov topilmadi")
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product topilmadi")

    # OQIM orqali kelgan bo‘lsa (oqim nomi ID bo'lishi mumkin)
    stream = db.query(Stream).filter(Stream.title == order.oqim, Stream.product_id == product.id).first()
    if stream:
        seller_profile = db.query(Profile).filter(Profile.user_id == stream.seller_id).first()
        if seller_profile:
            seller_profile.suma = (seller_profile.suma or 0) + 30000  # 30 ming so‘m qo‘shiladi

    db_order = Order(**order.dict(), user_id=user_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()





def create_region(db: Session, region: RegionCreate):
    db_region = Region(**region.dict())
    db.add(db_region)
    db.commit()
    db.refresh(db_region)
    return db_region

def get_regions(db: Session):
    return db.query(Region).all()

def create_district(db: Session, district: DistrictCreate):
    region = db.query(Region).filter(Region.id == district.region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="Region topilmadi")
    db_district = District(**district.dict())
    db.add(db_district)
    db.commit()
    db.refresh(db_district)
    return db_district

def get_districts(db: Session):
    return db.query(District).all()


def create_delivery(db: Session, delivery: DeliveryCreate, seller_id: int):
    db_delivery = Delivery(**delivery.dict(), seller_id=seller_id)
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery

def get_deliveries(db: Session):
    return db.query(Delivery).all()


def create_seller(db: Session, seller: SellerCreate):
    product = db.query(Product).filter(Product.id == seller.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product topilmadi")
    # 2. Region mavjudligini tekshir
    region = db.query(Region).filter(Region.id == seller.region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    # 3. Country mavjudligini tekshir
    country = db.query(Country).filter(Country.id == seller.country_id).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    db_seller = Seller(**seller.dict())
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return db_seller

def get_sellers(db: Session):
    return db.query(Seller).all()

def create_country(db: Session, country: CountryCreate):
    db_country = Country(**country.dict())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

def get_countries(db: Session):
    return db.query(Country).all()




# user address 

def create_user_address(db: Session, user_id: int, data: UserAddressCreate):
    region = db.query(Region).filter(Region.id == data.region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="Viloyat topilmadi")
    district = db.query(Region).filter(Region.id == data.district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail="Tuman topilmadi")


    db_address = UserAddress(**data.dict(), user_id=user_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_user_addresses(db: Session, user_id: int):
    return db.query(UserAddress).filter(UserAddress.user_id == user_id).all()


def create_stream(db: Session, stream: StreamCreate, seller_id: int):
    db_stream = Stream(**stream.dict(), seller_id=seller_id)
    db.add(db_stream)
    db.commit()
    db.refresh(db_stream)
    return db_stream