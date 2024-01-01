from fastapi.testclient import TestClient
from pydantic import BaseSettings

from app.main import app


client = TestClient(app)


class TestConfig(BaseSettings):
    username: str = ""
    password: str = ""

    class Config:
        env_prefix = "CASE_STUDY_TEST_"
        env_nested_delimiter = "__"
        case_sensitive = False


_config = TestConfig()


# @pytest.fixture
# def config():
#     return _config
# @pytest.fixture
# def headers():
#     data = {
#         "username": _config.username,
#         "password": _config.password,
#     }
#     response = client.post("/" + AUTH_URL, data=data)
#     schema = response.json()
#     return {"Authorization": "Bearer " + schema["access_token"]}
