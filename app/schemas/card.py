from pydantic import BaseModel, Field
from typing import Optional, Any, List
from enum import Enum
from .default import to_camel, SchemaCamelCaseConfig
from ..models.card import CardModel


class ReqCreateCardSchema(BaseModel):
    Config = SchemaCamelCaseConfig
    card_no: Optional[str] = None
    label: str


class ReqUpdateCardSchema(BaseModel):
    Config = SchemaCamelCaseConfig
    status: str
    card_no: str
    label: str


class ResCreateCardSchema(BaseModel):
    card_no: str


class ReqDeleteCardSchema(BaseModel):
    card_no: str


class CardSchema(BaseModel):
    label: str
    card_no: str
    user_id: str
    status: str


class ResFindAllCardSchema(BaseModel):
    cards: List[CardSchema]
