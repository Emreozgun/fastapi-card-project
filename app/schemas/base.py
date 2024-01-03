from pydantic import BaseModel


class ResMessageSchema(BaseModel):
    message: str
    is_success: bool

