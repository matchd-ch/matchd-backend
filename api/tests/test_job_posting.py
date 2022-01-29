import pytest

from django.contrib.auth.models import AnonymousUser

from graphql_relay import to_global_id

from api.tests.helpers.node_helper import assert_node_field, assert_node_id

from db.models import JobPosting, JobPostingState, JobPostingLanguageRelation, Match


# pylint: disable=R0913
@pytest.mark.django_db
def test_job_posting(query_job_posting, job_posting_object: JobPosting, job_type_objects, branch_objects,
                     company_object, job_requirement_objects, skill_objects, user_employee, language_objects,
                     language_level_objects, user_student):
    job_posting_object.title = 'title'
    job_posting_object.slug = 'title'
    job_posting_object.description = 'description'
    job_posting_object.job_type = job_type_objects[0]
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
    JobPostingLanguageRelation.objects.create(job_posting=job_posting_object, language=language_objects[0],
                                              language_level=language_level_objects[0])
    job_posting_object.branches.set([branch_objects[0]])

    data, errors = query_job_posting(user_student, 'title')

    assert errors is None
    assert data is not None
    job_posting = data.get('jobPosting')

    assert job_posting.get('title') == 'title'
    assert job_posting.get('displayTitle') == 'tit\xadle'
    assert job_posting.get('slug') == job_posting_object.slug
    assert job_posting.get('description') == job_posting_object.description
    assert job_posting.get('jobType').get('id') == to_global_id(
        'JobType', job_posting_object.job_type_id
    )
    assert job_posting.get('branches')[0].get('id') == to_global_id(
        'Branch', job_posting_object.branches.all()[0].id
    )
    assert job_posting.get('workload') == job_posting_object.workload
    assert job_posting.get('company').get('id') == to_global_id(
        'Company', job_posting_object.company_id
    )
    assert job_posting.get('jobFromDate') == '2021-08-01'
    assert job_posting.get('jobToDate') == '2021-10-01'
    assert job_posting.get('url') == job_posting_object.url
    assert len(job_posting.get('jobRequirements').get('edges')) == len(job_requirement_objects)
    assert job_posting.get('skills') is None  # skills should not be visible
    assert job_posting.get('languages') is None  # languages should not be visible
    assert int(job_posting.get('formStep')) == job_posting_object.form_step
    assert job_posting.get('state') == job_posting_object.state.upper()
    assert job_posting.get('employee').get('id') == to_global_id('Employee', user_employee.employee.id)

    match_status = job_posting.get('matchStatus')
    assert match_status is None

    match_hints = job_posting.get('matchHints')
    assert match_hints is not None
    assert match_hints.get('hasConfirmedMatch') is False
    assert match_hints.get('hasRequestedMatch') is False


# pylint: disable=R0913
@pytest.mark.django_db
def test_job_posting_as_employee(query_job_posting, job_posting_object: JobPosting, job_type_objects, branch_objects,
                                 company_object, job_requirement_objects, skill_objects, user_employee,
                                 language_objects, language_level_objects):
    job_posting_object.title = 'title'
    job_posting_object.slug = 'title'
    job_posting_object.description = 'description'
    job_posting_object.job_type = job_type_objects[0]
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
    JobPostingLanguageRelation.objects.create(job_posting=job_posting_object, language=language_objects[0],
                                              language_level=language_level_objects[0])
    job_posting_object.branches.set([branch_objects[0]])

    data, errors = query_job_posting(user_employee, 'title')

    assert errors is None
    assert data is not None
    job_posting = data.get('jobPosting')

    assert job_posting.get('title') == 'title'
    assert job_posting.get('displayTitle') == 'tit\xadle'
    assert job_posting.get('slug') == job_posting_object.slug
    assert job_posting.get('description') == job_posting_object.description
    assert job_posting.get('jobType').get('id') == to_global_id(
        'JobType', job_posting_object.job_type_id
    )
    assert job_posting.get('branches')[0].get('id') == to_global_id(
        'Branch', job_posting_object.branches.all()[0].id
    )
    assert job_posting.get('workload') == job_posting_object.workload
    assert job_posting.get('company').get('id') == to_global_id(
        'Company', job_posting_object.company_id
    )
    assert job_posting.get('jobFromDate') == '2021-08-01'
    assert job_posting.get('jobToDate') == '2021-10-01'
    assert job_posting.get('url') == job_posting_object.url
    assert len(job_posting.get('jobRequirements').get('edges')) == len(job_requirement_objects)
    assert len(job_posting.get('skills')) == len(skill_objects)
    assert len(job_posting.get('languages')) == 1
    assert int(job_posting.get('formStep')) == job_posting_object.form_step
    assert job_posting.get('state') == job_posting_object.state.upper()
    assert job_posting.get('employee').get('id') == to_global_id('Employee', user_employee.employee.id)

    match_status = job_posting.get('matchStatus')
    assert match_status is None

    match_hints = job_posting.get('matchHints')
    assert match_hints is None


