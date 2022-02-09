import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from django.utils.translation import gettext as _

from db.context.employee.employee_builder import EmployeeBuilder
from db.models import Employee as EmployeeModel


class Employee(DjangoObjectType):
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    phone = graphene.String()

    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )
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

        employee_builder = EmployeeBuilder().build(user, info, form_data)
        errors = employee_builder.errors
        employee = employee_builder.employee

        return AddEmployee(success=bool(employee), errors=errors, employee=employee)


class EmployeeMutation(ObjectType):
    add_employee = AddEmployee.Field()
