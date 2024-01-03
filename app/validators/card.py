from app.validators.common import CommonValidator
from typing import List
from beartype import beartype


@beartype
class CardValidator(CommonValidator):
    @staticmethod
    def validate_label_length(value: str) -> str:
        if value is not None:
            if len(value) > 255:
                raise ValueError("Label must be shorter than 255 character")
        return value

    @staticmethod
    def validate_statuses(value: str, valid_status: List[str]) -> str:
        if value not in valid_status:
            raise ValueError("Label must be shorter than 255 character")
        return value
