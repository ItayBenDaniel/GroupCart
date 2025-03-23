from fastapi import FastAPI
from backend.database import Base, engine
from backend.routers import products, users

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Shopping List API"}
