"""
Repository module for user-related database operations.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from src.db.tables.users_data_model import User
from src.models.user_schema import (
    UserCreateSchema,
    UserDeleteSchema,
    UserResponseSchema,
)
from src.utils.logger import get_logger

logger = get_logger("user_repository")


def create_user(db: Session, user: UserCreateSchema) -> UserCreateSchema:
    """
    Create a new user in the database.

    Args:
        db (Session): Database session.
        user (UserCreateSchema): User data to be created.

    Returns:
        UserResponseSchema: The created user data.
    """
    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,  # Ensure you hash it elsewhere before calling this function
        first_name=user.first_name,
        last_name=user.last_name,
        age=user.age,
        height=user.height,
        weight=user.weight,
        bio=user.bio,
        created_at=datetime.now(),  # Auto-populated
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    logger.info("User created: %s", db_user.id)
    logger.debug("User details: %s", db_user)

    return UserCreateSchema.model_validate(db_user, from_attributes=True)


def get_users(db: Session) -> list[UserResponseSchema]:
    """
    Retrieve all users from the database.

    Args:
        db (Session): Database session.

    Returns:
        list[UserResponseSchema]: List of all users.
    """
    users = db.query(User).all()
    logger.info("Retrieved %d users from the database", len(users))
    return [
        UserResponseSchema.model_validate(user, from_attributes=True) for user in users
    ]  # Convert to response schema


def get_user_by_id(db: Session, user_id: int) -> UserResponseSchema | None:
    """
    Retrieve a user by ID from the database.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user to retrieve.

    Returns:
        UserResponseSchema | None: The user data if found, otherwise None.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        logger.info("User found: %s", user.username)
        return UserResponseSchema.model_validate(user, from_attributes=True)
    logger.warning("User with ID %d not found", user_id)
    return []


def get_user_by_username_or_email(
    db: Session, username: str, email: str
) -> UserResponseSchema | None:
    """
    Retrieve a user by username or email from the database.

    Args:
        db (Session): Database session.
        username (str): Username of the user to retrieve.
        email (str): Email of the user to retrieve.

    Returns:
        UserResponseSchema | None: The user data if found, otherwise None.
    """
    user = (
        db.query(User)
        .filter((User.username == username) | (User.email == email))
        .first()
    )
    if user:
        logger.info("User found: %s", user.username)
        return UserResponseSchema.model_validate(user, from_attributes=True)
    logger.warning("User with username '%s' or email '%s' not found", username, email)
    return []


def delete_user_by_id(db: Session, user_id: int) -> UserDeleteSchema:
    """
    Delete a user by ID from the database.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user to delete.

    Returns:
        None
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        logger.info("User with ID %d deleted successfully", user_id)
        return UserDeleteSchema.model_validate({"id": user_id}, from_attributes=True)

    logger.warning("User with ID %d not found for deletion", user_id)
    return None
