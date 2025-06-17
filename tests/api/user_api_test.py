"""Test cases for User API endpoints.
This module contains test cases for creating and retrieving users using FastAPI's TestClient.
"""

import logging

from ..test_client_factory import TestClientFactory

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestUserAPI:
    """Test cases for User API endpoints."""

    def test_create_user(self, db_session):
        """Test creating a user."""
        client = TestClientFactory.create(
            db_session
        )  # Instantiate TestClient with the FastAPI app
        sample_user = {
            "height": 170,
            "bio": "manoj",
            "last_name": "doddi",
            "username": "manojdoddi",
            "weight": 70,
            "first_name": "manojdoddi",
            "password": "manojdoddi",
            "is_active": True,
            "email": "manojdoddi@gmail.com",
            "age": 0,
        }

        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = client.post("/api/users/", data=sample_user, headers=headers)
        logger.debug("Create User - Status: %s", response.status_code)
        logger.debug("Create User - Body: %s", response.json())
        assert response.status_code == 201

    def test_get_all_users(self, db_session):
        """Test retrieving all users."""
        client = TestClientFactory.create(db_session)

        # Ensure the database has at least one user
        sample_user = {
            "height": 170,
            "bio": "manoj",
            "last_name": "doddi",
            "username": "manojdoddi",
            "weight": 70,
            "first_name": "manojdoddi",
            "password": "manojdoddi",
            "is_active": True,
            "email": "manojdoddi@gmail.com",
            "age": 0,
        }
        client.post(
            "/api/users/",
            data=sample_user,
            headers={
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        # Fetch all users
        response = client.get("/api/users/")
        logger.debug("Get All Users - Status: %s", response.status_code)
        logger.debug("Get All Users - Body: %s", response.json())
        assert response.status_code == 200
        assert len(response.json()) > 0  # Ensure at least one user is returned

    def test_application_health_check(self, db_session):
        """Test application health check endpoint."""
        client = TestClientFactory.create(db_session)

        response = client.get("/")
        logger.debug("Health Check - Status: %s", response.status_code)
        logger.debug("Health Check - Body: %s", response.json())
        assert response.status_code == 200
