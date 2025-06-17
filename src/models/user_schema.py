"""
This module defines Pydantic schemas for user-related operations.
It includes schemas for creating a user and responding with user data.
"""

from datetime import datetime  # Fixed typo in import
from typing import (
    Annotated,  # Add this import at the top if not already present
    Optional,
)

from pydantic import BaseModel, ConfigDict, EmailStr, Field, confloat


class UserCreateSchema(BaseModel):
    """
    Schema for creating a new user.
    Includes validation for fields such as username, email, password, and
    optional attributes like age, height, and weight.
    """

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr  # Use EmailStr to validate email format
    password: str = Field(..., min_length=8, max_length=100)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    age: Optional[Annotated[float, confloat(ge=0)]] = (
        None  # Age must be a non-negative float
    )
    height: Optional[Annotated[float, confloat(ge=0)]] = None  # Height in cm
    weight: Optional[Annotated[float, confloat(ge=0)]] = None  # Weight in kg
    bio: Optional[str] = Field(None, max_length=500)  # User biography or description
    is_active: bool = True  # Default to active user


class UserResponseSchema(UserCreateSchema):
    """
    Schema for responding with user data.
    Includes fields such as id, username, email, and timestamps.
    """

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserDeleteSchema(BaseModel):
    """
    Schema for deleting a user.
    Includes the user ID to be deleted.
    """

    id: int

    model_config = ConfigDict(from_attributes=True)
