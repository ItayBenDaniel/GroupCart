from fastapi import FastAPI
from .database import Base, engine
from .routers import items

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI()

# Include the items router
app.include_router(items.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Shopping List API"}
