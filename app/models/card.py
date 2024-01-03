from sqlalchemy import ForeignKey, UniqueConstraint, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import SQLModel
from app import const


class CardModel(SQLModel):
    __tablename__ = const.TABLE_NAME_CARD

    label = mapped_column(String(255))
    card_no = mapped_column(String(17))
    user_id = mapped_column(String(255))
    status = mapped_column(String(255), default='passive')

    __table_args__ = (
        UniqueConstraint('card_no', 'user_id', name='uq_card_no_user_id'),
        CheckConstraint('LENGTH(label) < 255', name='label_length_check'),
        CheckConstraint('LENGTH(card_no) = 16', name='card_no_length_check'),
    )

