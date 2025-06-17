"""
This module defines the SQLAlchemy model for the User table.
"""
# pylint: disable=too-few-public-methods, not-callable

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from src.db.connection import Base


class User(Base):
    """
    SQLAlchemy model for the User table.
    Represents user-related data including personal details and account status.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    age = Column(Integer, nullable=True)
    height = Column(Float, nullable=True)  # Height in cm
    weight = Column(Float, nullable=True)  # Weight in kg
    bio = Column(Text, nullable=True)  # User biography or description
    is_active = Column(
        Boolean, nullable=False, default=True
    )  # Ensure is_active is of type Boolean
    # pylint: disable=not-callable
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # pylint: disable=too-few-public-methods
    def get_full_name(self):
        """
        Returns the full name of the user.
        """
        return (
            f"{self.first_name} {self.last_name}"
            if self.first_name and self.last_name
            else None
        )
