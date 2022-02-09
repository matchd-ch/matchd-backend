import pytest

from db.models import User
from db.models.employee import Employee


@pytest.mark.django_db
def test_create_employee(employee_valid_args):
    employee = Employee.objects.create(**employee_valid_args)

    assert isinstance(employee, Employee)


@pytest.mark.django_db
def test_get_employee(employee_valid_args):
    employee = Employee.objects.create(**employee_valid_args)
    employee = Employee.objects.get(id=employee.id)

    assert isinstance(employee, Employee)
    assert isinstance(employee.user, User)
    assert isinstance(employee.role, str)

    assert employee.user.first_name == employee_valid_args.get('user').first_name
    assert employee.role == employee_valid_args.get('role')


@pytest.mark.django_db
def test_update_employee(employee_valid_args):
    new_role = 'Lead developer'
    employee = Employee.objects.create(**employee_valid_args)
    Employee.objects.filter(id=employee.id).update(role=new_role)
    employee.refresh_from_db()

    assert isinstance(employee, Employee)
    assert isinstance(employee.role, str)

    assert employee.role == new_role


@pytest.mark.django_db
def test_delete_employee(employee_valid_args):
    employee = Employee.objects.create(**employee_valid_args)
    number_of_deletions, _ = employee.delete()

    assert number_of_deletions == 1
