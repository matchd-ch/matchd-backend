from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from db.models import Student


class NicknameValidator:

    def validate(self, user, nickname):
        already_exists = Student.objects.filter(nickname=nickname).exclude(user=user).exists()
        if already_exists:
            raise ValidationError(_('Nickname is already taken.'), code='unique')

    def get_help_text(self):
        return _('Nickname must be unique.')
