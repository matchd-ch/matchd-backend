import pytest

from graphql_relay import from_global_id

from django.contrib.auth.models import AnonymousUser

from db.helper.forms import convert_date
from db.models import JobPosting, JobType, Branch

# pylint: disable=R0913


@pytest.mark.django_db
def test_base_data(requests_mock, user_employee, login, job_posting_base_data, job_type_objects,
                   branch_objects):
    requests_mock.head('https://google.com/', text='data', headers={'Content-Type': 'text/html'})
    login(user_employee)
    data, errors = job_posting_base_data(user_employee, 'title', 'description', job_type_objects[0],
                                         [branch_objects[0]], 80, 100, '03.2021', '05.2021',
                                         'https://google.com')
    assert errors is None
    assert data is not None
    assert data.get('jobPostingBaseData') is not None
    assert data.get('jobPostingBaseData').get('success')

    slug = data.get('jobPostingBaseData').get('slug')
    element_id = from_global_id(data.get('jobPostingBaseData').get('jobPostingId'))[1]

    job_posting_slug = JobPosting.objects.get(slug=slug)
    job_posting = JobPosting.objects.get(pk=element_id)
    assert job_posting_slug == job_posting
    assert job_posting.title == 'title'
    assert job_posting.slug == f'title-{str(job_posting.id)}'
    assert job_posting.description == 'description'
    assert job_posting.job_type == job_type_objects[0]
    assert job_posting.branches.all()[0] == branch_objects[0]
    assert job_posting.workload_from == 80
    assert job_posting.workload_to == 100
    assert job_posting.job_from_date == convert_date('03.2021', '%m.%Y')
    assert job_posting.job_to_date == convert_date('05.2021', '%m.%Y')
    assert job_posting.url == 'https://google.com'
    assert job_posting.form_step == 2


@pytest.mark.django_db
def test_base_data_without_login(job_posting_base_data, job_type_objects, branch_objects):
    data, errors = job_posting_base_data(AnonymousUser(), 'title', 'description',
                                         job_type_objects[0], [branch_objects[0]], 80, 100,
                                         '03.2021', '05.2021', 'https://google.com')
    assert errors is not None
    assert data is not None
    assert data.get('jobPostingBaseData') is None


@pytest.mark.django_db
def test_base_data_as_student(user_student, login, job_posting_base_data, job_type_objects,
                              branch_objects):
    login(user_student)
    data, errors = job_posting_base_data(user_student, 'title', 'description', job_type_objects[0],
                                         [branch_objects[0]], 80, 100, '03.2021', '05.2021',
                                         'https://google.com')
    assert errors is None
    assert data is not None
    assert data.get('jobPostingBaseData') is not None
    assert data.get('jobPostingBaseData').get('slug') is None

    errors = data.get('jobPostingBaseData').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_base_data_with_invalid_data(requests_mock, user_employee, login, job_posting_base_data):
    login(user_employee)
    data, errors = job_posting_base_data(user_employee, '', '', JobType(id=1337), [Branch(id=1337)],
                                         0, 1000, '78.2021', '29.201', 'https://google.com')
    assert errors is None
    assert data is not None
    assert data.get('jobPostingBaseData') is not None
    assert data.get('jobPostingBaseData').get('success') is False
    assert data.get('jobPostingBaseData').get('slug') is None

    errors = data.get('jobPostingBaseData').get('errors')
    assert errors is not None
    assert 'title' in errors
    assert 'description' not in errors
    assert 'jobType' in errors
    assert 'branches' in errors
    assert 'workloadFrom' in errors
    assert 'workloadTo' in errors
    assert 'jobFromDate' in errors
    assert 'jobToDate' in errors
    assert 'url' in errors


