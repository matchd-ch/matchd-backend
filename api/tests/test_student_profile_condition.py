import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from db.models import ProfileState


@pytest.mark.django_db
def test_condition(login, user_student, student_condition):
    login(user_student)
    data, errors = student_condition(user_student, ProfileState.PUBLIC)
    assert errors is None
    assert data is not None
    assert data.get('studentProfileCondition') is not None
    assert data.get('studentProfileCondition').get('success')

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.state == ProfileState.PUBLIC


@pytest.mark.django_db
def test_condition_without_login(user_student, student_condition):
    data, errors = student_condition(AnonymousUser(), ProfileState.PUBLIC)
    assert errors is not None
    assert data is not None
    assert data.get('studentProfileCondition') is None

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.state == ProfileState.PUBLIC


@pytest.mark.django_db
def test_condition_as_company(login, user_employee, student_condition):
    login(user_employee)
    data, errors = student_condition(user_employee, ProfileState.PUBLIC)
    assert errors is None
    assert data is not None
    assert data.get('studentProfileCondition') is not None

    errors = data.get('studentProfileCondition').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_condition_invalid_data(login, user_student, student_condition):
    login(user_student)
    data, errors = student_condition(user_student, 'invalid')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileCondition') is not None
    assert data.get('studentProfileCondition').get('success') is False

    errors = data.get('studentProfileCondition').get('errors')
    assert errors is not None
    assert 'state' in errors

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.state == ProfileState.PUBLIC
