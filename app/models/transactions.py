from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import SQLModel
from app import const


class TransactionsModel(SQLModel):
    __tablename__ = const.TABLE_NAME_TRANSACTIONS

    amount: Mapped[float] = mapped_column("amount")
    description: Mapped[str] = mapped_column("description")
    card_id: Mapped[str] = mapped_column(ForeignKey(f"{const.TABLE_NAME_CARD}.card_no"))


