from fastapi import FastAPI
from app.database import engine
from app.models import Base

# Create tables in NeonDB on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FYP GitHub Administration API")

@app.get("/")
def read_root():
    return {"status": "online", "message": "API is successfully connected to the database."}