from pydantic import BaseModel
from enum import Enum
from .default import SchemaCamelCaseConfig


class VerificationType(str, Enum):
    register = "register"
    login = "login"


class ReqRegisterSchema(BaseModel):
    Config = SchemaCamelCaseConfig
    email: str
    password: str


class ReqLoginSchema(BaseModel):
    Config = SchemaCamelCaseConfig
    email: str
    password: str


class TokenSchema(BaseModel):
    Config = SchemaCamelCaseConfig
    access_token: str
    token_type: str


class UserSchema(BaseModel):
    Config = SchemaCamelCaseConfig
    user_uuid: str
