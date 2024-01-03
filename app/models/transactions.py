from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import SQLModel
from app import const
from sqlalchemy import Numeric


class TransactionsModel(SQLModel):
    __tablename__ = const.TABLE_NAME_TRANSACTIONS

    # TODO : check it precision=10, scale=2
    amount: Mapped[float] = mapped_column("amount", type_=Numeric(precision=10, scale=2))
    description: Mapped[str] = mapped_column("description")
    card_id: Mapped[str] = mapped_column(ForeignKey(f"{const.TABLE_NAME_CARD}.card_no"))


