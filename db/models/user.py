from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _

from .profile_state import ProfileState
from .profile_type import ProfileType


class User(AbstractUser):
    type = models.CharField(choices=ProfileType.choices, max_length=255, blank=False)
    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    company = models.ForeignKey('db.Company', on_delete=models.DO_NOTHING, blank=True, null=True,
                                related_name='users')

    def get_profile_content_type(self):
        if self.type in ProfileType.valid_student_types():
            return ContentType.objects.get(app_label='db', model='student')
        if self.type in ProfileType.valid_company_types():
            return ContentType.objects.get(app_label='db', model='company')
        return None

    def get_profile_id(self):
        if self.type in ProfileType.valid_student_types():
            # noinspection PyUnresolvedReferences
            # student is a reverse relation field
            return self.student.id
        if self.type in ProfileType.valid_company_types():
            return self.company.id
        return None

    def get_profile_step(self):
        if self.type in ProfileType.valid_student_types():
            # noinspection PyUnresolvedReferences
            # student is a reverse relation field
            return self.student.profile_step
        if self.type in ProfileType.valid_company_types():
            return self.company.profile_step
        return 0

    def get_profile_state(self):
        if self.type in ProfileType.valid_student_types():
            # noinspection PyUnresolvedReferences
            # student is a reverse relation field
            return self.student.state
        if self.type in ProfileType.valid_company_types():
            return self.company.state
        return ProfileState.INCOMPLETE
