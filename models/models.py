from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from datetime import datetime
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    phone_number = Column(String, unique=True, index=True)
    address = Column(String)
    hashed_password = Column(String)
    role = Column(String, default="user")  # ✅ SHU YERGA QO‘SHILADI

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)




class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    product_id = Column(Integer)
    lastname = Column(String)
    region_id = Column(Integer)
    district_id = Column(Integer)
    image = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String)
    name = Column(String)
    type = Column(String)



class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    quantity = Column(Integer)
    description = Column(String)
    video_id = Column(Integer)
    price = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))
    attribute_id = Column(Integer)

    category = relationship("Category")




class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    total_price = Column(Integer)
    status = Column(String)  # "pending", "paid", "cancelled"
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("Profile")
    product = relationship("Product")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    amount = Column(Integer)
    payment_type = Column(String)  # "click", "payme", "naqd", "karta"
    status = Column(String)        # "paid", "pending", "failed"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    transaction = relationship("Transaction")



class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone_number = Column(String)
    product_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    orderaddress = Column(String)
    status = Column(String)
    oqim = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    region_id = Column(Integer, ForeignKey("regions.id"))
    payment_id = Column(Integer, ForeignKey("payments.id"))
    payment_type = Column(String)

    user = relationship("User")
    product = relationship("Product")
    payment = relationship("Payment")


class Region(Base):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class District(Base):
    __tablename__ = "districts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    region_id = Column(Integer, ForeignKey("regions.id"))

    region = relationship("Region")


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    price = Column(Integer)
    description = Column(String)
    delivery_time = Column(DateTime)
    seller_id = Column(Integer, ForeignKey("users.id"))  # <-- USER yoki SELLER bilan bog‘lanadi

    seller = relationship("User")




class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username_tg = Column(String)
    product_id = Column(Integer, ForeignKey("products.id"))
    percentage = Column(Integer)
    country_id = Column(Integer)
    region_id = Column(Integer)

    product = relationship("Product")


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)







class UserAddress(Base):
    __tablename__ = "user_addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    region_id = Column(Integer, ForeignKey("regions.id"))
    district_id = Column(Integer, ForeignKey("districts.id"))
    address = Column(String)
    phone_number = Column(String)

    user = relationship("User")
    region = relationship("Region")
    district = relationship("District")
