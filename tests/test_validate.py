import pytest
from validate import validate_username, validate_password, validate_email, ValidationError

def test_validate_username_success():
    assert validate_username("Alice") == "Alice"
    assert validate_username("BobSmith") == "BobSmith"

def test_validate_username_failure():
    with pytest.raises(ValidationError):
        validate_username("Al")
    with pytest.raises(ValidationError):
        validate_username("Alice123")
    with pytest.raises(ValidationError):
        validate_username("Alice!")

def test_validate_password_success():
    assert validate_password("Aa123456!") == "Aa123456!"
    assert validate_password("Password1@") == "Password1@"

def test_validate_password_failure():
    with pytest.raises(ValidationError):
        validate_password("password")
    with pytest.raises(ValidationError):
        validate_password("PASSWORD1")
    with pytest.raises(ValidationError):
        validate_password("Passw1")

def test_validate_email_success():
    assert validate_email("test@example.com") == "test@example.com"
    assert validate_email("user.name@domain.co") == "user.name@domain.co"

def test_validate_email_failure():
    with pytest.raises(ValidationError):
        validate_email("invalid-email")
    with pytest.raises(ValidationError):
        validate_email("user@com")
    with pytest.raises(ValidationError):
        validate_email("user@domain,com")
