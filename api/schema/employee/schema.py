import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

from db.forms import EmployeeForm, UserForm
from db.helper.forms import validate_company_user_type, validate_form_data
from db.models import Employee as EmployeeModel


class Employee(DjangoObjectType):
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    phone = graphene.String()

    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node,)
        fields = ['role', 'user']

    def resolve_first_name(self: EmployeeModel, info):
        return self.user.first_name

    def resolve_last_name(self: EmployeeModel, info):
        return self.user.last_name

    def resolve_email(self: EmployeeModel, info):
        return self.user.email

    def resolve_phone(self: EmployeeModel, info):
        return self.user.company.phone


class EmployeeInput(graphene.InputObjectType):
    id = graphene.ID(required=False)
    role = graphene.String(description=_('Role'), required=False)


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
        description = _('Adds a new emplyoee to a company')

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
            type=user.type
        )

        # create employee
        employee = EmployeeModel.objects.create(
            role=employee_data.get('role'),
            user=user
        )

        user.status.send_password_reset_email(info)

        return AddEmployee(success=True, errors=None, employee=employee)


class EmployeeMutation(ObjectType):
    add_employee = AddEmployee.Field()
