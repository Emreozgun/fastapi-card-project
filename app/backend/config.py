from pydantic import (
    BaseModel,
    BaseSettings,
)


class DatabaseConfig(BaseModel):
    dsn: str = "sqlite:////tmp/db.sqlite3"

    @property
    def dbname(self):
        if self.dsn.startswith("sqlite:///"):
            return "main"
        return self.dsn.split("/")[-1]


class Config(BaseSettings):
    database: DatabaseConfig = DatabaseConfig()
    token_key: str = ""
    show_tables: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "TEMPLATE_"
        env_nested_delimiter = "__"
        case_sensitive = False


config = Config()
