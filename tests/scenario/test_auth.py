from fastapi.testclient import TestClient

from app.const import AUTH_URL, AUTH_TOKEN_TYPE
from app.main import app
from app.schemas.auth import TokenSchema

client = TestClient(app)


def test_create_and_login():
    data = {
        "email": "test@localhost",
        "password": "123456",
    }
    response = client.post("/" + AUTH_URL + "/register", json=data)
    assert response.status_code == 200
    token1 = TokenSchema.validate(response.json())
    assert token1.token_type == AUTH_TOKEN_TYPE
    assert len(token1.access_token) > 0

    response = client.get(
        "/" + AUTH_URL + "/check", headers={"Authorization": "Bearer " + "asd"}
    )
    assert response.status_code == 401

    response = client.get(
        "/" + AUTH_URL + "/check",
        headers={"Authorization": "Bearer " + token1.access_token},
    )
    assert response.status_code == 200


# def test_incorrect_password(config):
#     data = {
#         "username": config.username,
#         "password": "fake_password",
#     }
#     response = client.post("/" + AUTH_URL, data=data)
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
