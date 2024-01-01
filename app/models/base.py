from typing import (
    Any,
    Dict,
    List,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import DateTime, func
from datetime import datetime


class SQLModel(DeclarativeBase):
    """Base class used for model definitions.

    Provides convenience methods that can be used to convert model
    to the corresponding schema.
    """

    id: Mapped[str] = mapped_column("id", primary_key=True, unique=True)
    date_created: Mapped[datetime] = mapped_column(
        "date_created", DateTime(timezone=False), default=func.now()
    )
    date_modified: Mapped[datetime] = mapped_column(
        "date_modified", DateTime(timezone=False), default=func.now(), onupdate=func.now()
    )

    # date_created: Mapped[DateTime] = mapped_column("date_created", default=func.now())
    # date_modified: Mapped[DateTime] = mapped_column("date_modified", default=func.now(), onupdate=func.now())

    # date_created = Column(DateTime, default=func.now())
    # date_modified = Column(DateTime, default=func.now(), onupdate=func.now())

    @classmethod
    def schema(cls) -> str:
        """Return name of database schema the model refers to."""

        _schema = cls.__mapper__.selectable.schema
        if _schema is None:
            raise ValueError("Cannot identify model schema")
        return _schema

    @classmethod
    def table_name(cls) -> str:
        """Return name of the table the model refers to."""

        return cls.__tablename__

    @classmethod
    def fields(cls) -> List[str]:
        """Return list of model field names."""

        return cls.__mapper__.selectable.c.keys()

    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to a dictionary."""

        _dict: Dict[str, Any] = dict()
        for key in self.__mapper__.c.keys():
            _dict[key] = getattr(self, key)
        return _dict
