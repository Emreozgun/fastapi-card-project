from pydantic import BaseModel, validator
from typing import Optional, List

from app.validators.card import CardValidator
from beartype import beartype


# Request Schemas
class ReqCreateCardSchema(BaseModel, CardValidator):
    card_no: Optional[str] = None
    label: str

    @validator("card_no", pre=True, check_fields=False)
    def validate_card_no_create(cls, value: str):
        return cls.validate_card_no(value)

    @validator("label", pre=True, check_fields=False)
    def validate_label(cls, value: str):
        return cls.validate_label_length(value)


class ReqUpdateCardSchema(BaseModel, CardValidator):
    status: Optional[str] = None
    card_no: str
    label: Optional[str] = None

    @validator("card_no", pre=True, check_fields=False)
    def validate_card_no_create(cls, value: str):
        return cls.validate_card_no(value)

    @validator("label", pre=True, check_fields=False)
    def validate_label(cls, value: str):
        return cls.validate_label_length(value)

    @validator("status", pre=True, check_fields=False)
    def validate_status_field(cls, value: str):
        return cls.validate_statuses(value, ['passive', 'active'])


class ReqDeleteCardSchema(BaseModel, CardValidator):
    card_no: str

    @validator("card_no", pre=True, check_fields=False)
    def validate_card_no_create(cls, value: str):
        return cls.validate_card_no(value)


# Response Schemas
class ResCreateCardSchema(BaseModel):
    card_no: str


class CardSchema(BaseModel):
    label: str
    card_no: str
    user_id: str
    status: str


class ResFindAllCardSchema(BaseModel):
    cards: List[CardSchema]
