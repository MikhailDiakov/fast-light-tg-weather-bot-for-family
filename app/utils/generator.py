import random
import string


def generate_random_email() -> str:
    name = "".join(random.choices(string.ascii_lowercase, k=8))
    domain = random.choice(["example.com", "mail.com", "test.org"])
    return f"{name}@{domain}"


def generate_user_agent() -> str:
    app_name = "".join(random.choices(string.ascii_letters, k=6))
    email = generate_random_email()
    return f"{app_name}/1.0 ({email})"
