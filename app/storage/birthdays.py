import json
from datetime import datetime
from pathlib import Path

BIRTHDAY_FILE = Path("birthdays.json")


def load_birthdays() -> list[dict]:
    if BIRTHDAY_FILE.exists():
        return json.loads(BIRTHDAY_FILE.read_text(encoding="utf-8"))
    return []


def save_birthdays(data: list[dict]):
    def sort_key(b):
        dt = datetime.strptime(b["date"], "%d.%m.%Y")
        return (dt.month, dt.day)

    data_sorted = sorted(data, key=sort_key)

    BIRTHDAY_FILE.write_text(
        json.dumps(data_sorted, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def add_birthday(name: str, date: str) -> bool:
    data = load_birthdays()
    if any(b["name"].lower() == name.lower() for b in data):
        return False
    data.append({"name": name, "date": date})
    save_birthdays(data)
    return True


def get_all_birthdays() -> list[dict]:
    return load_birthdays()


def delete_birthday(name: str) -> bool:
    data = load_birthdays()
    initial_len = len(data)
    data = [b for b in data if b["name"].lower() != name.lower()]
    if len(data) == initial_len:
        return False
    save_birthdays(data)
    return True
