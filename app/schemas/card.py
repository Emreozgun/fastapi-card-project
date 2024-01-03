from pydantic import BaseModel, Field, validator, ValidationError
from typing import Optional, Any, List


class ReqCreateCardSchema(BaseModel):
    card_no: Optional[str] = None
    label: str

    @validator("card_no", pre=True, check_fields=False)
    def validate_card_no(cls, value):
        if value is not None:
            digits_only = ''.join(filter(str.isdigit, value))
            if len(digits_only) != 16:
                raise ValueError("Card number must be a 16-digit string")
        return value


class ReqUpdateCardSchema(BaseModel):
    status: Optional[str] = None
    card_no: str
    label: Optional[str] = None


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
