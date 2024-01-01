from pydantic import BaseModel
from .default import SchemaCamelCaseConfig
from typing import List


class ResCardStatsSchema(BaseModel):
    Config = SchemaCamelCaseConfig
    active_card_count: int
    total_amount_spent_on_active_cards: float
    passive_card_count: int
    total_amount_spent_on_passive_cards: float


class ReqCreateTransactionSchema(BaseModel):
    amount: float
    description: str
    card_id: str


class ResCreateTransactionSchema(BaseModel):
    t_id: str


class CardTransactionsDetails(BaseModel):
    label: str
    card_no: str
    amount: float
    description: str


class ResFilterCardTransactionsSchema(BaseModel):
    details: List[CardTransactionsDetails]
