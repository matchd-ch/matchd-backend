import pytest
from django.contrib.auth.models import AnonymousUser

from db.models import JobPosting, ProfileState, Employee


@pytest.mark.django_db
def test_step_3(user_employee, job_posting_object, login, job_posting_step_3):
    login(user_employee)
    job_posting_object.form_step = 3
    job_posting_object.save()
    data, errors = job_posting_step_3(user_employee, job_posting_object.id, ProfileState.PUBLIC, user_employee.employee)
    assert errors is None
    assert data is not None
    assert data.get('jobPostingStep3') is not None
    assert data.get('jobPostingStep3').get('success')

    job_posting = JobPosting.objects.get(slug=data.get('jobPostingStep3').get('slug'))
    assert job_posting.employee.id == user_employee.employee.id
    assert job_posting.state == ProfileState.PUBLIC
    assert job_posting.form_step == 4


@pytest.mark.django_db
def test_step_3_with_invalid_job_posting_id(user_employee, login, job_posting_step_3):
    login(user_employee)
    data, errors = job_posting_step_3(user_employee, 1337, ProfileState.PUBLIC, user_employee.employee)
    assert errors is not None
    assert data is not None
    assert data.get('jobPostingStep3') is None


@pytest.mark.django_db
def test_step_3_without_login(user_employee, job_posting_object, job_posting_step_3):
    data, errors = job_posting_step_3(AnonymousUser(), job_posting_object.id, ProfileState.PUBLIC,
                                      user_employee.employee)
    assert errors is not None
    assert data is not None
    assert data.get('jobPostingStep3') is None


@pytest.mark.django_db
def test_step_3_as_student(user_student, login, user_employee, job_posting_object, job_posting_step_3):
    login(user_student)
    data, errors = job_posting_step_3(user_student, job_posting_object.id, ProfileState.PUBLIC, user_employee.employee)
    assert errors is None
    assert data is not None
    assert data.get('jobPostingStep3') is not None
    assert data.get('jobPostingStep3').get('slug') is None

    errors = data.get('jobPostingStep3').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_step_3_as_employee_from_another_company(user_employee_2, job_posting_object, login, job_posting_step_3):
    login(user_employee_2)
    job_posting_object.form_step = 3
    job_posting_object.save()
    data, errors = job_posting_step_3(user_employee_2, job_posting_object.id, ProfileState.PUBLIC,
                                      user_employee_2.employee)
    assert errors is None
    assert data is not None
    assert data.get('jobPostingStep3') is not None
    assert data.get('jobPostingStep3').get('success') is False
    assert data.get('jobPostingStep3').get('slug') is None

    errors = data.get('jobPostingStep3').get('errors')
    assert errors is not None
    assert 'employee' in errors


@pytest.mark.django_db
def test_step_3_with_invalid_data(user_employee, job_posting_object, login, job_posting_step_3):
    login(user_employee)
    job_posting_object.form_step = 3
    job_posting_object.save()
    data, errors = job_posting_step_3(user_employee, job_posting_object.id, 'invalid', Employee(id=1337))
    assert errors is None
    assert data is not None
    assert data.get('jobPostingStep3') is not None
    assert data.get('jobPostingStep3').get('success') is False

    errors = data.get('jobPostingStep3').get('errors')
    assert errors is not None
    assert 'state' in errors
    assert 'employee' in errors

    job_posting = JobPosting.objects.get(pk=job_posting_object.id)
    assert job_posting.form_step == 3


@pytest.mark.django_db
def test_step_3_with_invalid_step(user_employee, job_posting_object, login, job_posting_step_3):
    login(user_employee)
    job_posting_object.form_step = 1
    job_posting_object.save()
    data, errors = job_posting_step_3(user_employee, job_posting_object.id, ProfileState.PUBLIC, user_employee.employee)
    assert errors is None
    assert data is not None
    assert data.get('jobPostingStep3') is not None
    assert data.get('jobPostingStep3').get('success') is False

    errors = data.get('jobPostingStep3').get('errors')
    assert errors is not None
    assert 'jobPostingStep' in errors
