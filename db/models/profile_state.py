from django.db import models
from django.utils.translation import gettext as _


class ProfileState(models.TextChoices):
    ANONYMOUS = 'anonymous', _('Anonymous')
    PUBLIC = 'public', _('Public')
