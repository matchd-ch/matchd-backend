# TODO: Possibly change once Forward Referencing is implemented in python.
from __future__ import annotations
from typing import Any

from django.contrib.auth import get_user_model

from db.forms import EmployeeForm, UserForm
from db.helper.forms import validate_company_user_type, validate_form_data
from db.models.employee import Employee
from db.models.user import User


class EmployeeBuilder():

    def __init__(self) -> None:
        self.__errors = {}
        self.__employee = None

    def build(self, user: User, info, form_data: dict[str:Any]) -> EmployeeBuilder:
        validate_company_user_type(user)
        validate_form_data(form_data)

        errors = {}
        company = user.company
        employee_data = None
        user_data = None

        employee_form = EmployeeForm(form_data)
        employee_form.full_clean()
        if employee_form.is_valid():
            employee_data = employee_form.cleaned_data
        else:
            errors.update(employee_form.errors.get_json_data())

        # copy email to username
        form_data['username'] = form_data.get('email')

        user_form = UserForm(form_data)
        user_form.full_clean()
        if user_form.is_valid():
            user_data = user_form.cleaned_data
        else:
            errors.update(user_form.errors.get_json_data())

        self.__errors = errors

        if not errors:
            # create user
            user = get_user_model().objects.create(first_name=user_data.get('first_name'),
                                                   last_name=user_data.get('last_name'),
                                                   email=user_data.get('email'),
                                                   username=user_data.get('username'),
                                                   company=company,
                                                   type=user.type)

            # create employee
            self.__employee = Employee.objects.create(role=employee_data.get('role'), user=user)

        user.status.send_password_reset_email(info)

        return self

    @property
    def employee(self):
        return self.__employee

    @property
    def errors(self):
        return self.__errors
