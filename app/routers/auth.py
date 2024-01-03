from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.backend.session import create_session
from app.const import (
    AUTH_TAGS,
    AUTH_URL,
)
from app.schemas.auth import (
    ReqRegisterSchema,
    ReqLoginSchema,
    TokenSchema,
)

from app.services.auth import AuthService
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/" + AUTH_URL, tags=AUTH_TAGS)


@router.post("/register", response_model=TokenSchema)
def register(
    data: ReqRegisterSchema,
    db_session: Session = Depends(create_session),
) -> TokenSchema:
    return AuthService(db_session).create_user(data)


@router.post("/login", response_model=TokenSchema)
def login(
    data: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(create_session),
) -> TokenSchema:
    data_json = {}
    if data.username:
        data_json["email"] = data.username
        data_json["password"] = data.password
    else:
        data_json = jsonable_encoder(data)
    print(data_json)
    schema = ReqLoginSchema(**data_json)
    return AuthService(db_session).login(schema)
