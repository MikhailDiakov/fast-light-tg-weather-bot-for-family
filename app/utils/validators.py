import re


def is_valid_time_format(time_str: str) -> bool:
    match = re.match(r"^(\d{1,2}):(\d{2})$", time_str)
    if not match:
        return False
    hours, minutes = int(match.group(1)), int(match.group(2))
    return 0 <= hours <= 23 and 0 <= minutes <= 59
