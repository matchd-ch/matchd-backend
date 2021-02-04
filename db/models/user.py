from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _


class UserType(models.TextChoices):
    INTERNAL = 'internal', _('Internal')
    STUDENT = 'student', _('Student')
    COLLEGE_STUDENT = 'college-student', _('College Student')
    JUNIOR = 'junior', _('Junior')
    COMPANY = 'company', _('Company')
    UNIVERSITY = 'university', _('University')
    OTHER = 'other', _('Other')

    @classmethod
    def valid_student_types(cls):
        return [
            cls.STUDENT,
            cls.COLLEGE_STUDENT,
            cls.JUNIOR
        ]


class User(AbstractUser):
    type = models.CharField(choices=UserType.choices, max_length=255, blank=False)
    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    company = models.ForeignKey('db.Company', on_delete=models.DO_NOTHING, blank=True, null=True,
                                related_name='users')

    @staticmethod
    def validate_user_type_student(user_type):
        valid_student_types = [
            UserType.STUDENT,
            UserType.COLLEGE_STUDENT,
            UserType.JUNIOR
        ]
        if user_type not in valid_student_types:
            raise ValidationError(
                code='invalid_choice',
                message=_('Select a valid choice.')
            )

    @staticmethod
    def validate_user_type_company(user_type):
        valid_student_types = [
            UserType.COMPANY,
            UserType.UNIVERSITY
        ]
        if user_type not in valid_student_types:
            raise ValidationError(
                code='invalid_choice',
                message=_('Select a valid choice.')
            )
