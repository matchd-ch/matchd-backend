import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from db.models import Branch


@pytest.mark.django_db
def test_step_2(login, user_rector, university_step_2, branch_objects):
    user_rector.company.profile_step = 2
    user_rector.company.save()
    login(user_rector)
    data, errors = university_step_2(user_rector, 'description', branch_objects)
    print(data)
    print(errors)
    assert errors is None
    assert data is not None
    assert data.get('universityProfileStep2') is not None
    assert data.get('universityProfileStep2').get('success')

    user = get_user_model().objects.get(pk=user_rector.id)

    assert user.company.description == 'description'
    assert len(user.company.branches.all()) == len(branch_objects)
    assert user.company.profile_step == 3


@pytest.mark.django_db
def test_step_2_without_login(user_rector, university_step_2, branch_objects):
    data, errors = university_step_2(AnonymousUser(), 'description', branch_objects)

    assert errors is not None
    assert data is not None
    assert data.get('universityProfileStep2') is None

    user = get_user_model().objects.get(pk=user_rector.id)

    assert user.company.description == ''
    assert len(user.company.branches.all()) == 0
    assert user.company.profile_step == 1


@pytest.mark.django_db
def test_step_2_as_student(login, user_student, university_step_2, branch_objects):
    login(user_student)
    data, errors = university_step_2(user_student, 'description', branch_objects)
    assert errors is None
    assert data is not None
    assert data.get('universityProfileStep2') is not None

    errors = data.get('universityProfileStep2').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_step_2_invalid_step(login, user_rector, university_step_2, branch_objects):
    user_rector.company.profile_step = 0
    user_rector.company.save()
    login(user_rector)
    data, errors = university_step_2(user_rector, 'description', branch_objects)
    assert errors is None
    assert data is not None
    assert data.get('universityProfileStep2') is not None
    assert data.get('universityProfileStep2').get('success') is False

    errors = data.get('universityProfileStep2').get('errors')
    assert errors is not None
    assert 'profileStep' in errors

    user = get_user_model().objects.get(pk=user_rector.id)
    assert user.company.profile_step == 0


@pytest.mark.django_db
def test_step_2_invalid_data(login, user_rector, university_step_2):
    user_rector.company.profile_step = 2
    user_rector.company.save()
    login(user_rector)
    data, errors = university_step_2(user_rector, 'a' * 1001, [Branch(id=1337)])
    assert errors is None
    assert data is not None
    assert data.get('universityProfileStep2') is not None
    assert data.get('universityProfileStep2').get('success') is False

    errors = data.get('universityProfileStep2').get('errors')
    assert errors is not None
    assert 'description' in errors
    assert 'branches' in errors

    user = get_user_model().objects.get(pk=user_rector.id)
    assert user.company.profile_step == 2
