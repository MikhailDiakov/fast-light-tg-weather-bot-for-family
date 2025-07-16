import json
from pathlib import Path

DATA_FILE = Path("user_data.json")


def load_data() -> dict:
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_user_data(
    user_id: int,
    lat: float,
    lon: float,
    notify_time: str,
    name: str = "друже",
    notes: str = "",
):
    data = load_data()
    data[str(user_id)] = {
        "lat": lat,
        "lon": lon,
        "time": notify_time,
        "name": name,
        "notes": notes,
    }
    save_data(data)


def get_all_users() -> dict:
    return load_data()


def get_user_data(user_id: int) -> dict | None:
    return load_data().get(str(user_id))


def user_exists(user_id: int) -> bool:
    data = load_data()
    return str(user_id) in data
