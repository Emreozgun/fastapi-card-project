from fastapi import Request
from fastapi.testclient import TestClient
from app.const import AUTH_URL
from app.services.auth import AuthDataManager
from app.schemas.auth import (
    TokenSchema,
)
from app.backend.session import create_session
from app.main import app
from app.util.common import get_current_user

client = TestClient(app)


class DefaultUser:
    def __init__(self):
        # db_session = next(create_session())
        # AuthDataManager(db_session).create_user("default@localhost", "12345678")
        # db_session.commit()
        self._register()

    def _register(self):
        db_session = next(create_session())
        AuthDataManager(db_session).delete_all()
        # print(verification.timestamp)

        data = {
            "email": "default@localhost",
            "password": "12345678",
        }
        response = client.post("/" + AUTH_URL + "/register", json=data)
        assert response.status_code == 200
        token = TokenSchema.validate(response.json())
        user_session = get_current_user(token.access_token, Request({"type": "http", "method": "GET"}))

        self.user_uuid = user_session.id
        self.access_token = token.access_token

    def __del__(self):
        db_session = next(create_session())
        AuthDataManager(db_session).delete_all()

    @staticmethod
    def count():
        db_session = next(create_session())
        return AuthDataManager(db_session).count()
