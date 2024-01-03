class CommonValidator:
    @staticmethod
    def validate_card_no(value):
        if value is not None:
            digits_only = ''.join(filter(str.isdigit, value))
            if len(digits_only) != 16:
                raise ValueError("Card number must be a 16-digit string")
        return value
