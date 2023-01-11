# TODO: Possibly change once Forward Referencing is implemented in python.
from __future__ import annotations

from django.utils.translation import gettext as _

from db.helper import generic_error_dict
from db.models import Challenge, ProfileType, User


class ChallengeManager():

    def __init__(self, challenge_id: int) -> None:
        self.__errors = {}
        try:
            self.__challenge = Challenge.objects.get(pk=challenge_id)
        except Challenge.DoesNotExist:
            self.__challenge = None
            self.__errors = generic_error_dict(
                'id', _('A challenge with the specified id does not exist'), 'not_found')

    def delete(self, requesting_user: User) -> ChallengeManager:
        errors = {}

        if self.challenge is None:
            return self

        if self.challenge.student is not None:
            if requesting_user.type not in ProfileType.valid_student_types():
                errors.update(
                    generic_error_dict('student', _('You are not a student'), 'invalid_type'))
            else:
                if requesting_user.student.id != self.challenge.student_id:
                    errors.update(
                        generic_error_dict('id', _('You are not the owner of the challenge'),
                                           'invalid_id'))

        if self.challenge.company is not None:
            if requesting_user.type not in ProfileType.valid_company_types():
                errors.update(
                    generic_error_dict('company', _('You are not part of a company'),
                                       'invalid_type'))
            else:
                if requesting_user.company is not None and requesting_user.company.id != self.challenge.company_id:
                    errors.update(
                        generic_error_dict('id', _('The challenge is not part of your company'),
                                           'invalid_id'))

        self.__errors = errors

        if not self.errors:
            self.challenge.delete()

            self.__challenge = None

        return self

    @property
    def challenge(self):
        return self.__challenge

    @property
    def errors(self):
        return self.__errors
