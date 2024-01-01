from pydantic import BaseModel
from .default import SchemaCamelCaseConfig


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
