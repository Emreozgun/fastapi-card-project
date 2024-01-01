from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable
from app.backend.config import config

from .base import SQLModel
from .card import CardModel
from .transactions import TransactionsModel

from .users import UserModel


def create_tables():
    engine = create_engine(config.database.dsn)
    SQLModel.metadata.create_all(bind=engine)
    print('create_table: ', config.show_tables)
    if config.show_tables:
        print("create_tables")
        print(CreateTable(UserModel.__table__))
        print(CreateTable(CardModel.__table__))
        print(CreateTable(TransactionsModel.__table__))
        print("OK")
