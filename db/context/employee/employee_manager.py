# TODO: Possibly change once Forward Referencing is implemented in python.
from __future__ import annotations

from django.utils.translation import gettext as _

from db.helper import generic_error_dict
from db.models import Employee, ProfileType, User


class EmployeeManager():

    def __init__(self, employee_id: int) -> None:
        self.__errors = {}
        try:
            self.__employee = Employee.objects.get(pk=employee_id)
        except Employee.DoesNotExist:
            self.__employee = None
            self.__errors = generic_error_dict(
                'id', _('An employee with the specified id does not exist'),
                'employee_does_not_exist')

    def delete(self, requesting_user: User) -> EmployeeManager:
        errors = {}

        if self.employee is None:
            return self

        if requesting_user.type not in ProfileType.valid_company_types():
            errors = errors.update(
                generic_error_dict('type', _('You are not part of a company'), 'invalid_type'))

        if requesting_user.id == self.employee.user.id:
            errors.update(
                generic_error_dict('id', _('An employee cannot delete itself'), 'invalid_id'))

        if requesting_user.company is not None and requesting_user.company.id != self.employee.user.company.id:
            errors.update(
                generic_error_dict('id',
                                   _('The employee to delete is not part of the same company'),
                                   'invalid_id'))

        self.__errors = errors

        if not self.errors:
            self.employee.user.delete()

            self.__employee = None

        return self

    @property
    def employee(self):
        return self.__employee

    @property
    def errors(self):
        return self.__errors
