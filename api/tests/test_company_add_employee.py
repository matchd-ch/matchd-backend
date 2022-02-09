import pytest


@pytest.mark.django_db
def test_add_employee(login, user_employee, add_employee):
    company = user_employee.company
    employee_count = len(company.users.all())
    new_username = 'employee-2@matchd.test'
    login(user_employee)
    data, errors = add_employee(user_employee, new_username, 'John', 'Doe', 'Role')
    assert errors is None
    assert data is not None
    assert data.get('addEmployee') is not None
    assert data.get('addEmployee').get('success')

    employee = data.get('addEmployee').get('employee')
    assert employee is not None
    assert employee.get('role') == 'Role'
    assert employee.get('firstName') == 'John'
    assert employee.get('lastName') == 'Doe'
    assert employee.get('email') == new_username
    assert employee_count + 1 == len(company.users.all())


@pytest.mark.django_db
def test_add_employee_with_existing_username(login, user_employee, add_employee):
    company = user_employee.company
    employee_count = len(company.users.all())
    login(user_employee)
    data, errors = add_employee(user_employee, user_employee.username, 'John', 'Doe', 'Role')

    assert errors is None
    assert data is not None
    assert data.get('addEmployee') is not None
    assert data.get('addEmployee').get('success') is False
    assert data.get('addEmployee').get('employee') is None

    errors = data.get('addEmployee').get('errors')
    assert errors is not None
    assert 'username' in errors
    assert errors.get('username')[0].get('code') == 'unique'
    assert employee_count == len(company.users.all())
