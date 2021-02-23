from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
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

    @classmethod
    def valid_company_types(cls):
        return [
            cls.COMPANY,
            cls.UNIVERSITY
        ]

    @classmethod
    def content_type_for_user(cls, user):
        if user.type in UserType.valid_student_types():
            return ContentType.objects.get(app_label='db', model='student')
        return None


class UserState(models.TextChoices):
    INCOMPLETE = 'incomplete', _('Incomplete')
    ANONYMOUS = 'anonymous', _('Anonymous')
    PUBLIC = 'public', _('Public')


class User(AbstractUser):
    type = models.CharField(choices=UserType.choices, max_length=255, blank=False)
    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    company = models.ForeignKey('db.Company', on_delete=models.DO_NOTHING, blank=True, null=True,
                                related_name='users')
    state = models.CharField(choices=UserState.choices, max_length=255, blank=False, default=UserState.INCOMPLETE)
    profile_step = models.IntegerField(default=1)

    def get_profile_id(self):
        if self.type in UserType.valid_student_types():
            # noinspection PyUnresolvedReferences
            # student is reverse relation field
            return self.student.id
        elif self.type in UserType.valid_company_types():
            return self.company.id
        return None

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
