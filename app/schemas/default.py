from pydantic import BaseModel, Field


class DefaultUuidSchema(BaseModel):
    id: str


def to_camel(x: str) -> str:
    y = "".join(x.capitalize() for x in x.lower().split("_"))
    return y[0].lower() + y[1:]


class SchemaCamelCaseConfig:
    alias_generator = to_camel
    allow_population_by_field_name = True