@pytest.mark.django_db
def test_job_posting_by_id(query_job_posting_by_id, job_posting_object: JobPosting, job_type_objects, branch_objects,
                           company_object, job_requirement_objects, skill_objects, user_employee, language_objects,
                           language_level_objects, user_student):
    job_posting_object.title = 'title'
    job_posting_object.slug = 'title'
    job_posting_object.description = 'description'
    job_posting_object.job_type = job_type_objects[0]
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
    JobPostingLanguageRelation.objects.create(job_posting=job_posting_object, language=language_objects[0],
                                              language_level=language_level_objects[0])
    job_posting_object.branches.set([branch_objects[0]])

    data, errors = query_job_posting_by_id(user_student, job_posting_object.id)

    assert errors is None
    assert data is not None
    job_posting = data.get('jobPosting')

    assert job_posting.get('title') == 'title'
    assert job_posting.get('displayTitle') == 'tit\xadle'
    assert job_posting.get('slug') == job_posting_object.slug
    assert job_posting.get('description') == job_posting_object.description
    assert job_posting.get('jobType').get('id') == to_global_id(
        'JobType', job_posting_object.job_type_id
    )
    assert job_posting.get('branches')[0].get('id') == to_global_id(
        'Branch', job_posting_object.branches.all()[0].id
    )
    assert job_posting.get('workload') == job_posting_object.workload
    assert job_posting.get('company').get('id') == to_global_id(
        'Company', job_posting_object.company_id
    )
    assert job_posting.get('jobFromDate') == '2021-08-01'
    assert job_posting.get('jobToDate') == '2021-10-01'
    assert job_posting.get('url') == job_posting_object.url
    assert len(job_posting.get('jobRequirements').get('edges')) == len(job_requirement_objects)
    assert job_posting.get('skills') is None  # skills should not be visible
    assert job_posting.get('languages') is None  # languages should not be visible
    assert int(job_posting.get('formStep')) == job_posting_object.form_step
    assert job_posting.get('state') == job_posting_object.state.upper()
    assert job_posting.get('employee').get('id') == to_global_id(
        'Employee', user_employee.employee.id
    )

    match_status = job_posting.get('matchStatus')
    assert match_status is None

    match_hints = job_posting.get('matchHints')
    assert match_hints is not None
    assert match_hints.get('hasConfirmedMatch') is False
    assert match_hints.get('hasRequestedMatch') is False


@pytest.mark.django_db
def test_job_posting_is_draft_but_accessible_for_employee(login, query_job_posting, job_posting_object: JobPosting,
                                                          job_type_objects, branch_objects, company_object,
                                                          job_requirement_objects, skill_objects, user_employee):
    job_posting_object.title = 'title'
    job_posting_object.slug = 'title'
    job_posting_object.description = 'description'
    job_posting_object.job_type = job_type_objects[0]
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
    job_posting_object.branches.set([branch_objects[0]])

    login(user_employee)

    data, errors = query_job_posting(user_employee, 'title')

    assert errors is None
    assert data is not None
    job_posting = data.get('jobPosting')

    assert job_posting.get('title') == 'title'
    assert job_posting.get('displayTitle') == 'tit\xadle'
    assert job_posting.get('slug') == job_posting_object.slug
    assert job_posting.get('description') == job_posting_object.description
    assert job_posting.get('jobType').get('id') == to_global_id(
        'JobType', job_posting_object.job_type_id
    )
    assert job_posting.get('branches')[0].get('id') == to_global_id(
        'Branch', job_posting_object.branches.all()[0].id
    )
    assert job_posting.get('workload') == job_posting_object.workload
    assert job_posting.get('company').get('id') == to_global_id(
        'Company', job_posting_object.company_id
    )
    assert job_posting.get('jobFromDate') == '2021-08-01'
    assert job_posting.get('jobToDate') == '2021-10-01'
    assert job_posting.get('url') == job_posting_object.url
    assert len(job_posting.get('jobRequirements').get('edges')) == len(job_requirement_objects)
    assert len(job_posting.get('skills')) == len(skill_objects)
    assert len(job_posting.get('languages')) == 0
    assert int(job_posting.get('formStep')) == job_posting_object.form_step
    assert job_posting.get('state') == job_posting_object.state.upper()
    assert job_posting.get('employee').get('id') == to_global_id(
        'Employee', user_employee.employee.id
    )

    match_status = job_posting.get('matchStatus')
    assert match_status is None

    match_hints = job_posting.get('matchHints')
    assert match_hints is None


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
    edges = data.get('jobPostings').get('edges')

    assert edges is not None
    assert_node_id(edges[0].get('node'), 'JobPosting', job_posting_objects[1].id)
    assert_node_id(edges[1].get('node'), 'JobPosting', job_posting_objects[2].id)
    assert_node_field(edges[0].get('node'), 'slug', job_posting_objects[1].slug)
    assert_node_field(edges[1].get('node'), 'slug', job_posting_objects[2].slug)
    assert len(edges) == len(job_posting_objects) - 1


