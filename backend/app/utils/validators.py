import re


USERNAME_PATTERN = re.compile(
    r"^[A-Za-z]{5,}$"
)

PASSWORD_PATTERN = re.compile(
    r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$%*]).{5,}$"
)


def validate_username(username: str) -> bool:
    return bool(USERNAME_PATTERN.fullmatch(username))


def validate_password(password: str) -> bool:
    return bool(PASSWORD_PATTERN.fullmatch(password))