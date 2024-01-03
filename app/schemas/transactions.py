from pydantic import BaseModel
from typing import List


# Request Schemas
class ReqCreateTransactionSchema(BaseModel):
    amount: float
    description: str
    card_id: str


# Response Schemas
class ResCardStatsSchema(BaseModel):
    active_card_count: int
    total_amount_spent_on_active_cards: float
    passive_card_count: int
    total_amount_spent_on_passive_cards: float


class ResCreateTransactionSchema(BaseModel):
    t_id: str


class CardTransactionsDetails(BaseModel):
    label: str
    card_no: str
    amount: float
    description: str


class ResFilterCardTransactionsSchema(BaseModel):
    details: List[CardTransactionsDetails]
