from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Original imports from your architecture
from app.api.v1 import admin, auth, coordinator, dashboard, github, group, student, webhooks
from app.core.database import engine
from app.models import Base, Student, ProjectGroup # Adjust Student/ProjectGroup if your models are named differently

# Configure standard logging for the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP: Database Parity & Connection Check ---
    logger.info("--- Initiating Zero-Touch DB Verification ---")
    
    try:
        # Create tables in NeonDB on startup (moved inside lifespan for error handling)
        Base.metadata.create_all(bind=engine)
        logger.info("SUCCESS: Database schema verified.")
    except Exception as e:
        logger.error(f"DATABASE SCHEMA ERROR: {str(e)}")

    try:
        with Session(engine) as session:
            # Check row counts to verify we aren't connected to an empty database
            student_count = session.query(Student).count()
            team_count = session.query(ProjectGroup).count()
            
            logger.info("SUCCESS: Database connection established to NeonDB.")
            logger.info(f"DATA PARITY: Found {student_count} Students and {team_count} Project Groups.")
            
            if team_count == 0 or student_count == 0:
                logger.warning(
                    "CRITICAL: 0 records found. The app successfully connected to NeonDB, "
                    "but the tables are empty. Data migration or population is required before syncing."
                )
    except Exception as e:
        logger.error(f"DATABASE QUERY ERROR: {str(e)}")
    
    yield # The FastAPI application runs during this yield
    
    # --- SHUTDOWN ---
    logger.info("--- Shutting down backend ---")

# Initialize the main app with the lifespan manager
app = FastAPI(
    title="FYP GitHub Administration API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect the routers to the main app
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(coordinator.router, prefix="/api/v1/coordinator", tags=["Coordinator Dashboard"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Coordinator Dashboard"])
app.include_router(group.router, prefix="/api/v1/groups", tags=["Student Groups"])
app.include_router(github.router, prefix="/api/v1/github", tags=["GitHub Integration"])
app.include_router(student.router, prefix="/api/v1/students", tags=["Students"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["Webhooks"])

@app.get("/")
def read_root():
    return {"status": "online", "message": "API is successfully connected to the database."}