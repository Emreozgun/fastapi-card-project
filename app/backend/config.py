from pydantic import (
    BaseModel,
    BaseSettings,
)
from dotenv import load_dotenv
import os

load_dotenv()


class DatabaseConfig(BaseModel):
    dsn: str = os.environ.get('MYSQL_HOST')
    # For local development
    # dsn: str = "sqlite:///./test.db"

    @property
    def dbname(self):
        if self.dsn.startswith("sqlite:///"):
            return "main"
        return self.dsn.split("/")[-1]


class Config(BaseSettings):
    database: DatabaseConfig = DatabaseConfig()
    token_key: str = os.environ.get('JWT_TOKEN_KEY')
    show_tables: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "TEMPLATE_"
        env_nested_delimiter = "__"
        case_sensitive = False


config = Config()
