from enum import Enum
from typing import (
    Final,
    List,
)

TABLE_NAME_USER: Final = "users"
TABLE_NAME_USER_SESSION: Final = "users_sessions"
TABLE_NAME_CARD: Final = "card"
TABLE_NAME_TRANSACTIONS: Final = "transactions"

# Open API parameters
OPEN_API_TITLE: Final = "OPEN_API_TITLE"
OPEN_API_DESCRIPTION: Final = "OPEN_API_DESCRIPTION"

# HealthCheck service constants
HEALTH_CHECK_URL: Final = "health-check"
HEALTH_CHECK_TAGS: Final = []

# Authentication service constants
AUTH_TAGS: Final[List[str]] = ["Authentication"]
AUTH_URL: Final = "auth"
AUTH_TOKEN_TYPE: Final = "bearer"
AUTH_TOKEN_EXPIRE_MINUTES: Final = 60
AUTH_TOKEN_ALGORITHM: Final = "HS256"

# Card service constants
CARD_TAGS: Final[List[str]] = ["Card"]
CARD_URL: Final = "card"

