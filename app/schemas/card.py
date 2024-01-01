from pydantic import BaseModel, Field
from typing import Optional, Any
from enum import Enum
from .default import to_camel, SchemaCamelCaseConfig


class ReqCreateCardSchema(BaseModel):
    Config = SchemaCamelCaseConfig
    card_no: Optional[str] = None
    label: str


class ReqUpdateCardSchema(BaseModel):
    Config = SchemaCamelCaseConfig
    status: str
    card_no: str
    label: str


class ResCreateCardSchema(BaseModel):
    card_no: str


class ReqDeleteCardSchema(BaseModel):
    card_no: str


