from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.backend.session import create_session
from app.const import (
    CARD_URL, CARD_TAGS,
)
from app.schemas.auth import (
    TokenSchema, UserSchema,
)
from app.schemas.base import ResMessageSchema
from app.schemas.card import ResCreateCardSchema, ReqCreateCardSchema, ReqUpdateCardSchema, ReqDeleteCardSchema

from app.services.card import CardService
from app.util.common import get_current_user

router = APIRouter(prefix="/" + CARD_URL, tags=CARD_TAGS)


@router.post("", response_model=ResCreateCardSchema)
def create(
        data: ReqCreateCardSchema,
        db_session: Session = Depends(create_session),
        user: UserSchema = Depends(get_current_user),
) -> ResCreateCardSchema:
    return CardService(db_session).create_card(data, user)


@router.put("", response_model=ResMessageSchema)
def update(
        data: ReqUpdateCardSchema,
        db_session: Session = Depends(create_session),
        user: UserSchema = Depends(get_current_user),
) -> ResMessageSchema:
    return CardService(db_session).update_card(data, user)


@router.delete("", response_model=ResMessageSchema)
def delete(
        data: ReqDeleteCardSchema,
        db_session: Session = Depends(create_session),
        user: UserSchema = Depends(get_current_user),
) -> ResMessageSchema:
    return CardService(db_session).delete_card(data, user)


@router.get("", response_model=TokenSchema)
def find_all(
        db_session: Session = Depends(create_session),
        user: UserSchema = Depends(get_current_user),
) -> TokenSchema:
    return CardService(db_session).find_all_cards(user)
