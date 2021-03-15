import graphene
from django.contrib.auth import get_user_model
from graphql_auth.bases import Output
from django.utils.translation import gettext as _
from graphql_jwt.decorators import login_required

from api.schema.user.schema import Employee
from db.models import Employee as EmployeeModel


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
        employee_data = data.get('add_employee')
        user = get_user_model().objects.create(
            first_name=employee_data.get('first_name'),
            last_name=employee_data.get('last_name'),
            email=employee_data.get('email'),
            username=employee_data.get('email')
        )

        employee = EmployeeModel.objects.create(
            role=employee_data.get('role'),
            user=user
        )
        return AddEmployee(success=True, errors=None, employee=employee)


class EmployeeMutation(graphene.ObjectType):
    add_employee = AddEmployee.Field()