@pytest.mark.django_db
def test_base_data_with_invalid_date_range(requests_mock, user_employee, login,
                                           job_posting_base_data, job_type_objects, branch_objects):
    requests_mock.head('https://google.com/', text='data', headers={'Content-Type': 'text/html'})
    login(user_employee)
    data, errors = job_posting_base_data(user_employee, 'title', 'description', job_type_objects[0],
                                         [branch_objects[0]], 80, 100, '03.2021', '01.2021',
                                         'https://google.com')
    assert errors is None
    assert data is not None
    assert data.get('jobPostingBaseData') is not None
    assert data.get('jobPostingBaseData').get('success') is False
    assert data.get('jobPostingBaseData').get('slug') is None

    errors = data.get('jobPostingBaseData').get('errors')
    assert errors is not None
    assert 'jobToDate' in errors


@pytest.mark.django_db
def test_base_data_with_only_to_date(requests_mock, user_employee, login, job_posting_base_data,
                                     job_type_objects, branch_objects):
    requests_mock.head('https://google.com/', text='data', headers={'Content-Type': 'text/html'})
    login(user_employee)
    data, errors = job_posting_base_data(user_employee, 'title', 'description', job_type_objects[0],
                                         [branch_objects[0]], 80, 100, None, '05.2021',
                                         'https://google.com')
    assert errors is None
    assert data is not None
    assert data.get('jobPostingBaseData') is not None
    assert data.get('jobPostingBaseData').get('success')

    element_id = from_global_id(data.get('jobPostingBaseData').get('jobPostingId'))[1]

    job_posting = JobPosting.objects.get(pk=element_id)
    assert job_posting.job_from_date is None
    assert job_posting.job_to_date == convert_date('05.2021', '%m.%Y')


@pytest.mark.django_db
def test_base_data_with_only_from_date(requests_mock, user_employee, login, job_posting_base_data,
                                       job_type_objects, branch_objects):
    requests_mock.head('https://google.com/', text='data', headers={'Content-Type': 'text/html'})
    login(user_employee)
    data, errors = job_posting_base_data(user_employee, 'title', 'description', job_type_objects[0],
                                         [branch_objects[0]], 80, 100, '05.2021', None,
                                         'https://google.com')
    assert errors is None
    assert data is not None
    assert data.get('jobPostingBaseData') is not None
    assert data.get('jobPostingBaseData').get('success')

    element_id = from_global_id(data.get('jobPostingBaseData').get('jobPostingId'))[1]

    job_posting = JobPosting.objects.get(pk=element_id)
    assert job_posting.job_from_date == convert_date('05.2021', '%m.%Y')
    assert job_posting.job_to_date is None


@pytest.mark.django_db
def test_base_data_with_job_period_by_agreement(requests_mock, user_employee, login,
                                                job_posting_base_data, job_type_objects,
                                                branch_objects):
    requests_mock.head('https://google.com/', text='data', headers={'Content-Type': 'text/html'})
    login(user_employee)
    data, errors = job_posting_base_data(user_employee, 'title', 'description', job_type_objects[0],
                                         [branch_objects[0]], 80, 100, None, None,
                                         'https://google.com')
    assert errors is None
    assert data is not None
    assert data.get('jobPostingBaseData') is not None
    assert data.get('jobPostingBaseData').get('success')

    element_id = from_global_id(data.get('jobPostingBaseData').get('jobPostingId'))[1]

    job_posting = JobPosting.objects.get(pk=element_id)
    assert job_posting.job_from_date is None
    assert job_posting.job_to_date is None


@pytest.mark.django_db
def test_base_data_with_workload_from_greated_than_workload_to_fails(requests_mock, user_employee,
                                                                     login, job_posting_base_data,
                                                                     job_type_objects,
                                                                     branch_objects):
    requests_mock.head('https://google.com/', text='data', headers={'Content-Type': 'text/html'})
    login(user_employee)
    data, errors = job_posting_base_data(user_employee, 'title', 'description', job_type_objects[0],
                                         [branch_objects[0]], 20, 10, '03.2021', '01.2023',
                                         'https://google.com')

    errors = data.get('jobPostingBaseData').get('errors')

    assert errors is not None
    assert 'workloadTo' in errors
