from fastapi.testclient import TestClient
from pytunes.main import app, get_current_username

app.dependency_overrides[get_current_username] = lambda: "current_username"
client = TestClient(app)
