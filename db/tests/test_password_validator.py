import pytest
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_min_length(password_validator):
    with pytest.raises(ValidationError, match='Das Password muss mindestens 8 Zeichen lang sein.'):
        password_validator.validate('123')


@pytest.mark.django_db
def test_digit(password_validator):
    with pytest.raises(ValidationError, match='Das Passwort muss mindestens 1 Zahl beinhalten.'):
        password_validator.validate('abcdefgh')


@pytest.mark.django_db
def test_letter(password_validator):
    with pytest.raises(ValidationError,
                       match='Das Passwort muss mindestens 1 Buchstaben beinhalten.'):
        password_validator.validate('12345678')


@pytest.mark.django_db
def test_specialchars(password_validator):
    with pytest.raises(ValidationError,
                       match='Das Password muss mindestens 1 Sonderzeichen beinhalten.'):
        password_validator.validate('abcd1234')


@pytest.mark.django_db
def test_specialchars_dot(password_validator):
    password_validator.validate('abcd1234.')


@pytest.mark.django_db
def test_specialchars_comma(password_validator):
    password_validator.validate('abcd1234,')


@pytest.mark.django_db
def test_specialchars_dash(password_validator):
    password_validator.validate('abcd1234-')


@pytest.mark.django_db
def test_specialchars_underscore(password_validator):
    password_validator.validate('abcd1234_')
