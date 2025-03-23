from fastapi import FastAPI
from backend.database import Base, engine
from backend.routers import items, users

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI()

# Include the items router
app.include_router(items.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Shopping List API"}
