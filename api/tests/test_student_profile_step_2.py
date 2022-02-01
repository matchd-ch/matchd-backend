import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from db.helper.forms import convert_date
from db.models import JobType, DateMode, Branch


@pytest.mark.django_db
def test_step_2_date_range(login, user_student, student_step_2, job_type_objects_date_range, branch_objects):
    user_student.student.profile_step = 2
    user_student.student.save()
    login(user_student)
    data, errors = student_step_2(user_student, job_type_objects_date_range[0], '01.1337', '02.1337', branch_objects[0])
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep2') is not None
    assert data.get('studentProfileStep2').get('success')

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.job_type.id == job_type_objects_date_range[0].id
    assert user.student.branch.id == branch_objects[0].id
    assert user.student.job_from_date == convert_date('01.1337', '%m.%Y')
    assert user.student.job_to_date == convert_date('02.1337', '%m.%Y')
    assert user.student.profile_step == 3


@pytest.mark.django_db
def test_step_2_without_valid_date_range(login, user_student, student_step_2, job_type_objects_date_range,
                                         branch_objects):
    user_student.student.profile_step = 2
    user_student.student.save()
    login(user_student)
    data, errors = student_step_2(user_student, job_type_objects_date_range[0], None, None, branch_objects[0])

    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep2') is not None
    assert data.get('studentProfileStep2').get('success') is False

    errors = data.get('studentProfileStep2').get('errors')
    assert errors is not None
    assert 'jobFromDate' in errors
    assert 'jobToDate' in errors

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.job_type is None
    assert user.student.branch is None
    assert user.student.job_from_date is None
    assert user.student.job_to_date is None
    assert user.student.profile_step == 2


@pytest.mark.django_db
def test_step_2_with_from_date_only(login, user_student, student_step_2,
                                                        job_type_objects_date_range, branch_objects):
    user_student.student.profile_step = 2
    user_student.student.save()
    login(user_student)
    data, errors = student_step_2(user_student, job_type_objects_date_range[0], '01.1337', None, branch_objects[0])

    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep2') is not None
    assert data.get('studentProfileStep2').get('success') is False

    errors = data.get('studentProfileStep2').get('errors')
    assert errors is not None
    assert 'jobToDate' in errors

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.job_type is None
    assert user.student.branch is None
    assert user.student.job_from_date is None
    assert user.student.job_to_date is None
    assert user.student.profile_step == 2


@pytest.mark.django_db
def test_step_2_date_from(login, user_student, student_step_2, job_type_objects_date_from, branch_objects):
    user_student.student.profile_step = 2
    user_student.student.save()
    login(user_student)
    data, errors = student_step_2(user_student, job_type_objects_date_from[0], '01.1337', None, branch_objects[0])
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep2') is not None
    assert data.get('studentProfileStep2').get('success')

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.job_type.id == job_type_objects_date_from[0].id
    assert user.student.branch.id == branch_objects[0].id
    assert user.student.job_from_date == convert_date('01.1337', '%m.%Y')
    assert user.student.job_to_date is None
    assert user.student.profile_step == 3


@pytest.mark.django_db
def test_step_2_without_login(user_student, student_step_2, job_type_objects_date_range, branch_objects):
    data, errors = student_step_2(AnonymousUser(), job_type_objects_date_range[0], '01.1337', '02.1337',
                                  branch_objects[0])
    assert errors is not None
    assert data is not None
    assert data.get('studentProfileStep2') is None

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.job_type is None
    assert user.student.branch is None
    assert user.student.job_from_date is None
    assert user.student.job_to_date is None
    assert user.student.profile_step == 1


@pytest.mark.django_db
def test_step_2_as_company(login, user_employee, student_step_2, job_type_objects_date_range, branch_objects):
    login(user_employee)
    data, errors = student_step_2(user_employee, job_type_objects_date_range[0], '01.1337', '02.1337',
                                  branch_objects[0])

    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep2') is not None

    errors = data.get('studentProfileStep2').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_step_2_invalid_step(login, user_student, student_step_2, job_type_objects_date_range, branch_objects):
    user_student.student.profile_step = 0
    user_student.student.save()
    login(user_student)
    data, errors = student_step_2(user_student, job_type_objects_date_range[0], '01.1337', '02.1337', branch_objects[0])
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep2') is not None
    assert data.get('studentProfileStep2').get('success') is False

    errors = data.get('studentProfileStep2').get('errors')
    assert errors is not None
    assert 'profileStep' in errors

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.profile_step == 0


@pytest.mark.django_db
def test_step_2_invalid_date_range(login, user_student, student_step_2):
    user_student.student.profile_step = 2
    user_student.student.save()

    login(user_student)
    data, errors = student_step_2(user_student, JobType(id=1337, mode=DateMode.DATE_RANGE), '03.1337', '02.1337',
                                  Branch(id=1337))
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep2') is not None

    errors = data.get('studentProfileStep2').get('errors')
    assert errors is not None
    assert 'jobType' in errors
    assert 'branch' in errors


@pytest.mark.django_db
def test_step_2_invalid_date_from(login, user_student, student_step_2):
    user_student.student.profile_step = 2
    user_student.student.save()
    login(user_student)
    data, errors = student_step_2(user_student, JobType(id=1337, mode=DateMode.DATE_FROM), '1337.1337', None,
                                  Branch(id=1337))
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep2') is not None

    errors = data.get('studentProfileStep2').get('errors')
    assert errors is not None
    assert 'jobType' in errors
    assert 'branch' in errors


@pytest.mark.django_db
def test_step_2_invalid_date_range_with_valid_job_type(login, user_student, student_step_2,
                                                       job_type_objects_date_range):
    user_student.student.profile_step = 2
    user_student.student.save()
    login(user_student)
    data, errors = student_step_2(user_student, job_type_objects_date_range[0], '03.1337', '02.1337',
                                  Branch(id=1337))
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep2') is not None

    errors = data.get('studentProfileStep2').get('errors')
    assert errors is not None
    assert 'jobToDate' in errors
    assert 'branch' in errors


@pytest.mark.django_db
def test_step_2_invalid_date_from_with_valid_job_type(login, user_student, student_step_2, job_type_objects_date_from):
    user_student.student.profile_step = 2
    user_student.student.save()
    login(user_student)
    data, errors = student_step_2(user_student, job_type_objects_date_from[0], '1337.1337', None, Branch(id=1337))
    assert errors is None
    assert data is not None
    assert data.get('studentProfileStep2') is not None

    errors = data.get('studentProfileStep2').get('errors')
    assert errors is not None
    assert 'jobFromDate' in errors
    assert 'branch' in errors
