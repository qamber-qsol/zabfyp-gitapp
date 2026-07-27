from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.api.v1 import provision # <--- Import the new router

# Create tables in NeonDB on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FYP GitHub Administration API")

# Connect the provision router to the main app
app.include_router(provision.router, prefix="/api/v1/provision", tags=["Provisioning"])

@app.get("/")
def read_root():
    return {"status": "online", "message": "API is successfully connected to the database."}