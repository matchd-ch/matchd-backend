import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_specific_data(login, user_student, student_specific_data):
    login(user_student)
    data, errors = student_specific_data(user_student, 'nickname')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileSpecificData') is not None
    assert data.get('studentProfileSpecificData').get('success')
    assert data.get('studentProfileSpecificData').get('nickname_suggestions') is None

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.nickname == 'nickname'
    assert user.student.slug == 'nickname'


@pytest.mark.django_db
def test_specific_data_without_login(user_student, student_specific_data):
    data, errors = student_specific_data(AnonymousUser(), 'nickname')
    assert errors is not None
    assert data is not None
    assert data.get('studentProfileSpecificData') is None

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.nickname is None


@pytest.mark.django_db
def test_specific_data_as_company(login, user_employee, student_specific_data):
    login(user_employee)
    data, errors = student_specific_data(user_employee, 'nickname')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileSpecificData') is not None

    errors = data.get('studentProfileSpecificData').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_specific_data_invalid_data(login, user_student, student_specific_data):
    login(user_student)
    data, errors = student_specific_data(user_student, '')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileSpecificData') is not None
    assert data.get('studentProfileSpecificData').get('success') is False

    errors = data.get('studentProfileSpecificData').get('errors')
    assert errors is not None
    assert 'nickname' in errors


@pytest.mark.django_db
def test_specific_data_nickname_already_exists(login, user_student, user_student_2,
                                               student_specific_data):
    user_student_2.student.nickname = 'nickname'
    user_student_2.student.save()
    login(user_student)
    data, errors = student_specific_data(user_student, 'nickname')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileSpecificData') is not None
    assert data.get('studentProfileSpecificData').get('success') is False

    errors = data.get('studentProfileSpecificData').get('errors')
    assert errors is not None
    assert 'nickname' in errors

    nickname_suggestions = data.get('studentProfileSpecificData').get('nicknameSuggestions')
    assert nickname_suggestions is not None
    assert len(nickname_suggestions) == 5
