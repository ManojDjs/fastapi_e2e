"""This file sets up the test environment for FastAPI applications using pytest.
This module sets up the test environment for FastAPI applications using pytest.
It includes the following:
- Configuration of a SQLite in-memory database for testing purposes.
- Creation of a SQLAlchemy engine and sessionmaker for database interactions.
- A pytest fixture `db_session` that provides a new database session for each test.
Key Components:
- `DATABASE_URL`: Specifies the in-memory SQLite database URL.
- `engine`: SQLAlchemy engine connected to the in-memory SQLite database.
- `TestingSessionLocal`: A sessionmaker instance for creating database sessions.
- `Base.metadata.create_all(bind=engine)`: Ensures all database tables are created before tests run.
- `db_session` fixture: Manages the lifecycle of a database session,
 including setup and teardown for each test.
Usage:
- Import the `db_session` fixture in your test files to interact with the database during tests.
- The fixture ensures isolation between tests by rolling back transactions and
 closing connections after each test.
It configures a SQLite in-memory database for testing purposes and
 provides a fixture for database sessions.
"""

import os

# pylint: disable=wrong-import-position
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.connection import Base

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Provides a new database session for a test."""
    connection = engine.connect()
    transaction = connection.begin()
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
