import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphql_auth.bases import Output
from graphql_jwt.decorators import login_required

from django.utils.translation import gettext as _

from api.helper import resolve_node_id

from db.context.employee import EmployeeBuilder, EmployeeManager
from db.models import Employee as EmployeeModel

# pylint: disable=W0221


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
    id = graphene.String(required=False)
    role = graphene.String(description=_('Role'), required=False)


class AddEmployee(Output, relay.ClientIDMutation):

    employee = graphene.Field(Employee)

    class Input:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        role = graphene.String(required=True)
        email = graphene.String(required=True)

    class Meta:
        description = _('Adds a new emplyoee to a company')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        form_data = data.get('input', None)

        employee_builder = EmployeeBuilder().build(user, info, form_data)
        errors = employee_builder.errors
        employee = employee_builder.employee

        return AddEmployee(success=bool(employee), errors=errors, employee=employee)


class DeleteEmployee(Output, relay.ClientIDMutation):

    class Input:
        id = graphene.String(required=True)

    class Meta:
        description = _('Deletes an employee within the same company')

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user

        form_data = data.get('input', None)
        id_to_delete = int(resolve_node_id(form_data.get('id')))

        employee_manager = EmployeeManager(id_to_delete).delete(user)
        errors = employee_manager.errors
        employee = employee_manager.employee

        return DeleteEmployee(success=(employee is None and errors == {}), errors=errors)


class EmployeeMutation(ObjectType):
    add_employee = AddEmployee.Field()
    delete_employee = DeleteEmployee.Field()
