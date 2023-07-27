import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from db.helper.forms import convert_date


@pytest.mark.django_db
def test_base_data(login, user_student, student_base_data):
    login(user_student)
    data, errors = student_base_data(user_student, 'John', 'Doe', 'street 1', '0000', 'nowhere',
                                     '01.01.1337', '+41791234567')

    assert errors is None
    assert data is not None
    assert data.get('studentProfileBaseData') is not None
    assert data.get('studentProfileBaseData').get('success')

    user = get_user_model().objects.get(pk=user_student.id)

    assert user.first_name == 'John'
    assert user.last_name == 'Doe'
    assert user.student.street == 'street 1'
    assert user.student.zip == '0000'
    assert user.student.city == 'nowhere'
    assert user.student.date_of_birth == convert_date('01.01.1337')
    assert user.student.mobile == '+41791234567'


@pytest.mark.django_db
def test_base_data_without_login(user_student, student_base_data):
    data, errors = student_base_data(AnonymousUser(), 'John', 'Doe', 'street 1', '0000', 'nowhere',
                                     '01.01.1337', '+41791234569')

    assert errors is not None
    assert data is not None
    assert data.get('studentProfileBaseData') is None

    user = get_user_model().objects.get(pk=user_student.id)

    assert user.first_name == ''
    assert user.last_name == ''
    assert user.student.street == ''
    assert user.student.zip == ''
    assert user.student.city == ''
    assert user.student.date_of_birth is None
    assert user.student.mobile == ''


@pytest.mark.django_db
def test_base_data_as_company(login, user_employee, student_base_data):
    login(user_employee)
    data, errors = student_base_data(user_employee, 'John', 'Doe', 'street 1', '0000', 'nowhere',
                                     '01.01.1337', '+41791234569')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileBaseData') is not None

    errors = data.get('studentProfileBaseData').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_base_data_invalid_data(login, user_student, student_base_data):
    login(user_student)
    data, errors = student_base_data(user_student, '', '', '', '', '', '1337.1337.1337', '')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileBaseData') is not None
    assert data.get('studentProfileBaseData').get('success') is False

    errors = data.get('studentProfileBaseData').get('errors')
    assert errors is not None
    assert 'firstName' in errors
    assert 'lastName' in errors
    assert 'street' not in errors
    assert 'zip' not in errors
    assert 'city' not in errors
    assert 'dateOfBirth' in errors
    assert 'mobile' not in errors
