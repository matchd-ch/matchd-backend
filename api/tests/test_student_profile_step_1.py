import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from db.helper.forms import convert_date


@pytest.mark.django_db
def test_step_1(login, user_student, student_step_1):
    login(user_student)
    data, errors = student_step_1(user_student, 'John', 'Doe', 'street 1', '0000', 'nowhere', '01.01.1337',
                                  '+41791234567')

    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep1') is not None
    assert data.get('studentProfileStep1').get('success')

    user = get_user_model().objects.get(pk=user_student.id)

    assert user.first_name == 'John'
    assert user.last_name == 'Doe'
    assert user.student.street == 'street 1'
    assert user.student.zip == '0000'
    assert user.student.city == 'nowhere'
    assert user.student.date_of_birth == convert_date('01.01.1337')
    assert user.student.mobile == '+41791234567'
    assert user.student.profile_step == 2


@pytest.mark.django_db
def test_step_1_without_login(user_student, student_step_1):
    data, errors = student_step_1(AnonymousUser(), 'John', 'Doe', 'street 1', '0000', 'nowhere', '01.01.1337',
                                  '+41791234569')

    assert errors is not None
    assert data is not None
    assert data.get('studentProfileStep1') is None

    user = get_user_model().objects.get(pk=user_student.id)

    assert user.first_name == ''
    assert user.last_name == ''
    assert user.student.street == ''
    assert user.student.zip == ''
    assert user.student.city == ''
    assert user.student.date_of_birth is None
    assert user.student.mobile == ''
    assert user.student.profile_step == 1


@pytest.mark.django_db
def test_step_1_as_company(login, user_employee, student_step_1):
    login(user_employee)
    data, errors = student_step_1(user_employee, 'John', 'Doe', 'street 1', '0000', 'nowhere', '01.01.1337',
                                  '+41791234569')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep1') is not None

    errors = data.get('studentProfileStep1').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_step_1_invalid_step(login, user_student, student_step_1):
    user_student.student.profile_step = 0
    user_student.student.save()
    login(user_student)
    data, errors = student_step_1(user_student, 'John', 'Doe', 'street 1', '0000', 'nowhere', '01.01.1337',
                                  '+41791234567')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep1') is not None
    assert data.get('studentProfileStep1').get('success') is False

    errors = data.get('studentProfileStep1').get('errors')
    assert errors is not None
    assert 'profileStep' in errors

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.profile_step == 0


@pytest.mark.django_db
def test_step_1_invalid_data(login, user_student, student_step_1):
    login(user_student)
    data, errors = student_step_1(user_student, '', '', '', '', '', '1337.1337.1337', '')
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep1') is not None
    assert data.get('studentProfileStep1').get('success') is False

    errors = data.get('studentProfileStep1').get('errors')
    assert errors is not None
    assert 'firstName' in errors
    assert 'lastName' in errors
    assert 'street' not in errors
    assert 'zip' not in errors
    assert 'city' not in errors
    assert 'dateOfBirth' in errors
    assert 'mobile' not in errors

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.profile_step == 1
