# TODO: Possibly change once Forward Referencing is implemented in python.
from __future__ import annotations

from django.utils.translation import gettext as _

from db.helper import generic_error_dict
from db.models import User, ProfileType


class UserManager():

    def __init__(self, user_id: int) -> None:
        self.__errors = {}
        try:
            self.__user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            self.__user = None
            self.__errors = generic_error_dict('id',
                                               _('A user with the specified id does not exist'),
                                               'not_found')

    def delete(self) -> UserManager:
        errors = {}

        if self.user is None:
            return self

        self.__errors = errors

        if not self.errors:
            if self.user.type in ProfileType.valid_company_types():
                if len(self.user.company.get_employees()) == 1:
                    self.user.company.delete()

            self.user.delete()

            self.__user = None

        return self

    @property
    def user(self):
        return self.__user

    @property
    def errors(self):
        return self.__errors
