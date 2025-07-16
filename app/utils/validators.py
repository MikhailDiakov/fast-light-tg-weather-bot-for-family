import re
from datetime import datetime


def is_valid_time_format(time_str: str) -> bool:
    match = re.match(r"^(\d{1,2}):(\d{2})$", time_str)
    if not match:
        return False
    hours, minutes = int(match.group(1)), int(match.group(2))
    return 0 <= hours <= 23 and 0 <= minutes <= 59


def is_valid_date_format(date_str: str) -> bool:
    if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", date_str):
        return False
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False
