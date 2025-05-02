from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str
    phone_number: str
    address: str
    hashed_password:str

class UserCreate(BaseModel):
    username: str
    phone_number: str
    address: str
    password: str

class UserOut(UserBase):
    id: int
    username: str
    phone_number: str
    address: str
    hashed_password: str
    role: str  # ✅ QO‘SHILADI

    class Config:
        from_attributes = True




class ProfileBase(BaseModel):
    name: str
    product_id: int
    lastname: str
    region_id: int
    district_id: int
    image: str
    user_id: int
    
class ProfileCreate(ProfileBase):
    pass

class ProfileOut(ProfileBase):
    id: int
    name: str
    product_id: int
    lastname: str
    region_id: int
    district_id: int
    image: str
    user_id: int

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    image: str
    name: str
    type: str

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int
    image: str
    name: str
    type: str

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    quantity: int
    description: str
    video_id: int
    price: int
    category_id: int
    attribute_id: int

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    name: str
    quantity: int
    description: str
    video_id: int
    price: int
    category_id: int
    attribute_id: int

    class Config:
        from_attributes = True






class TransactionBase(BaseModel):
    profile_id: int
    product_id: int
    quantity: int
    total_price: int
    status: str

class TransactionCreate(TransactionBase):
    pass

class TransactionOut(TransactionBase):
    id: int
    profile_id: int
    product_id: int
    quantity: int
    total_price: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class PaymentBase(BaseModel):
    transaction_id: int
    amount: int
    payment_type: str
    status: str

class PaymentCreate(PaymentBase):
    pass

class PaymentOut(PaymentBase):
    id: int
    created_at: datetime
    transaction_id: int
    amount: int
    payment_type: str
    status: str 
    class Config:
        from_attributes = True






class OrderBase(BaseModel):
    name: str
    phone_number: str
    product_id: int
    orderaddress: str
    status: str
    oqim: str
    region_id: int
    payment_id: int
    payment_type: str

class OrderCreate(OrderBase):
    pass

class OrderOut(OrderBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True



class RegionBase(BaseModel):
    name: str

class RegionCreate(RegionBase): pass

class RegionOut(RegionBase):
    id: int
    class Config:
        from_attributes = True


class DistrictBase(BaseModel):
    name: str
    region_id: int

class DistrictCreate(DistrictBase): pass

class DistrictOut(DistrictBase):
    id: int
    region: RegionOut
    class Config:
        from_attributes = True


from datetime import datetime

class DeliveryBase(BaseModel):
    type: str
    price: int
    description: str
    delivery_time: datetime

class DeliveryCreate(DeliveryBase):
    pass

class DeliveryOut(DeliveryBase):
    id: int
    product_id: int
    class Config:
        from_attributes = True


class SellerBase(BaseModel):
    name: str
    username_tg: str
    product_id: int
    percentage: int
    country_id: int
    region_id: int

class SellerCreate(SellerBase): pass

class SellerOut(SellerBase):
    id: int
    class Config:
        from_attributes = True

class CountryBase(BaseModel):
    name: str

class CountryCreate(CountryBase):
    pass

class CountryOut(CountryBase):
    id: int

    class Config:
        from_attributes = True


class UserAddressBase(BaseModel):
    region_id: int
    district_id: int
    address: str
    phone_number: str

class UserAddressCreate(UserAddressBase):
    pass

class UserAddressOut(UserAddressBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True


class StreamCreate(BaseModel):
    product_id: int
    title: str

class StreamOut(StreamCreate):
    id: int
    seller_id: int
    created_at: datetime

    class Config:
        from_attributes = True