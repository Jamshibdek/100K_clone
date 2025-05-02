from fastapi import FastAPI
from models.models import Base
from database import engine
import routers.users as user_router
import routers.profiles as profile_router
import routers.categories as category_router
import routers.products as product_router

import routers.transactions as transaction_router
import routers.payments as payment_router
from auth import router as auth_router
from routers import orders as orders_router
from routers import regions as region_router
from routers import sellers as seller_router
from routers import countries as country_router
from routers import addresses as address_router
from routers import admin as admin_router
from routers import streams

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router.router)
app.include_router(profile_router.router)
app.include_router(category_router.router)
app.include_router(product_router.router)
app.include_router(transaction_router.router)
app.include_router(payment_router.router)
app.include_router(auth_router)
app.include_router(orders_router.router)
app.include_router(region_router.router)
app.include_router(seller_router.router)
app.include_router(country_router.router)
app.include_router(address_router.router)
app.include_router(streams.router)
app.include_router(admin_router.router)