"""
User Service layer for business logic
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.user_schema import (
    UserCreateSchema,
    UserDeleteSchema,
    UserResponseSchema,
)
from src.repositories.user_repository import (
    create_user,
    delete_user_by_id,
    get_user_by_id,
    get_user_by_username_or_email,
    get_users,
)
from src.utils.logger import get_logger

logger = get_logger("user_service")


def create_user_service(db: Session, user: UserCreateSchema) -> UserCreateSchema:
    """
    Register a new user in the database.

    Args:
        db (Session): Database session.
        user (UserCreateSchema): User data to be registered.

    Returns:
        UserResponseSchema: The registered user data.

    Raises:
        HTTPException: If the user already exists or if there is an error during registration.
    """
    try:
        logger.info("Attempting to register user: %s", user)
        existing_user = get_user_by_username_or_email(db, user.username, user.email)
        if existing_user:
            logger.warning(
                "User with username %s or email %s already exists",
                user.username,
                user.email,
            )
            raise HTTPException(
                status_code=400, detail="Username or email already exists"
            )
        new_user = create_user(db, user)
        logger.info("User registered successfully: %s", new_user.username)
        return UserCreateSchema.model_validate(new_user)
    except HTTPException:
        # Let intentional HTTP exceptions bubble up without modification
        raise
    except Exception as e:
        logger.error("Error registering user: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal server error") from e


def get_all_users_service(db: Session) -> list[UserResponseSchema]:
    """
    Retrieve all users from the database.

    Args:
        db (Session): Database session.

    Returns:
        list[UserResponseSchema]: List of all users.

    Raises:
        HTTPException: If there is an error during retrieval.
    """
    try:
        logger.info("Retrieving all users from the database")
        users = get_users(db)
        logger.info("Retrieved %d users from the database", len(users))
        return [
            UserResponseSchema.model_validate(user) for user in users
        ]  # Convert to response schema
    except Exception as e:
        logger.error("Error retrieving users: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal server error") from e


def get_user_by_id_service(db: Session, user_id: int) -> UserResponseSchema:
    """
    Retrieve a user by ID from the database.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user to retrieve.

    Returns:
        UserResponseSchema: The user data if found, otherwise raises HTTPException.

    Raises:
        HTTPException: If the user is not found or if there is an error during retrieval.
    """
    try:
        logger.info("Retrieving user with ID: %d", user_id)
        user = get_user_by_id(db, user_id)
        if not user:
            logger.warning("User with ID %d not found", user_id)
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponseSchema.model_validate(user)  # Convert to response schema
    except HTTPException:
        # Let intentional HTTP exceptions bubble up without modification
        raise
    except Exception as e:
        logger.error("Error retrieving user by ID %d: %s", user_id, str(e))
        raise HTTPException(status_code=500, detail="Internal server error") from e

    
def delete_user_service(db: Session, user_id: int) -> UserDeleteSchema:
    try:
        logger.info("Attempting to delete user with ID: %d", user_id)
        deleted_user = delete_user_by_id(db, user_id)
        if not deleted_user:
            logger.warning("User with ID %d not found for deletion", user_id)
            raise HTTPException(status_code=404, detail="User not found")
        logger.info("User with ID %d deleted successfully", deleted_user.id)
        return UserDeleteSchema.model_validate({"id": deleted_user.id})
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error deleting user with ID %d: %s", user_id, str(e))
        raise HTTPException(status_code=500, detail="Internal server error") from e
    

