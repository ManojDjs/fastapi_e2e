"""
FastAPI application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.user_api import user_router
from src.config.config import config
from src.db.connection import Base, engine
from src.utils.logger import get_logger

# Ensure the DATABASE_URL environment variable is set
# Base.metadata.delate_all(bind=engine)  # Drop all tables
# Base.metadata.drop_all(bind=engine)  # Drop all tables
Base.metadata.create_all(bind=engine)
app = FastAPI()
logger = get_logger("orchestrator")
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow Vue app (running on localhost:5173)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)
# inclde Environmental Severity Model and Mission Model Route

app.include_router(user_router, prefix="/api", tags=["User API"])


@app.get("/")
async def read_root():
    """
    Root endpoint to check if the API is running.
    Returns:
        dict: A dictionary with a message indicating the API is running.
    """
    logger.info("Root endpoint was accessed")
    return {
        "message": "running",
        "Hello": "World",
        "database_url": config.get_database_url(),
        "log_level": config.get_log_level(),
        "celery_broker_url": config.get_celery_broker_url(),
        "redis_connection_string": config.get_celery_broker_url(),
        "esm_api": config.get_esm_api_url(),
        "spe_api": config.get_spe_api_url(),
        "thor_api": config.get_thor_api_url(),
    }
