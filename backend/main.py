from fastapi import FastAPI
from backend.database import Base, engine
from backend.routers import (
    products,
    store,
    users,
    cart,
    purchase,
    family,
    store_product,
    cart_change,
)
from fastapi.staticfiles import StaticFiles
import os

# Initialize database tables
Base.metadata.create_all(bind=engine)


# Create the FastAPI app
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


@app.get("/")
def read_root():
    return {"message": "Welcome to the Shopping List API"}
