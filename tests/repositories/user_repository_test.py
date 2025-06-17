"""
Test cases for User Repository functions."""

from src.models.user_schema import UserCreateSchema
from src.repositories.user_repository import create_user, get_users


class TestUserRepository:
    """Test cases for User Repository functions."""

    def test_create_user(self, db_session):
        """Test creating a user with valid data."""
        user_data = {
            "username": "testuser",
            "email": "manoj.doddi@gmail.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "age": 30,
            "height": 170.0,
            "weight": 70.0,
            "bio": "This is a test user.",
            "is_active": True,
        }
        user_data = UserCreateSchema(**user_data)
        user = create_user(db_session, user_data)
        assert user is not None
        assert user.username == user_data.username
        assert user.email == user_data.email

    def test_create_user_with_invalid_data(self, db_session):
        """Test creating a user with invalid data."""
        user_data = {
            "username": "testuser",
            "email": "invalid-email",  # Invalid email format
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "age": 30,
            "height": 170.0,
            "weight": 70.0,
            "bio": "This is a test user.",
            "is_active": True,
        }
        try:
            user_data = UserCreateSchema(**user_data)
            create_user(db_session, user_data)
            assert False, "Expected ValueError for invalid email format"
        except ValueError as e:
            assert "value is not a valid email address" in str(e), (
                f"Unexpected error message: {str(e)}"
            )
        except TypeError as e:  # Replace with a more specific exception if applicable
            assert False, f"Unexpected exception raised: {e}"

    def test_create_user_with_missing_required_fields(self, db_session):
        """Test creating a user with missing required fields."""
        user_data = {
            "email": "manoj@gmail.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "age": 30,
            "height": 170.0,
            "weight": 70.0,
        }
        try:
            user_data = UserCreateSchema(**user_data)
            create_user(db_session, user_data)
            assert False, "Expected ValueError for missing username field"
        except ValueError as e:  # Specific exception for validation errors
            assert "Field required" in str(e) and "username" in str(e), (
                f"Unexpected error message: {str(e)}"
            )
        except TypeError as e:  # Replace broad Exception with TypeError
            assert False, f"Unexpected exception raised: {e}"

    def test_get_all_users(self, db_session):
        """Test retrieving all users."""
        # Create a user to ensure the database has at least one user
        # Assuming create_user is already tested and works correctly
        users = get_users(
            db_session
        )  # Shortened line to comply with 100-character limit
        assert isinstance(users, list)
