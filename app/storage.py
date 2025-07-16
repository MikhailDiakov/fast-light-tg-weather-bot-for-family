import json
from pathlib import Path

from cryptography.fernet import Fernet

from app.config import SECRET_KEY

DATA_FILE = Path("user_data.json")
fernet = Fernet(SECRET_KEY)


def load_data() -> dict:
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "rb") as f:
        encrypted = f.read()
    decrypted = fernet.decrypt(encrypted)
    return json.loads(decrypted.decode("utf-8"))


def save_data(data: dict):
    json_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
    encrypted = fernet.encrypt(json_bytes)
    with open(DATA_FILE, "wb") as f:
        f.write(encrypted)


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
