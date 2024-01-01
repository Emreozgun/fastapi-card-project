from fastapi import APIRouter, Depends
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

router = APIRouter(prefix="/" + AUTH_URL, tags=AUTH_TAGS)


@router.post("/register", response_model=TokenSchema)
def register(
    data: ReqRegisterSchema,
    db_session: Session = Depends(create_session),
) -> TokenSchema:
    return AuthService(db_session).create_user(data)


@router.post("/login", response_model=TokenSchema)
def login(
    data: ReqLoginSchema,
    db_session: Session = Depends(create_session),
) -> TokenSchema:
    return AuthService(db_session).login(data)
