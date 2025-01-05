from fastapi import FastAPI
from backend.routers import items
from backend.database import Base, engine

# Initialize the database tables
Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI()

# Include the items router
app.include_router(items.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Shopping List API"}
