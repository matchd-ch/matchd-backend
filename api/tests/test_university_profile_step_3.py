import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from db.models import ProfileState


@pytest.mark.django_db
def test_step_3(login, user_rector, university_step_3):
    user_rector.company.profile_step = 3
    user_rector.company.save()
    login(user_rector)
    data, errors = university_step_3(user_rector, 'services', 'http://edu.lo', 'http://projects.lo', 'http://thesis.lo')
    assert errors is None
    assert data is not None
    assert data.get('universityProfileStep3') is not None
    assert data.get('universityProfileStep3').get('success')

    user = get_user_model().objects.get(pk=user_rector.id)

    assert user.company.services == 'services'
    assert user.company.link_education == 'http://edu.lo'
    assert user.company.link_projects == 'http://projects.lo'
    assert user.company.link_thesis == 'http://thesis.lo'
    assert user.company.profile_step == 4
    assert user.company.state == ProfileState.PUBLIC


@pytest.mark.django_db
def test_step_3_without_login(user_rector, university_step_3):
    user_rector.company.profile_step = 3
    user_rector.company.save()
    data, errors = university_step_3(AnonymousUser(), 'services', 'http://edu.lo', 'http://projects.lo',
                                     'http://thesis.lo')
    assert errors is not None
    assert data is not None
    assert data.get('universityProfileStep3') is None

    user = get_user_model().objects.get(pk=user_rector.id)

    assert user.company.services == ''
    assert user.company.link_education is None
    assert user.company.link_projects is None
    assert user.company.link_thesis is None
    assert user.company.profile_step == 3


@pytest.mark.django_db
def test_step_3_as_student(login, user_student, university_step_3):
    login(user_student)
    data, errors = university_step_3(user_student, 'services', 'http://edu.lo', 'http://projects.lo',
                                     'http://thesis.lo')
    assert errors is None
    assert data is not None
    assert data.get('universityProfileStep3') is not None

    errors = data.get('universityProfileStep3').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_step_3_invalid_step(login, user_rector, university_step_3):
    user_rector.company.profile_step = 0
    user_rector.company.save()
    login(user_rector)
    data, errors = university_step_3(user_rector, 'services', 'http://edu.lo', 'http://projects.lo', 'http://thesis.lo')
    assert errors is None
    assert data is not None
    assert data.get('universityProfileStep3') is not None
    assert data.get('universityProfileStep3').get('success') is False

    errors = data.get('universityProfileStep3').get('errors')
    assert errors is not None
    assert 'profileStep' in errors

    user = get_user_model().objects.get(pk=user_rector.id)
    assert user.company.profile_step == 0


@pytest.mark.django_db
def test_step_3_invalid_data(login, user_rector, university_step_3):
    user_rector.company.profile_step = 3
    user_rector.company.save()
    login(user_rector)
    data, errors = university_step_3(user_rector, 'a' * 301, 'invalid', 'invalid', 'invalid')
    assert errors is None
    assert data is not None
    assert data.get('universityProfileStep3') is not None
    assert data.get('universityProfileStep3').get('success') is False

    errors = data.get('universityProfileStep3').get('errors')
    assert errors is not None
    assert 'services' in errors
    assert 'linkEducation' in errors
    assert 'linkProjects' in errors
    assert 'linkThesis' in errors

    user = get_user_model().objects.get(pk=user_rector.id)
    assert user.company.profile_step == 3
