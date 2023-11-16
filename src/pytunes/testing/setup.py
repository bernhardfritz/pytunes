from unittest.mock import Mock

from fastapi.testclient import TestClient

from pytunes.dependencies import get_db
from pytunes.main import app, get_current_username

mock_current_username = "current_username"
app.dependency_overrides[get_current_username] = lambda: mock_current_username

mock_db = Mock()
app.dependency_overrides[get_db] = lambda: mock_db

client = TestClient(app)
