import re


class InsufficientFunds(Exception):
    pass

class TripStarted(Exception):
    pass

class NegativeValue(Exception):
    pass

class NotAdmin(Exception):
    pass

class ChoiceError(Exception):
    pass

class ValidationError(Exception):
    pass

class TypeError(Exception):
    pass



username_validate = re.compile(r"^[a-zA-Z]{3,20}$")
password_validate = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).{8,}$")
email_validte = re.compile(r"^[\w.\-]+@([\w\-]+\.)+[\w\-]{2,4}$")


def validate_username(username):
    if not username_validate.match(username):
        raise ValidationError("username must contain letters and it should be more than two characters")
    return username


def validate_password(password):
    if not password_validate.match(password):
        raise ValidationError("your password is not valid")
    return password

def validate_email(email):
    if not email_validte.match(email):
        raise ValidationError("your email is not valid")
    return email