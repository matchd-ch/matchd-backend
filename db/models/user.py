from gettext import gettext as _

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    INTERNAL = 'internal', _('Internal')
    STUDENT = 'student', _('Student')
    COLLEGE_STUDENT = 'college-student', _('College Student')
    JUNIOR = 'junior', _('Junior')
    COMPANY = 'company', _('Company')
    UNIVERSITY = 'university', _('University')
    OTHER = 'other', _('Other')


class User(AbstractUser):
    role = models.CharField(choices=UserRole.choices, max_length=255, blank=False)
    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
