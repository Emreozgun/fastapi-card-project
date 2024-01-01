from fastapi.testclient import TestClient

from app.const import AUTH_URL
from app.main import app

client = TestClient(app)


def test_login():
    data = {
        "email": "test@localhost",
        "password": "123456",
    }
    response = client.post("/" + AUTH_URL + "/login", json=data)
    assert response.status_code == 400
