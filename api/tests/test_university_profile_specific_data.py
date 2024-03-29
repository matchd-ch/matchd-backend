import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_specific_data(login, user_rector, university_specific_data):
    login(user_rector)

    data, errors = university_specific_data(user_rector, 'description')
    assert errors is None
    assert data is not None
    assert data.get('universityProfileSpecificData') is not None
    assert data.get('universityProfileSpecificData').get('success')

    user = get_user_model().objects.get(pk=user_rector.id)

    assert user.company.description == 'description'


@pytest.mark.django_db
def test_specific_data_without_login(user_rector, university_specific_data):
    data, errors = university_specific_data(AnonymousUser(), 'description')

    assert errors is not None
    assert data is not None
    assert data.get('universityProfileSpecificData') is None

    user = get_user_model().objects.get(pk=user_rector.id)

    assert user.company.description == ''


@pytest.mark.django_db
def test_specific_data_as_student(login, user_student, university_specific_data):
    login(user_student)
    data, errors = university_specific_data(user_student, 'description')
    assert errors is None
    assert data is not None
    assert data.get('universityProfileSpecificData') is not None

    errors = data.get('universityProfileSpecificData').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_specific_data_invalid_data(login, user_rector, university_specific_data):
    login(user_rector)
    data, errors = university_specific_data(user_rector, 'a' * 3001)
    assert errors is None
    assert data is not None
    assert data.get('universityProfileSpecificData') is not None
    assert data.get('universityProfileSpecificData').get('success') is False

    errors = data.get('universityProfileSpecificData').get('errors')
    assert errors is not None
    assert 'description' in errors
