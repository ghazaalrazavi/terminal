import re


class InsufficientFunds(Exception):
    pass


class TripStarted(Exception):
    pass


class NegativeValue(Exception):
    pass


class NotAdmin(Exception):
    pass


class ValidationError(Exception):
    pass


username_validate = re.compile(r"^[a-zA-Z]{3,20}$")
password_validate = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z1-9]){8,}$"
)


def validate_username(username):
    if not username_validate.match(username):
        raise ValidationError("username must contain letters and it should be more than two characters")
    return username


def validate_password(password):
    if not password_validate.match(password):
        raise ValidationError("your password is not valid")
    return password