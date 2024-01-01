from pydantic import BaseModel


class HealthCheckSchema(BaseModel):
    cpu: str
    mem: str
