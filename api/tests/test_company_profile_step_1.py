import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_step_1(login, user_employee, company_step_1):
    login(user_employee)
    data, errors = company_step_1(user_employee, 'John', 'Doe', 'Company 1 edited', 'street 1', '1337', 'nowhere',
                                  '+41791234567', 'Role')
    assert errors is None
    assert data is not None
    assert data.get('companyProfileStep1') is not None
    assert data.get('companyProfileStep1').get('success')

    user = get_user_model().objects.get(pk=user_employee.id)
    assert user.first_name == 'John'
    assert user.last_name == 'Doe'
    assert user.company.name == 'Company 1 edited'
    assert user.company.street == 'street 1'
    assert user.company.zip == '1337'
    assert user.company.city == 'nowhere'
    assert user.company.phone == '+41791234567'
    assert user.employee.role == 'Role'
    assert user.company.profile_step == 2


@pytest.mark.django_db
def test_step_1_without_login(user_employee, company_step_1):
    data, errors = company_step_1(AnonymousUser(), 'John', 'Doe', 'Company 1 edited', 'street 1', '1337', 'nowhere',
                                  '+41791234567', 'Role')
    assert errors is not None
    assert data is not None
    assert data.get('companyProfileStep1') is None

    user = get_user_model().objects.get(pk=user_employee.id)
    assert user.first_name == ''
    assert user.last_name == ''
    assert user.company.name == 'Company 1'
    assert user.company.street == ''
    assert user.company.zip == ''
    assert user.company.city == ''
    assert user.company.phone == ''
    assert user.employee.role == ''
    assert user.company.profile_step == 1


@pytest.mark.django_db
def test_step_1_as_student(login, user_student, company_step_1):
    login(user_student)
    data, errors = company_step_1(user_student, 'John', 'Doe', 'Company 1 edited', 'street 1', '1337', 'nowhere',
                                  '+41791234567', 'Role')
    assert errors is None
    assert data is not None
    assert data.get('companyProfileStep1') is not None

    errors = data.get('companyProfileStep1').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_step_1_invalid_step(login, user_employee, company_step_1):
    user_employee.company.profile_step = 0
    user_employee.company.save()
    login(user_employee)
    data, errors = company_step_1(user_employee, 'John', 'Doe', 'Company 1 edited', 'street 1', '1337', 'nowhere',
                                  '+41791234567', 'Role')
    assert errors is None
    assert data is not None
    assert data.get('companyProfileStep1') is not None
    assert data.get('companyProfileStep1').get('success') is False

    errors = data.get('companyProfileStep1').get('errors')
    assert errors is not None
    assert 'profileStep' in errors

    user = get_user_model().objects.get(pk=user_employee.id)
    assert user.company.profile_step == 0


@pytest.mark.django_db
def test_step_1_invalid_data(login, user_employee, company_step_1):
    login(user_employee)
    data, errors = company_step_1(user_employee, '', '', '', '', '', '', '', '')
    assert errors is None
    assert data is not None
    assert data.get('companyProfileStep1') is not None
    assert data.get('companyProfileStep1').get('success') is False

    errors = data.get('companyProfileStep1').get('errors')
    assert errors is not None
    assert 'firstName' in errors
    assert 'lastName' in errors
    assert 'name' in errors
    assert 'street' in errors
    assert 'zip' in errors
    assert 'city' in errors
    assert 'phone' in errors
    assert 'role' in errors

    user = get_user_model().objects.get(pk=user_employee.id)
    assert user.company.profile_step == 1
