from unittest import TestCase

from django.core.exceptions import ValidationError

from db.validators import PasswordValidator


class PasswordValidatorTest(TestCase):

    def setUp(self) -> None:
        self.validator = PasswordValidator()

    def test_min_length(self):
        with self.assertRaises(ValidationError, msg='Das Password muss mindestens 8 Zeichen lang sein.'):
            self.validator.validate('123')

    def test_digit(self):
        with self.assertRaises(ValidationError, msg='Das Passwort muss mindestens 1 Zahl beinhalten.'):
            self.validator.validate('abcdefgh')

    def test_letter(self):
        with self.assertRaises(ValidationError, msg='Das Passwort muss mindestens 1 Buchstaben beinhalten.'):
            self.validator.validate('12345678')

    def test_specialchars(self):
        with self.assertRaises(ValidationError, msg='Das Password muss mindestens 1 Sonderzeichen beinhalten.'):
            self.validator.validate('abcd1234')
