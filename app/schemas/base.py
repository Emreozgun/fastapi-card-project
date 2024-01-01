from pydantic import BaseModel
from .default import SchemaCamelCaseConfig


class ResMessageSchema(BaseModel):
    Config = SchemaCamelCaseConfig
    message: str
    is_success: bool

