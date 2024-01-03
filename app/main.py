from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.const import (
    OPEN_API_DESCRIPTION,
    OPEN_API_TITLE,
)
from app.routers import auth, health_check, card, transaction
from app.version import __version__
from app.models import create_tables


def update_operation_ids(app: FastAPI, prefix: str) -> FastAPI:
    for route in app.routes:
        if isinstance(route, APIRoute):
            # print(f"{prefix}_{route.name}")
            route.operation_id = f"{prefix}_{route.name}"
    return app


app = FastAPI(
    title=OPEN_API_TITLE,
    description=OPEN_API_DESCRIPTION,
    version=__version__,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.include_router(update_operation_ids(auth.router, "auth"))
app.include_router(update_operation_ids(health_check.router, "health"))
app.include_router(update_operation_ids(card.router, "card"))
app.include_router(update_operation_ids(transaction.router, "transaction"))

# TODO development only
if True:
    create_tables()


@app.get("/")
def root() -> str:
    return "OK"
