from fastapi import FastAPI

from app.api.v1 import admin, auth, student, webhooks
from app.core.database import engine
from app.models import Base

# Create tables in NeonDB on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FYP GitHub Administration API")

# Connect the new routers to the main app
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(student.router, prefix="/api/v1/students", tags=["Students"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["Webhooks"])


@app.get("/")
def read_root():
    return {"status": "online", "message": "API is successfully connected to the database."}