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
