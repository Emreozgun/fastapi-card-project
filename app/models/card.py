from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import SQLModel
from app import const


class CardModel(SQLModel):
    __tablename__ = const.TABLE_NAME_CARD

    label: Mapped[str] = mapped_column("label", unique=True) # TODO:  max_len = 255
    card_no: Mapped[str] = mapped_column("card_no") # TODO: max_len = 16
    user_id: Mapped[str] = mapped_column(ForeignKey(f"{const.TABLE_NAME_USER}.id"))
    status: Mapped[str] = mapped_column("status", default='passive')  # TODO enum (active, passive, deleted)

    __table_args__ = (
        UniqueConstraint('card_no', 'user_id', name='uq_card_no_user_id'),
    )

