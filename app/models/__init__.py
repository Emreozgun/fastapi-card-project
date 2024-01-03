from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable
from app.backend.config import config

from .base import SQLModel
from .card import CardModel
from .transactions import TransactionsModel

from .users import UserModel


def create_tables():
    try:

        engine = create_engine(config.database.dsn)
        SQLModel.metadata.create_all(bind=engine)
        if config.show_tables:
            print("create_tables")
            print(CreateTable(UserModel.__table__))
            print(CreateTable(CardModel.__table__))
            print(CreateTable(TransactionsModel.__table__))
            print("OK")
    except Exception as e:
        print('ERROR: ', e)