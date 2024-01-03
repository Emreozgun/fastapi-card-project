from pydantic import (
    BaseModel,
    BaseSettings,
)


class DatabaseConfig(BaseModel):
    dsn: str = "sqlite:///./test.db"

    @property
    def dbname(self):
        if self.dsn.startswith("sqlite:///"):
            return "main"
        return self.dsn.split("/")[-1]


class Config(BaseSettings):
    database: DatabaseConfig = DatabaseConfig()
    token_key: str = ""
    show_tables: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "TEMPLATE_"
        env_nested_delimiter = "__"
        case_sensitive = False


config = Config()
