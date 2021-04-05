import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from db.models import ProfileState


@pytest.mark.django_db
def test_step_6(login, user_student, student_step_6):
    user_student.student.profile_step = 6
    user_student.student.save()
    login(user_student)
    data, errors = student_step_6(user_student, ProfileState.PUBLIC)
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep6') is not None
    assert data.get('studentProfileStep6').get('success')

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.state == ProfileState.PUBLIC
    assert user_student.student.profile_step == 7


@pytest.mark.django_db
def test_step_6_without_login(user_student, student_step_6):
    data, errors = student_step_6(AnonymousUser(), ProfileState.PUBLIC)
    assert errors is not None
    assert data is not None
    assert data.get('studentProfileStep6') is None

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.state == ProfileState.INCOMPLETE


@pytest.mark.django_db
def test_step_6_as_company(login, user_employee, student_step_6):
    login(user_employee)
    data, errors = student_step_6(user_employee, ProfileState.PUBLIC)
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep6') is not None

    errors = data.get('studentProfileStep6').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_step_6_invalid_step(login, user_student, student_step_6):
    user_student.student.profile_step = 0
    user_student.student.save()
    login(user_student)
    data, errors = student_step_6(user_student, ProfileState.PUBLIC)
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep6') is not None
    assert data.get('studentProfileStep6').get('success') is False

    errors = data.get('studentProfileStep6').get('errors')
    assert errors is not None
    assert 'profileStep' in errors

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.profile_step == 0


@pytest.mark.django_db
def test_step_6_invalid_data(login, user_student, student_step_6):
    user_student.student.profile_step = 6
    user_student.student.save()
    login(user_student)
    data, errors = student_step_6(user_student, 'invalid')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep6') is not None
    assert data.get('studentProfileStep6').get('success') is False

    errors = data.get('studentProfileStep6').get('errors')
    assert errors is not None
    assert 'state' in errors

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.state == ProfileState.INCOMPLETE
    assert user_student.student.profile_step == 6


@pytest.mark.django_db
def test_step_6_invalid_data(login, user_student, student_step_6):
    user_student.student.profile_step = 6
    user_student.student.save()
    login(user_student)
    data, errors = student_step_6(user_student, ProfileState.INCOMPLETE)
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep6') is not None
    assert data.get('studentProfileStep6').get('success') is False

    errors = data.get('studentProfileStep6').get('errors')
    assert errors is not None
    assert 'state' in errors

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.state == ProfileState.INCOMPLETE
    assert user_student.student.profile_step == 6
