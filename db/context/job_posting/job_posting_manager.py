# TODO: Possibly change once Forward Referencing is implemented in python.
from __future__ import annotations

from django.utils.translation import gettext as _

from db.helper import generic_error_dict
from db.models import JobPosting, ProfileType, User


class JobPostingManager():

    def __init__(self, job_posting_id: int) -> None:
        self.__errors = {}
        try:
            self.__job_posting = JobPosting.objects.get(pk=job_posting_id)
        except JobPosting.DoesNotExist:
            self.__job_posting = None
            self.__errors = generic_error_dict(
                'id', _('An job posting with the specified id does not exist'), 'not_found')

    def delete(self, requesting_user: User) -> JobPostingManager:
        errors = {}

        if self.job_posting is None:
            return self

        if requesting_user.type not in ProfileType.valid_company_types():
            errors.update(
                generic_error_dict('company', _('You are not part of a company'), 'invalid_type'))

        if requesting_user.company is not None and requesting_user.company.id != self.job_posting.company_id:
            errors.update(
                generic_error_dict('id', _('The job posting is not part of the same company'),
                                   'invalid_id'))

        self.__errors = errors

        if not self.errors:
            self.job_posting.delete()

            self.__job_posting = None

        return self

    @property
    def job_posting(self):
        return self.__job_posting

    @property
    def errors(self):
        return self.__errors
