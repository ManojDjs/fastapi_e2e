"""TestClientFactory for FastAPI Applications
This module provides a factory class to create a TestClient for FastAPI applications,"""

from fastapi.testclient import TestClient
from src.db.connection import get_db
from src.main import app


class TestClientFactory:
    """Factory class to create a TestClient for FastAPI applications."""

    # pylint: disable=too-few-public-methods
    @staticmethod
    def create(db_session):
        """Create a TestClient instance with a dependency
        override for the database session."""
        app.dependency_overrides[get_db] = lambda: db_session
        return TestClient(app)
