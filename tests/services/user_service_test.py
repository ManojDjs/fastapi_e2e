"""Test cases for the user service create_user_service function."""
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.user_schema import UserCreateSchema,UserDeleteSchema
from src.services.user_service import create_user_service, delete_user_service,get_all_users_service
from src.db.tables.users_data_model import User


@pytest.fixture
def user_input():
    """Fixture to provide a valid UserCreateSchema instance for testing."""
    return UserCreateSchema(
        username="testuser",
        email="manoj.oddi@gmail.com",
        password="testpassword",
        first_name="Test",
        last_name="User",
        age=30,
        height=170.0,
        weight=70.0,
        bio="This is a test user.",
        is_active=True,
    )


@patch("src.services.user_service.get_user_by_username_or_email")
@patch("src.services.user_service.create_user")
def test_create_user_success(mock_create_user, mock_get_user, user_input):
    """Test the create_user_service function for successful user creation."""
    # Arrange
    mock_get_user.return_value = None
    db = MagicMock(spec=Session)

    # Mock the return value of create_user to be a valid UserCreateSchema instance
    mock_create_user.return_value = user_input

    # Act
    result = create_user_service(db, user_input)

    # Assert
    assert result.username == user_input.username
    assert result.email == user_input.email
    mock_get_user.assert_called_once_with(db, user_input.username, user_input.email)
    mock_create_user.assert_called_once_with(db, user_input)


@patch("src.services.user_service.get_user_by_username_or_email")
def test_create_user_already_exists(mock_get_user, user_input):
    """Test the create_user_service function when user already exists."""
    # Mock the get_user_by_username_or_email to return a user, simulating an existing
    mock_db = MagicMock(spec=Session)
    # Arrange
    mock_get_user.return_value = MagicMock()

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        create_user_service(mock_db, user_input)

    assert exc_info.value.status_code == 400
    assert "already exists" in exc_info.value.detail


@patch("src.services.user_service.get_user_by_username_or_email")
@patch("src.services.user_service.create_user")
def test_create_user_raises_generic_error(mock_create_user, mock_get_user, user_input):
    """Test the create_user_service function when a generic error occurs during user creation."""
    # Arrange
    mock_db = MagicMock(spec=Session)  # Replace missing mock_db fixture with MagicMock
    mock_get_user.return_value = None
    mock_create_user.side_effect = Exception("DB error")

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        create_user_service(mock_db, user_input)

    assert exc_info.value.status_code == 500
    assert "Internal server error" in exc_info.value.detail

@patch("src.services.user_service.delete_user_by_id")
def test_delete_user_service_success(mock_delete_user):
    """Test the delete_user_service function for successful user deletion."""
    # Arrange
    db = MagicMock(spec=Session)
    mock_user = MagicMock(spec=User)
    mock_user.id = 123
    mock_delete_user.return_value = mock_user

    # Act
    result = delete_user_service(db, user_id=123)

    # Assert
    assert isinstance(result, UserDeleteSchema)
    assert result.id == 123
    mock_delete_user.assert_called_once_with(db, 123)


@patch("src.services.user_service.delete_user_by_id")
def test_delete_user_service_user_not_found(mock_delete_user):
    """Test the delete_user_service function when the user is not found."""
    # Arrange
    db = MagicMock(spec=Session)
    mock_delete_user.return_value = None

    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        delete_user_service(db, user_id=999)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "User not found"
    mock_delete_user.assert_called_once_with(db, 999)


@patch("src.services.user_service.delete_user_by_id")
def test_delete_user_service_unexpected_error(mock_delete_user):
    """Test the delete_user_service function when an unexpected error occurs."""
    # Arrange
    db = MagicMock(spec=Session)
    mock_user = MagicMock(spec=User)
    mock_user.id = 456
    mock_delete_user.return_value = mock_user

    # Simulate error during validation (or logger failure etc.)
    with patch("src.services.user_service.UserDeleteSchema.model_validate") as mock_validate:
        mock_validate.side_effect = Exception("Something went wrong")

        with pytest.raises(HTTPException) as excinfo:
            delete_user_service(db, user_id=456)

        assert excinfo.value.status_code == 500
        assert excinfo.value.detail == "Internal server error"
        mock_delete_user.assert_called_once_with(db, 456)

@patch("src.services.user_service.get_users")
def test_get_all_users_service(mock_get_all_users):
    """Test the get_all_users_service function to ensure it retrieves all users correctly."""
    # Arrange
    db = MagicMock(spec=Session)

    mock_user = MagicMock(spec=User)
    mock_user.username = "user1"
    mock_user.email = "manoj.doddi@gmail.com"
    mock_user.first_name = "First"
    mock_user.last_name = "User"
    mock_user.age = 25
    mock_user.height = 175.0
    mock_user.weight = 70.0
    mock_user.bio = "Bio of user1"
    mock_user.is_active = True
    mock_user.password = "hashed_password"

    mock_get_all_users.return_value = [mock_user]

    # Act
    result = get_all_users_service(db)

    # Assert
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].username == "user1"
