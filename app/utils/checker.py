from app.config import ADMIN_ID, ALLOWED_USERS


def is_family_member(user_id: int) -> bool:
    return user_id in ALLOWED_USERS


def is_admin_member(user_id: int) -> bool:
    return user_id == ADMIN_ID
