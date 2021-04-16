import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_step_5(login, user_student, student_step_5):
    user_student.student.profile_step = 5
    user_student.student.save()
    login(user_student)
    data, errors = student_step_5(user_student, 'nickname')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep5') is not None
    assert data.get('studentProfileStep5').get('success')
    assert data.get('studentProfileStep5').get('nickname_suggestions') is None

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.nickname == 'nickname'
    assert user.student.slug == 'nickname'
    assert user_student.student.profile_step == 6


@pytest.mark.django_db
def test_step_5_without_login(user_student, student_step_5):
    data, errors = student_step_5(AnonymousUser(), 'nickname')
    assert errors is not None
    assert data is not None
    assert data.get('studentProfileStep5') is None

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.nickname is None


@pytest.mark.django_db
def test_step_5_as_company(login, user_employee, student_step_5):
    login(user_employee)
    data, errors = student_step_5(user_employee, 'nickname')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep5') is not None

    errors = data.get('studentProfileStep5').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_step_5_invalid_step(login, user_student, student_step_5):
    user_student.student.profile_step = 0
    user_student.student.save()
    login(user_student)
    data, errors = student_step_5(user_student, 'nickname')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep5') is not None
    assert data.get('studentProfileStep5').get('success') is False

    errors = data.get('studentProfileStep5').get('errors')
    assert errors is not None
    assert 'profileStep' in errors

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.profile_step == 0


@pytest.mark.django_db
def test_step_5_invalid_data(login, user_student, student_step_5):
    user_student.student.profile_step = 5
    user_student.student.save()
    login(user_student)
    data, errors = student_step_5(user_student, '')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep5') is not None
    assert data.get('studentProfileStep5').get('success') is False

    errors = data.get('studentProfileStep5').get('errors')
    assert errors is not None
    assert 'nickname' in errors


@pytest.mark.django_db
def test_step_5_nickname_already_exists(login, user_student, user_student_2, student_step_5):
    user_student_2.student.nickname = 'nickname'
    user_student_2.student.save()
    user_student.student.profile_step = 5
    user_student.student.save()
    login(user_student)
    data, errors = student_step_5(user_student, 'nickname')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep5') is not None
    assert data.get('studentProfileStep5').get('success') is False

    errors = data.get('studentProfileStep5').get('errors')
    assert errors is not None
    assert 'nickname' in errors

    nickname_suggestions = data.get('studentProfileStep5').get('nicknameSuggestions')
    assert nickname_suggestions is not None
    assert len(nickname_suggestions) == 5

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.profile_step == 5
