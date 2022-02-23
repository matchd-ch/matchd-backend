from graphql_relay import from_global_id
import pytest

from django.contrib.auth.models import AnonymousUser

from db.models import JobPosting, JobPostingState, Employee


@pytest.mark.django_db
def test_allocation(user_employee, job_posting_object, login, job_posting_allocation):
    login(user_employee)
    job_posting_object.form_step = 3
    job_posting_object.state = JobPostingState.DRAFT
    job_posting_object.save()
    data, errors = job_posting_allocation(user_employee, job_posting_object.id,
                                          JobPostingState.PUBLIC, user_employee.employee)
    assert errors is None
    assert data is not None
    assert data.get('jobPostingAllocation') is not None
    assert data.get('jobPostingAllocation').get('success')

    slug = data.get('jobPostingAllocation').get('slug')
    element_id = from_global_id(data.get('jobPostingAllocation').get('jobPostingId'))[1]

    job_posting_slug = JobPosting.objects.get(slug=slug)
    job_posting = JobPosting.objects.get(pk=element_id)
    assert job_posting_slug == job_posting
    assert job_posting.employee.id == user_employee.employee.id
    assert job_posting.state == JobPostingState.PUBLIC
    assert job_posting.date_published is not None
    assert job_posting.form_step == 4


@pytest.mark.django_db
def test_allocation_with_invalid_job_posting_id(user_employee, login, job_posting_allocation):
    login(user_employee)
    data, errors = job_posting_allocation(user_employee, 1337, JobPostingState.PUBLIC,
                                          user_employee.employee)
    assert errors is not None
    assert data is not None
    assert data.get('jobPostingAllocation') is None


@pytest.mark.django_db
def test_allocation_without_login(user_employee, job_posting_object, job_posting_allocation):
    data, errors = job_posting_allocation(AnonymousUser(), job_posting_object.id,
                                          JobPostingState.PUBLIC, user_employee.employee)
    assert errors is not None
    assert data is not None
    assert data.get('jobPostingAllocation') is None


@pytest.mark.django_db
def test_allocation_as_student(user_student, login, user_employee, job_posting_object,
                               job_posting_allocation):
    login(user_student)
    data, errors = job_posting_allocation(user_student, job_posting_object.id,
                                          JobPostingState.PUBLIC, user_employee.employee)
    assert errors is None
    assert data is not None
    assert data.get('jobPostingAllocation') is not None
    assert data.get('jobPostingAllocation').get('slug') is None

    errors = data.get('jobPostingAllocation').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_allocation_as_employee_from_another_company(user_employee_2, job_posting_object, login,
                                                     job_posting_allocation):
    login(user_employee_2)
    job_posting_object.form_step = 3
    job_posting_object.save()
    data, errors = job_posting_allocation(user_employee_2, job_posting_object.id,
                                          JobPostingState.PUBLIC, user_employee_2.employee)
    assert errors is None
    assert data is not None
    assert data.get('jobPostingAllocation') is not None
    assert data.get('jobPostingAllocation').get('success') is False
    assert data.get('jobPostingAllocation').get('slug') is None

    errors = data.get('jobPostingAllocation').get('errors')
    assert errors is not None
    assert 'employee' in errors


@pytest.mark.django_db
def test_allocation_with_invalid_data(user_employee, job_posting_object, login,
                                      job_posting_allocation):
    login(user_employee)
    job_posting_object.form_step = 3
    job_posting_object.save()
    data, errors = job_posting_allocation(user_employee, job_posting_object.id, 'invalid',
                                          Employee(id=1337))
    assert errors is None
    assert data is not None
    assert data.get('jobPostingAllocation') is not None
    assert data.get('jobPostingAllocation').get('success') is False

    errors = data.get('jobPostingAllocation').get('errors')
    assert errors is not None
    assert 'state' in errors
    assert 'employee' in errors

    job_posting = JobPosting.objects.get(pk=job_posting_object.id)
    assert job_posting.form_step == 3


@pytest.mark.django_db
def test_allocation_with_invalid_step(user_employee, job_posting_object, login,
                                      job_posting_allocation):
    login(user_employee)
    job_posting_object.form_step = 1
    job_posting_object.save()
    data, errors = job_posting_allocation(user_employee, job_posting_object.id,
                                          JobPostingState.PUBLIC, user_employee.employee)
    assert errors is None
    assert data is not None
    assert data.get('jobPostingAllocation') is not None
    assert data.get('jobPostingAllocation').get('success') is False

    errors = data.get('jobPostingAllocation').get('errors')
    assert errors is not None
    assert 'jobPostingStep' in errors