@pytest.mark.django_db
def test_job_posting_node_query(query_job_posting_node, job_posting_objects, user_employee):
    data, errors = query_job_posting_node(user_employee, job_posting_objects[1].id)

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, 'JobPosting', job_posting_objects[1].id)
    assert_node_field(node, 'slug', job_posting_objects[1].slug)


@pytest.mark.django_db
def test_job_posting_node_without_login_query(query_job_posting_node, job_posting_objects):
    data, errors = query_job_posting_node(AnonymousUser(), job_posting_objects[1].id)

    assert errors is not None
    assert data is not None

    error = errors[0].get('message')
    node = data.get('node')
    assert node is None
    assert error == "You do not have permission to perform this action"


@pytest.mark.django_db
def test_job_posting_with_match_status_initiated_by_employee(login, query_job_posting, job_posting_object: JobPosting,
                                                             user_employee, user_student):
    job_posting_object.title = 'title'
    job_posting_object.slug = 'title'
    job_posting_object.form_step = 4
    job_posting_object.state = JobPostingState.PUBLIC
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()

    Match.objects.create(job_posting=job_posting_object, student=user_student.student,
                         initiator=user_employee.type, company_confirmed=True, student_confirmed=True)

    login(user_student)
    data, errors = query_job_posting(user_student, 'title')

    assert errors is None
    assert data is not None
    job_posting = data.get('jobPosting')

    match_status = job_posting.get('matchStatus')
    assert match_status is not None
    assert match_status.get('initiator') == user_employee.type.upper()
    assert match_status.get('confirmed') is True

    match_hints = job_posting.get('matchHints')
    assert match_hints is not None
    assert match_hints.get('hasConfirmedMatch') is True
    assert match_hints.get('hasRequestedMatch') is False


@pytest.mark.django_db
def test_job_posting_with_match_status_initiated_by_student(login, query_job_posting, job_posting_object: JobPosting,
                                                             user_employee, user_student):
    job_posting_object.title = 'title'
    job_posting_object.slug = 'title'
    job_posting_object.form_step = 4
    job_posting_object.state = JobPostingState.PUBLIC
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()

    Match.objects.create(job_posting=job_posting_object, student=user_student.student,
                         initiator=user_student.type, student_confirmed=True)

    login(user_student)
    data, errors = query_job_posting(user_student, 'title')

    assert errors is None
    assert data is not None
    job_posting = data.get('jobPosting')

    match_status = job_posting.get('matchStatus')
    assert match_status is not None
    assert match_status.get('initiator') == user_student.type.upper()
    assert match_status.get('confirmed') is False

    match_hints = job_posting.get('matchHints')
    assert match_hints is not None
    assert match_hints.get('hasConfirmedMatch') is False
    assert match_hints.get('hasRequestedMatch') is True


@pytest.mark.django_db
def test_job_posting_with_match_status_initiated_by_student_on_other_job_posting(
        login, query_job_posting, job_posting_object: JobPosting, job_posting_object_2, user_employee, user_student):
    job_posting_object.title = 'title'
    job_posting_object.slug = 'title'
    job_posting_object.form_step = 4
    job_posting_object.state = JobPostingState.PUBLIC
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()

    Match.objects.create(job_posting=job_posting_object_2, student=user_student.student,
                         initiator=user_student.type, student_confirmed=True)

    login(user_student)
    data, errors = query_job_posting(user_student, 'title')

    assert errors is None
    assert data is not None
    job_posting = data.get('jobPosting')

    match_status = job_posting.get('matchStatus')
    assert match_status is None

    match_hints = job_posting.get('matchHints')
    assert match_hints is not None
    assert match_hints.get('hasConfirmedMatch') is False
    assert match_hints.get('hasRequestedMatch') is True
