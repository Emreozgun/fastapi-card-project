from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.backend.session import create_session
from app.const import (
    TRANSACTION_URL, TRANSACTION_TAGS,
)
from app.schemas.auth import (
    UserSchema,
)
from app.schemas.transactions import ResCreateTransactionSchema, ReqCreateTransactionSchema, ResCardStatsSchema, \
    ResFilterCardTransactionsSchema
from typing import Union

from app.services.transactions import TransactionService
from app.util.common import get_current_user

router = APIRouter(prefix="/" + TRANSACTION_URL, tags=TRANSACTION_TAGS)


@router.post("", response_model=ResCreateTransactionSchema)
def create(
        data: ReqCreateTransactionSchema,
        db_session: Session = Depends(create_session),
        user: UserSchema = Depends(get_current_user),
) -> ResCreateTransactionSchema:
    return TransactionService(db_session).create(data, user)


@router.get("/stats", response_model=ResCardStatsSchema)
def stats(
        db_session: Session = Depends(create_session),
        user: UserSchema = Depends(get_current_user),
) -> ResCardStatsSchema:
    return TransactionService(db_session).get_card_stats(user)


@router.get("/details", response_model=ResFilterCardTransactionsSchema)
def details(
        text: Union[str, None] = Query(default=None, max_length=255),
        db_session: Session = Depends(create_session),
        user: UserSchema = Depends(get_current_user),
) -> ResFilterCardTransactionsSchema:
    return TransactionService(db_session).filtered_card_transactions(text, user)
