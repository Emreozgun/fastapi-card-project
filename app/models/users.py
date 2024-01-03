from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import SQLModel
from app import const
from sqlalchemy import String


class UserModel(SQLModel):
    __tablename__ = const.TABLE_NAME_USER

    email = mapped_column(String(255), unique=True)
    # hashed_password
    password = mapped_column(String(255))
