import pytest
from django.contrib.auth.models import AnonymousUser

from db.helper.forms import convert_date
from db.models import JobPosting, JobType, Branch

# pylint: disable=R0913


@pytest.mark.django_db
def test_step_1(requests_mock, user_employee, login, job_posting_step_1, job_type_objects, branch_objects):
    requests_mock.head('http://www.job-posting.lo/', text='data', headers={'Content-Type': 'text/html'})
    login(user_employee)
    data, errors = job_posting_step_1(user_employee, 'title', 'description', job_type_objects[0], branch_objects[0],
                                      100, '03.2021', '05.2021', 'www.job-posting.lo')
    assert errors is None
    assert data is not None
    assert data.get('jobPostingStep1') is not None
    assert data.get('jobPostingStep1').get('success')

    job_posting_slug = JobPosting.objects.get(slug=data.get('jobPostingStep1').get('slug'))
    job_posting = JobPosting.objects.get(pk=data.get('jobPostingStep1').get('jobPostingId'))
    assert job_posting_slug == job_posting
    assert job_posting.title == 'title'
    assert job_posting.slug == f'title-{str(job_posting.id)}'
    assert job_posting.description == 'description'
    assert job_posting.job_type == job_type_objects[0]
    assert job_posting.branch == branch_objects[0]
    assert job_posting.workload == 100
    assert job_posting.job_from_date == convert_date('03.2021', '%m.%Y')
    assert job_posting.job_to_date == convert_date('05.2021', '%m.%Y')
    assert job_posting.url == 'http://www.job-posting.lo'
    assert job_posting.form_step == 2


@pytest.mark.django_db
def test_step_1_without_login(job_posting_step_1, job_type_objects, branch_objects):
    data, errors = job_posting_step_1(AnonymousUser(), 'title', 'description', job_type_objects[0], branch_objects[0],
                                      100, '03.2021', '05.2021', 'www.job-posting.lo')
    assert errors is not None
    assert data is not None
    assert data.get('jobPostingStep1') is None


@pytest.mark.django_db
def test_step_1_as_student(user_student, login, job_posting_step_1, job_type_objects, branch_objects):
    login(user_student)
    data, errors = job_posting_step_1(user_student, 'title', 'description', job_type_objects[0], branch_objects[0], 100,
                                      '03.2021', '05.2021', 'www.job-posting.lo')
    assert errors is None
    assert data is not None
    assert data.get('jobPostingStep1') is not None
    assert data.get('jobPostingStep1').get('slug') is None

    errors = data.get('jobPostingStep1').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_step_1_with_invalid_data(requests_mock, user_employee, login, job_posting_step_1):
    requests_mock.head('http://www.job-posting.lo/', text='data', headers={'Content-Type': 'application/pdf'})
    login(user_employee)
    data, errors = job_posting_step_1(user_employee, '', '', JobType(id=1337), Branch(id=1337), 1000, '78.2021',
                                      '29.201', 'www.job-posting.lo')
    assert errors is None
    assert data is not None
    assert data.get('jobPostingStep1') is not None
    assert data.get('jobPostingStep1').get('success') is False
    assert data.get('jobPostingStep1').get('slug') is None

    errors = data.get('jobPostingStep1').get('errors')
    assert errors is not None
    assert 'title' in errors
    assert 'description' in errors
    assert 'jobType' in errors
    assert 'branch' in errors
    assert 'workload' in errors
    assert 'jobFromDate' in errors
    assert 'jobToDate' in errors
    assert 'url' in errors


@pytest.mark.django_db
def test_step_1_with_invalid_date_range(requests_mock, user_employee, login, job_posting_step_1, job_type_objects,
                                        branch_objects):
    requests_mock.head('http://www.job-posting.lo/', text='data', headers={'Content-Type': 'text/html'})
    login(user_employee)
    data, errors = job_posting_step_1(user_employee, 'title', 'description', job_type_objects[0], branch_objects[0],
                                      100, '03.2021', '01.2021', 'www.job-posting.lo')
    assert errors is None
    assert data is not None
    assert data.get('jobPostingStep1') is not None
    assert data.get('jobPostingStep1').get('success') is False
    assert data.get('jobPostingStep1').get('slug') is None

    errors = data.get('jobPostingStep1').get('errors')
    assert errors is not None
    assert 'jobToDate' in errors
