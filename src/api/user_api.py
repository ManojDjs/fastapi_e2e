"""
This module defines the API routes for user-related operations.
It includes endpoints for creating, retrieving, and managing users.
"""

from typing import Annotated, List

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.models.user_schema import UserCreateSchema, UserResponseSchema
from src.services.user_service import (
    create_user_service,
    delete_user_service,
    get_all_users_service,
    get_user_by_id_service,
)
from src.utils.logger import get_logger

logger = get_logger("user_api")
user_router = APIRouter(tags=["User API"])


@user_router.post("/users/", response_model=UserCreateSchema, status_code=201)
async def create_user(
    user: Annotated[UserCreateSchema, Form()], db: Session = Depends(get_db)
) -> UserCreateSchema:
    """
    Create a new user in the database.
    """
    create_user_service(db, user)
    logger.info("User created: %s", user.username)
    return user


@user_router.get("/users/", response_model=List[UserResponseSchema], status_code=200)
async def read_users(db: Session = Depends(get_db)) -> List[UserResponseSchema]:
    """
    Retrieve all users from the database.
    """
    logger.info("Retrieving all users from the database")
    users = get_all_users_service(db)
    logger.info("Retrieved %d users from the database", len(users))
    return users


@user_router.get("/users/{user_id}", response_model=UserResponseSchema)
async def read_user(user_id: int, db: Session = Depends(get_db)) -> UserResponseSchema:
    """
    Retrieve a user by ID from the database.
    """
    logger.info("Retrieving user with ID: %d", user_id)

    return get_user_by_id_service(db, user_id)


@user_router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by ID from the database.
    """
    logger.info("Deleting user with ID: %d", user_id)
    delete_user_service(db, user_id)
    logger.info("User with ID %d deleted successfully", user_id)
    return {"detail": "User deleted successfully"}
