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


@pytest.mark.django_db
def test_delete_employee(login, user_employee, user_employee_2, delete_employee):
    company = user_employee.company
    user_employee_2.company = company
    user_employee_2.save()

    employee_count = len(company.users.all())

    login(user_employee)
    data, errors = delete_employee(user_employee, user_employee_2.employee.id)
    assert errors is None
    assert data is not None

    assert data.get('deleteEmployee') is not None
    assert data.get('deleteEmployee').get('success')
    assert employee_count - 1 == len(company.users.all())


@pytest.mark.django_db
def test_delete_employee_fails_user_doesnt_exists(login, user_employee, delete_employee):
    company = user_employee.company
    employee_count = len(company.users.all())

    login(user_employee)
    data, errors = delete_employee(user_employee, 9999999)
    assert errors is None
    assert data is not None

    assert data.get('deleteEmployee') is not None
    assert not data.get('deleteEmployee').get('success')
    error_message = data.get('deleteEmployee').get('errors').get('id')[0].get('message')
    assert error_message == 'An employee with the specified id does not exist'
    assert employee_count == len(company.users.all())


@pytest.mark.django_db
def test_delete_employee_fails_cannot_delete_itself(login, user_employee, delete_employee):
    company = user_employee.company
    employee_count = len(company.users.all())

    login(user_employee)
    data, errors = delete_employee(user_employee, user_employee.employee.id)
    assert errors is None
    assert data is not None

    assert data.get('deleteEmployee') is not None
    assert not data.get('deleteEmployee').get('success')
    error_message = data.get('deleteEmployee').get('errors').get('id')[0].get('message')
    assert error_message == 'An employee cannot delete itself'
    assert employee_count == len(company.users.all())


@pytest.mark.django_db
def test_delete_employee_fails_employee_not_in_same_company(login, user_employee, user_employee_2,
                                                            delete_employee):
    company = user_employee.company
    employee_count = len(company.users.all())

    login(user_employee)
    data, errors = delete_employee(user_employee, user_employee_2.employee.id)
    assert errors is None
    assert data is not None

    assert data.get('deleteEmployee') is not None
    assert not data.get('deleteEmployee').get('success')
    error_message = data.get('deleteEmployee').get('errors').get('id')[0].get('message')
    assert error_message == 'The employee to delete is not part of the same company'
    assert employee_count == len(company.users.all())
