import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from db.helper.forms import convert_date
from db.models import JobType, DateMode, Branch


@pytest.mark.django_db
def test_employment_date_range(login, user_student, student_employment, job_type_objects_date_range,
                               branch_objects):
    login(user_student)
    data, errors = student_employment(user_student, job_type_objects_date_range[0], '01.1337',
                                      '02.1337', branch_objects[0])
    assert errors is None
    assert data is not None
    assert data.get('studentProfileEmployment') is not None
    assert data.get('studentProfileEmployment').get('success')

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.job_type.id == job_type_objects_date_range[0].id
    assert user.student.branch.id == branch_objects[0].id
    assert user.student.job_from_date == convert_date('01.1337', '%m.%Y')
    assert user.student.job_to_date == convert_date('02.1337', '%m.%Y')


@pytest.mark.django_db
def test_employment_without_valid_date_range(login, user_student, student_employment,
                                             job_type_objects_date_range, branch_objects):
    user_student.student.save()
    login(user_student)
    data, errors = student_employment(user_student, job_type_objects_date_range[0], None, None,
                                      branch_objects[0])

    assert errors is None
    assert data is not None
    assert data.get('studentProfileEmployment') is not None
    assert data.get('studentProfileEmployment').get('success') is False

    errors = data.get('studentProfileEmployment').get('errors')
    assert errors is not None
    assert 'jobFromDate' in errors
    assert 'jobToDate' in errors

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.job_type is None
    assert user.student.branch is None
    assert user.student.job_from_date is None
    assert user.student.job_to_date is None


@pytest.mark.django_db
def test_employment_with_from_date_only(login, user_student, student_employment,
                                        job_type_objects_date_range, branch_objects):
    login(user_student)
    data, errors = student_employment(user_student, job_type_objects_date_range[0], '01.1337', None,
                                      branch_objects[0])

    assert errors is None
    assert data is not None
    assert data.get('studentProfileEmployment') is not None
    assert data.get('studentProfileEmployment').get('success') is False

    errors = data.get('studentProfileEmployment').get('errors')
    assert errors is not None
    assert 'jobToDate' in errors

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.job_type is None
    assert user.student.branch is None
    assert user.student.job_from_date is None
    assert user.student.job_to_date is None


@pytest.mark.django_db
def test_employment_date_from(login, user_student, student_employment, job_type_objects_date_from,
                              branch_objects):
    login(user_student)
    data, errors = student_employment(user_student, job_type_objects_date_from[0], '01.1337', None,
                                      branch_objects[0])
    assert errors is None
    assert data is not None
    assert data.get('studentProfileEmployment') is not None
    assert data.get('studentProfileEmployment').get('success')

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.job_type.id == job_type_objects_date_from[0].id
    assert user.student.branch.id == branch_objects[0].id
    assert user.student.job_from_date == convert_date('01.1337', '%m.%Y')
    assert user.student.job_to_date is None


@pytest.mark.django_db
def test_employment_without_login(user_student, student_employment, job_type_objects_date_range,
                                  branch_objects):
    data, errors = student_employment(AnonymousUser(), job_type_objects_date_range[0], '01.1337',
                                      '02.1337', branch_objects[0])
    assert errors is not None
    assert data is not None
    assert data.get('studentProfileEmployment') is None

    user = get_user_model().objects.get(pk=user_student.id)
    assert user.student.job_type is None
    assert user.student.branch is None
    assert user.student.job_from_date is None
    assert user.student.job_to_date is None


@pytest.mark.django_db
def test_employment_as_company(login, user_employee, student_employment,
                               job_type_objects_date_range, branch_objects):
    login(user_employee)
    data, errors = student_employment(user_employee, job_type_objects_date_range[0], '01.1337',
                                      '02.1337', branch_objects[0])

    assert errors is None
    assert data is not None
    assert data.get('studentProfileEmployment') is not None

    errors = data.get('studentProfileEmployment').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_employment_invalid_date_range(login, user_student, student_employment):
    login(user_student)
    data, errors = student_employment(user_student, JobType(id=1337, mode=DateMode.DATE_RANGE),
                                      '03.1337', '02.1337', Branch(id=1337))
    assert errors is None
    assert data is not None
    assert data.get('studentProfileEmployment') is not None

    errors = data.get('studentProfileEmployment').get('errors')
    assert errors is not None
    assert 'jobType' in errors
    assert 'branch' in errors


@pytest.mark.django_db
def test_employment_invalid_date_from(login, user_student, student_employment):
    login(user_student)
    data, errors = student_employment(user_student, JobType(id=1337, mode=DateMode.DATE_FROM),
                                      '1337.1337', None, Branch(id=1337))
    assert errors is None
    assert data is not None
    assert data.get('studentProfileEmployment') is not None

    errors = data.get('studentProfileEmployment').get('errors')
    assert errors is not None
    assert 'jobType' in errors
    assert 'branch' in errors


@pytest.mark.django_db
def test_employment_invalid_date_range_with_valid_job_type(login, user_student, student_employment,
                                                           job_type_objects_date_range):
    login(user_student)
    data, errors = student_employment(user_student, job_type_objects_date_range[0], '03.1337',
                                      '02.1337', Branch(id=1337))
    assert errors is None
    assert data is not None
    assert data.get('studentProfileEmployment') is not None

    errors = data.get('studentProfileEmployment').get('errors')
    assert errors is not None
    assert 'jobToDate' in errors
    assert 'branch' in errors


@pytest.mark.django_db
def test_employment_invalid_date_from_with_valid_job_type(login, user_student, student_employment,
                                                          job_type_objects_date_from):
    login(user_student)
    data, errors = student_employment(user_student, job_type_objects_date_from[0], '1337.1337',
                                      None, Branch(id=1337))
    assert errors is None
    assert data is not None
    assert data.get('studentProfileEmployment') is not None

    errors = data.get('studentProfileEmployment').get('errors')
    assert errors is not None
    assert 'jobFromDate' in errors
    assert 'branch' in errors
