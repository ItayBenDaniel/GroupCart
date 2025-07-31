from fastapi import FastAPI
from backend.database import Base, engine
from backend.routers import (
    products,
    recommendations,
    store,
    users,
    cart,
    purchase,
    family,
    store_product,
    cart_change,
    liked_items,
)
from fastapi.staticfiles import StaticFiles
import os

Base.metadata.create_all(bind=engine)


app = FastAPI()
icons_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../frontend/assets/icons")
)
app.mount("/static/icons", StaticFiles(directory=icons_path), name="icons")
app.include_router(products.router)
app.include_router(users.router)
app.include_router(cart.router)
app.include_router(purchase.router)
app.include_router(family.router)
app.include_router(store.router)
app.include_router(store_product.router)
app.include_router(cart_change.router)
app.include_router(recommendations.router)
app.include_router(liked_items.router)


@app.get("/")
def read_root():
    return {"message": "Welcome"}
