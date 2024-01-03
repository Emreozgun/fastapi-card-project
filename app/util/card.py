import random
from typing import List

from app.models import CardModel
from beartype import beartype


@beartype
def generate_card_no(excluded_card_nos:  List[CardModel] = None) -> str:
    excluded_card_nos = excluded_card_nos or set()

    while True:
        first_digit = str(random.randint(1, 9))
        rest_of_digits = ''.join(str(random.randint(0, 9)) for _ in range(15))
        card_no = first_digit + rest_of_digits
        if card_no not in excluded_card_nos:
            return str(card_no)
