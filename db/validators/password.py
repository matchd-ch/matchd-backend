from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class PasswordValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _('Das Password muss mindestens %(min_length)d Zeichen lang sein.'),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Das Passwort muss mindestens 1 Zahl beinhalten.'), code='no_digit')

        # check for letter
        if not any(char.isalpha() for char in password):
            raise ValidationError(_('Das Passwort muss mindestens 1 Buchstaben beinhalten.'), code='no_letter')

        # check for special character
        if not any(not char.isalnum() for char in password):
            raise ValidationError(_('Das Password muss mindestens 1 Sonderzeichen beinhalten.'),
                                  code='no_specialchars')

    def get_help_text(self):
        return _(
            f'Your password must contain at least {self.min_length} characters.'
        )
