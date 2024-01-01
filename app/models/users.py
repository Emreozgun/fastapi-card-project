from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import SQLModel
from app import const


class UserModel(SQLModel):
    __tablename__ = const.TABLE_NAME_USER

    email: Mapped[str] = mapped_column("email", unique=True)
    # hashed_password
    password: Mapped[str] = mapped_column("password")
