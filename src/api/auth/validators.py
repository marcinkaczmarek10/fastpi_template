import re


def validate_email(email: str) -> bool:
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(pattern=pattern, string=email):
        return True
    return False


def validate_password(password: str) -> bool:
    if not 4 <= len(password) <= 64:
        return False
    pattern = r"(^[a-zA-Z0-9~@#$^*()_+=[\]{}|\\,.?!:<>'\"/;`%-]+$)"
    if re.match(pattern=pattern, string=password):
        return True
    return False
