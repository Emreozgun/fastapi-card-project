import psutil

from fastapi import (
    APIRouter,
    Depends,
)

from app.const import HEALTH_CHECK_URL, HEALTH_CHECK_TAGS
from app.schemas.health_check import HealthCheckSchema


router = APIRouter(prefix="/" + HEALTH_CHECK_URL, tags=HEALTH_CHECK_TAGS)


@router.get("", response_model=HealthCheckSchema)
async def main() -> HealthCheckSchema:
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent

    return { "cpu": cpu, "mem": mem }

