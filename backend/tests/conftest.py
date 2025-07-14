import os
import sys
import pytest
import pytest_asyncio
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.database import init_db
from app.main import app
from fastapi.testclient import TestClient
from httpx import AsyncClient

@pytest.fixture(scope="session")
def client():
    """Create FastAPI TestClient for testing"""
    return TestClient(app)

@pytest_asyncio.fixture
async def async_client():
    """Create async client for testing async endpoints"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(autouse=True)
def setup_database():
    """Initialize database before each test"""
    init_db()
    yield  # Run test
    # Clean up database after test if needed 