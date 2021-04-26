import pytest
from django.core.exceptions import ValidationError


def test_min_length(password_validator):
    with pytest.raises(ValidationError, match='Das Password muss mindestens 8 Zeichen lang sein.'):
        password_validator.validate('123')


def test_digit(password_validator):
    with pytest.raises(ValidationError, match='Das Passwort muss mindestens 1 Zahl beinhalten.'):
        password_validator.validate('abcdefgh')


def test_letter(password_validator):
    with pytest.raises(ValidationError, match='Das Passwort muss mindestens 1 Buchstaben beinhalten.'):
        password_validator.validate('12345678')


def test_specialchars(password_validator):
    with pytest.raises(ValidationError, match='Das Password muss mindestens 1 Sonderzeichen beinhalten.'):
        password_validator.validate('abcd1234')
