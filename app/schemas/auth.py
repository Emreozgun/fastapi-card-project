from enum import Enum
from pydantic import BaseModel, EmailStr


# Request Schemas
class ReqRegisterSchema(BaseModel):
    email: EmailStr
    password: str


class ReqLoginSchema(BaseModel):
    email: EmailStr
    password: str


# Response Schemas
class VerificationType(str, Enum):
    register = "register"
    login = "login"


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class UserSchema(BaseModel):
    id: str
