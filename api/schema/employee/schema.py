import graphene
from django.contrib.auth import get_user_model
from graphql_auth.bases import Output
from django.utils.translation import gettext as _
from graphql_jwt.decorators import login_required

from api.schema.user.schema import Employee
from db.forms import EmployeeForm, UserForm
from db.helper.forms import validate_company_user_type, validate_form_data
from db.models import Employee as EmployeeModel, UserType


class AddEmployeeInput(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    role = graphene.String(required=True)
    email = graphene.String(required=True)


class AddEmployee(Output, graphene.Mutation):

    employee = graphene.Field(Employee)

    class Arguments:
        add_employee = AddEmployeeInput(description=_('Employee input is required'), required=True)

    class Meta:
        description = _('Adds a new emplyoee to a comany')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('add_employee', None)

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

        if errors:
            return AddEmployee(success=False, errors=errors, employee=None)

        # create user
        user = get_user_model().objects.create(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email'),
            username=user_data.get('username'),
            company=company,
            type=UserType.COMPANY
        )

        # create employee
        employee = EmployeeModel.objects.create(
            role=employee_data.get('role'),
            user=user
        )

        user.status.send_password_reset_email(info)

        return AddEmployee(success=True, errors=None, employee=employee)


class EmployeeMutation(graphene.ObjectType):
    add_employee = AddEmployee.Field()
