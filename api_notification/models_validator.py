import re

from django.core.exceptions import ValidationError


def mobile_phone_validator(value: str):
    if re.fullmatch(r'7\d{10}', value) is None:
        raise ValidationError(
            f'phone is not correct 7XXXXXXXXXX {value} '
        )
