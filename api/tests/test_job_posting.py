import pytest
from django.contrib.auth.models import AnonymousUser

from db.models import JobPosting, JobPostingState


@pytest.mark.django_db
def test_job_posting(query_job_posting, job_posting_object: JobPosting, job_type_objects, branch_objects,
                     company_object, job_requirement_objects, skill_objects, user_employee):
    job_posting_object.title = 'title'
    job_posting_object.slug = 'title'
    job_posting_object.description = 'description'
    job_posting_object.job_type = job_type_objects[0]
    job_posting_object.branch = branch_objects[0]
    job_posting_object.workload = 80
    job_posting_object.company = company_object
    job_posting_object.job_from_date = '2021-08-01'
    job_posting_object.job_to_date = '2021-10-01'
    job_posting_object.url = 'http://www.url.lo'
    job_posting_object.job_requirements.set(job_requirement_objects)
    job_posting_object.skills.set(skill_objects)
    job_posting_object.form_step = 4
    job_posting_object.state = JobPostingState.PUBLIC
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()

    data, errors = query_job_posting(user_employee, 'title')

    assert errors is None
    assert data is not None
    job_posting = data.get('jobPosting')

    assert job_posting.get('title') == job_posting_object.title
    assert job_posting.get('slug') == job_posting_object.slug
    assert job_posting.get('description') == job_posting_object.description
    assert int(job_posting.get('jobType').get('id')) == job_posting_object.job_type_id
    assert int(job_posting.get('branch').get('id')) == job_posting_object.branch_id
    assert job_posting.get('workload') == job_posting_object.workload
    assert int(job_posting.get('company').get('id')) == job_posting_object.company_id
    assert job_posting.get('jobFromDate') == '2021-08-01'
    assert job_posting.get('jobToDate') == '2021-10-01'
    assert job_posting.get('url') == job_posting_object.url
    assert len(job_posting.get('jobRequirements')) == len(job_requirement_objects)
    assert len(job_posting.get('skills')) == len(skill_objects)
    assert int(job_posting.get('formStep')) == job_posting_object.form_step
    assert job_posting.get('state') == job_posting_object.state.upper()
    assert int(job_posting.get('employee').get('id')) == user_employee.employee.id


@pytest.mark.django_db
def test_job_posting_is_draft_but_accessible_for_employee(login, query_job_posting, job_posting_object: JobPosting,
                                                          job_type_objects, branch_objects, company_object,
                                                          job_requirement_objects, skill_objects, user_employee):
    job_posting_object.title = 'title'
    job_posting_object.slug = 'title'
    job_posting_object.description = 'description'
    job_posting_object.job_type = job_type_objects[0]
    job_posting_object.branch = branch_objects[0]
    job_posting_object.workload = 80
    job_posting_object.company = company_object
    job_posting_object.job_from_date = '2021-08-01'
    job_posting_object.job_to_date = '2021-10-01'
    job_posting_object.url = 'http://www.url.lo'
    job_posting_object.job_requirements.set(job_requirement_objects)
    job_posting_object.skills.set(skill_objects)
    job_posting_object.form_step = 4
    job_posting_object.state = JobPostingState.DRAFT
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()

    login(user_employee)

    data, errors = query_job_posting(user_employee, 'title')

    assert errors is None
    assert data is not None
    job_posting = data.get('jobPosting')

    assert job_posting.get('title') == job_posting_object.title
    assert job_posting.get('slug') == job_posting_object.slug
    assert job_posting.get('description') == job_posting_object.description
    assert int(job_posting.get('jobType').get('id')) == job_posting_object.job_type_id
    assert int(job_posting.get('branch').get('id')) == job_posting_object.branch_id
    assert job_posting.get('workload') == job_posting_object.workload
    assert int(job_posting.get('company').get('id')) == job_posting_object.company_id
    assert job_posting.get('jobFromDate') == '2021-08-01'
    assert job_posting.get('jobToDate') == '2021-10-01'
    assert job_posting.get('url') == job_posting_object.url
    assert len(job_posting.get('jobRequirements')) == len(job_requirement_objects)
    assert len(job_posting.get('skills')) == len(skill_objects)
    assert int(job_posting.get('formStep')) == job_posting_object.form_step
    assert job_posting.get('state') == job_posting_object.state.upper()
    assert int(job_posting.get('employee').get('id')) == user_employee.employee.id


@pytest.mark.django_db
def test_job_posting_without_login(query_job_posting, job_posting_object: JobPosting,  company_object, user_employee):
    job_posting_object.title = 'title'
    job_posting_object.slug = 'title'
    job_posting_object.company = company_object
    job_posting_object.state = JobPostingState.DRAFT
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()

    data, errors = query_job_posting(AnonymousUser(), 'title')

    assert errors is not None
    assert data is not None
    assert data.get('jobPosting') is None


@pytest.mark.django_db
def test_job_posting_is_draft(login, query_job_posting, job_posting_object: JobPosting,  company_object, user_employee,
                              user_student):
    job_posting_object.title = 'title'
    job_posting_object.slug = 'title'
    job_posting_object.company = company_object
    job_posting_object.state = JobPostingState.DRAFT
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()

    login(user_student)

    data, errors = query_job_posting(user_student, 'title')

    assert errors is not None
    assert data is not None
    assert data.get('jobPosting') is None


@pytest.mark.django_db
def test_job_postings(query_job_postings, job_posting_objects, company_object, user_employee):

    for job_posting_object in job_posting_objects:
        job_posting_object.company = company_object
        job_posting_object.state = JobPostingState.PUBLIC
        job_posting_object.employee = user_employee.employee
        job_posting_object.save()

    job_posting_objects[0].state = JobPostingState.DRAFT
    job_posting_objects[0].save()

    data, errors = query_job_postings(user_employee, user_employee.company.slug)

    assert errors is None
    assert data is not None
    job_postings = data.get('jobPostings')

    assert job_postings is not None
    assert len(job_postings) == len(job_posting_objects) - 1