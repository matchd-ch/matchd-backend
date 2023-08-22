import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_base_data(login, user_employee, company_base_data):
    login(user_employee)
    data, errors = company_base_data(user_employee, 'John', 'Doe', 'Company 1 edited', 'street 1',
                                     '1337', 'nowhere', '+41791234567', 'Role')
    assert errors is None
    assert data is not None
    assert data.get('companyProfileBaseData') is not None
    assert data.get('companyProfileBaseData').get('success')

    user = get_user_model().objects.get(pk=user_employee.id)
    assert user.first_name == 'John'
    assert user.last_name == 'Doe'
    assert user.company.name == 'Company 1 edited'
    assert user.company.street == 'street 1'
    assert user.company.zip == '1337'
    assert user.company.city == 'nowhere'
    assert user.company.phone == '+41791234567'
    assert user.employee.role == 'Role'


@pytest.mark.django_db
def test_base_data_without_login(user_employee, company_base_data):
    data, errors = company_base_data(AnonymousUser(), 'John', 'Doe', 'Company 1 edited', 'street 1',
                                     '1337', 'nowhere', '+41791234567', 'Role')
    assert errors is not None
    assert data is not None
    assert data.get('companyProfileBaseData') is None

    user = get_user_model().objects.get(pk=user_employee.id)
    assert user.first_name == ''
    assert user.last_name == ''
    assert user.company.name == 'Company 1'
    assert user.company.street == ''
    assert user.company.zip == ''
    assert user.company.city == ''
    assert user.company.phone == ''
    assert user.employee.role == ''


@pytest.mark.django_db
def test_base_data_as_student(login, user_student, company_base_data):
    login(user_student)
    data, errors = company_base_data(user_student, 'John', 'Doe', 'Company 1 edited', 'street 1',
                                     '1337', 'nowhere', '+41791234567', 'Role')
    assert errors is None
    assert data is not None
    assert data.get('companyProfileBaseData') is not None

    errors = data.get('companyProfileBaseData').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_base_data_empty_data(login, user_employee, company_base_data):
    login(user_employee)
    data, errors = company_base_data(user_employee, '', '', '', '', '', '', '', '')
    assert errors is None
    assert data is not None
    assert data.get('companyProfileBaseData') is not None
    assert data.get('companyProfileBaseData').get('success') is True

    errors = data.get('companyProfileBaseData').get('errors')
    assert errors is None
