from django.db import models
from django.utils.translation import gettext as _


class ProfileState(models.TextChoices):
    INCOMPLETE = 'incomplete', _('Incomplete')
    ANONYMOUS = 'anonymous', _('Anonymous')
    PUBLIC = 'public', _('Public')
