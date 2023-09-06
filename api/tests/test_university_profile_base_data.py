import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_base_data(login, user_rector, university_base_data):
    login(user_rector)
    data, errors = university_base_data(user_rector, 'John', 'Doe', 'University 1 edited',
                                        'street 1', '1337', 'nowhere', '+41791234567', 'Role',
                                        'https://www.1337.lo', 'https://www.top-level.lo',
                                        'top level description')
    assert errors is None
    assert data is not None
    assert data.get('universityProfileBaseData') is not None
    assert data.get('universityProfileBaseData').get('success')

    user = get_user_model().objects.get(pk=user_rector.id)
    assert user.first_name == 'John'
    assert user.last_name == 'Doe'
    assert user.company.name == 'University 1 edited'
    assert user.company.street == 'street 1'
    assert user.company.zip == '1337'
    assert user.company.city == 'nowhere'
    assert user.company.phone == '+41791234567'
    assert user.company.website == 'https://www.1337.lo'
    assert user.company.top_level_organisation_website == 'https://www.top-level.lo'
    assert user.company.top_level_organisation_description == 'top level description'
    assert user.employee.role == 'Role'


@pytest.mark.django_db
def test_base_data_without_login(user_rector, university_base_data):
    data, errors = university_base_data(AnonymousUser(), 'John', 'Doe', 'University 1 edited',
                                        'street 1', '1337', 'nowhere', '+41791234567', 'Role',
                                        'https://www.1337.lo', 'https://www.top-level.lo',
                                        'top level description')
    assert errors is not None
    assert data is not None
    assert data.get('universityProfileBaseData') is None

    user = get_user_model().objects.get(pk=user_rector.id)
    assert user.first_name == ''
    assert user.last_name == ''
    assert user.company.name == 'University 1'
    assert user.company.street == ''
    assert user.company.zip == ''
    assert user.company.city == ''
    assert user.company.phone == ''
    assert user.employee.role == ''


@pytest.mark.django_db
def test_base_data_as_student(login, user_student, university_base_data):
    login(user_student)
    data, errors = university_base_data(user_student, 'John', 'Doe', 'Company 1 edited', 'street 1',
                                        '1337', 'nowhere', '+41791234567', 'Role',
                                        'https://www.1337.lo', 'https://www.top-level.lo',
                                        'top level description')
    assert errors is None
    assert data is not None
    assert data.get('universityProfileBaseData') is not None

    errors = data.get('universityProfileBaseData').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_base_data_empty_data(login, user_rector, university_base_data):
    login(user_rector)
    data, errors = university_base_data(user_rector, '', '', 'test', '', '', '', '', '', '', '',
                                        'a' * 1000)
    assert errors is None
    assert data is not None

    assert data.get('universityProfileBaseData') is not None
    assert data.get('universityProfileBaseData').get('success') is True

    errors = data.get('universityProfileBaseData').get('errors')
    assert errors is None


@pytest.mark.django_db
def test_base_data_invalid_data(login, user_rector, university_base_data):
    login(user_rector)
    data, errors = university_base_data(user_rector, '', '', '', '', '', '', '', '', '', 'invalid',
                                        'a' * 1001)
    assert errors is None
    assert data is not None
    assert data.get('universityProfileBaseData') is not None
    assert data.get('universityProfileBaseData').get('success') is False

    errors = data.get('universityProfileBaseData').get('errors')
    assert errors is not None
    assert 'name' in errors
    assert 'topLevelOrganisationWebsite' in errors
    assert 'topLevelOrganisationDescription' in errors
