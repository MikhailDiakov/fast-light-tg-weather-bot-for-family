import re
from datetime import datetime


def is_valid_time_format(time_str: str) -> bool:
    match = re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", time_str)
    return bool(match)


def is_valid_date_format(date_str: str) -> bool:
    if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", date_str):
        return False
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False
