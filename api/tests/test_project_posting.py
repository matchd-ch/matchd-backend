import pytest

from django.contrib.auth.models import AnonymousUser

from graphql_relay import to_global_id

from api.tests.helper.node_helper import assert_node_field, assert_node_id

from db.models import ProjectPosting, ProjectPostingState
# pylint: disable=R0913


@pytest.mark.django_db
def test_student_project_posting(query_project_posting,
                                 company_project_posting_object: ProjectPosting,
                                 project_type_objects, keyword_objects, user_student,
                                 user_employee):
    company_project_posting_object.title = 'title'
    company_project_posting_object.slug = 'title'
    company_project_posting_object.description = 'description'
    company_project_posting_object.team_size = 5
    company_project_posting_object.compensation = 'to be discussed'
    company_project_posting_object.project_from_date = '2021-08-01'
    company_project_posting_object.website = 'http://www.project-posting.lo'
    company_project_posting_object.project_type = project_type_objects[0]
    company_project_posting_object.form_step = 3
    company_project_posting_object.company = None
    company_project_posting_object.employee = None
    company_project_posting_object.student = user_student.student
    company_project_posting_object.state = ProjectPostingState.PUBLIC
    company_project_posting_object.save()
    company_project_posting_object.keywords.set(keyword_objects)

    data, errors = query_project_posting(user_employee, company_project_posting_object.slug)

    assert errors is None
    assert data is not None
    project_posting = data.get('projectPosting')

    assert project_posting.get('title') == 'title'
    assert project_posting.get('displayTitle') == 'tit\xadle'
    assert project_posting.get('slug') == company_project_posting_object.slug
    assert project_posting.get('description') == company_project_posting_object.description
    assert project_posting.get('teamSize') == company_project_posting_object.team_size
    assert project_posting.get('compensation') == company_project_posting_object.compensation
    assert project_posting.get('projectFromDate') == '2021-08-01'
    assert project_posting.get('website') == company_project_posting_object.website
    assert project_posting.get('projectType').get('id') == to_global_id(
        'ProjectType', company_project_posting_object.project_type_id)
    assert int(project_posting.get('formStep')) == company_project_posting_object.form_step
    assert project_posting.get('company') is None
    assert project_posting.get('employee') is None
    assert project_posting.get('student').get('id') == to_global_id('Student',
                                                                    user_student.student.id)
    assert len(project_posting.get('keywords')) == len(
        company_project_posting_object.keywords.all())
    assert project_posting.get('state') == company_project_posting_object.state.upper()


@pytest.mark.django_db
def test_student_project_posting_draft(query_project_posting,
                                       company_project_posting_object: ProjectPosting,
                                       project_type_objects, keyword_objects, user_student):
    company_project_posting_object.title = 'title'
    company_project_posting_object.slug = 'title'
    company_project_posting_object.description = 'description'
    company_project_posting_object.team_size = 5
    company_project_posting_object.compensation = 'to be discussed'
    company_project_posting_object.project_from_date = '2021-08-01'
    company_project_posting_object.website = 'http://www.project-posting.lo'
    company_project_posting_object.project_type = project_type_objects[0]
    company_project_posting_object.form_step = 3
    company_project_posting_object.company = None
    company_project_posting_object.employee = None
    company_project_posting_object.student = user_student.student
    company_project_posting_object.state = ProjectPostingState.DRAFT
    company_project_posting_object.save()
    company_project_posting_object.keywords.set(keyword_objects)

    data, errors = query_project_posting(user_student, company_project_posting_object.slug)

    assert errors is None
    assert data is not None
    project_posting = data.get('projectPosting')

    assert project_posting.get('title') == 'title'
    assert project_posting.get('displayTitle') == 'tit\xadle'
    assert project_posting.get('slug') == company_project_posting_object.slug
    assert project_posting.get('description') == company_project_posting_object.description
    assert project_posting.get('teamSize') == company_project_posting_object.team_size
    assert project_posting.get('compensation') == company_project_posting_object.compensation
    assert project_posting.get('projectFromDate') == '2021-08-01'
    assert project_posting.get('website') == company_project_posting_object.website
    assert project_posting.get('projectType').get('id') == to_global_id(
        'ProjectType', company_project_posting_object.project_type_id)
    assert int(project_posting.get('formStep')) == company_project_posting_object.form_step
    assert project_posting.get('company') is None
    assert project_posting.get('employee') is None
    assert project_posting.get('student').get('id') == to_global_id('Student',
                                                                    user_student.student.id)
    assert len(project_posting.get('keywords')) == len(
        company_project_posting_object.keywords.all())
    assert project_posting.get('state') == company_project_posting_object.state.upper()


@pytest.mark.django_db
def test_student_project_posting_by_id(query_project_posting_by_id,
                                       company_project_posting_object: ProjectPosting,
                                       project_type_objects, keyword_objects, user_student):
    company_project_posting_object.title = 'title'
    company_project_posting_object.slug = 'title'
    company_project_posting_object.description = 'description'
    company_project_posting_object.team_size = 5
    company_project_posting_object.compensation = 'to be discussed'
    company_project_posting_object.project_from_date = '2021-08-01'
    company_project_posting_object.website = 'http://www.project-posting.lo'
    company_project_posting_object.project_type = project_type_objects[0]
    company_project_posting_object.form_step = 3
    company_project_posting_object.company = None
    company_project_posting_object.employee = None
    company_project_posting_object.student = user_student.student
    company_project_posting_object.state = ProjectPostingState.PUBLIC
    company_project_posting_object.save()
    company_project_posting_object.keywords.set(keyword_objects)

    data, errors = query_project_posting_by_id(user_student, company_project_posting_object.id)

    assert errors is None
    assert data is not None
    project_posting = data.get('projectPosting')

    assert project_posting.get('title') == 'title'
    assert project_posting.get('displayTitle') == 'tit\xadle'
    assert project_posting.get('slug') == company_project_posting_object.slug
    assert project_posting.get('description') == company_project_posting_object.description
    assert project_posting.get('teamSize') == company_project_posting_object.team_size
    assert project_posting.get('compensation') == company_project_posting_object.compensation
    assert project_posting.get('projectFromDate') == '2021-08-01'
    assert project_posting.get('website') == company_project_posting_object.website
    assert project_posting.get('projectType').get('id') == to_global_id(
        'ProjectType', company_project_posting_object.project_type_id)
    assert int(project_posting.get('formStep')) == company_project_posting_object.form_step
    assert project_posting.get('company') is None
    assert project_posting.get('employee') is None
    assert project_posting.get('student').get('id') == to_global_id('Student',
                                                                    user_student.student.id)
    assert len(project_posting.get('keywords')) == len(
        company_project_posting_object.keywords.all())
    assert project_posting.get('state') == company_project_posting_object.state.upper()


@pytest.mark.django_db
def test_company_project_posting(query_project_posting,
                                 company_project_posting_object: ProjectPosting,
                                 project_type_objects, keyword_objects, user_employee):
    company_project_posting_object.title = 'title'
    company_project_posting_object.slug = 'title'
    company_project_posting_object.description = 'description'
    company_project_posting_object.team_size = 5
    company_project_posting_object.compensation = 'to be discussed'
    company_project_posting_object.project_from_date = '2021-08-01'
    company_project_posting_object.website = 'http://www.project-posting.lo'
    company_project_posting_object.project_type = project_type_objects[0]
    company_project_posting_object.form_step = 3
    company_project_posting_object.company = user_employee.company
    company_project_posting_object.employee = user_employee.employee
    company_project_posting_object.student = None
    company_project_posting_object.state = ProjectPostingState.PUBLIC
    company_project_posting_object.save()
    company_project_posting_object.keywords.set(keyword_objects)

    data, errors = query_project_posting(user_employee, company_project_posting_object.slug)

    assert errors is None
    assert data is not None
    project_posting = data.get('projectPosting')

    assert project_posting.get('title') == 'title'
    assert project_posting.get('displayTitle') == 'tit\xadle'
    assert project_posting.get('slug') == company_project_posting_object.slug
    assert project_posting.get('description') == company_project_posting_object.description
    assert project_posting.get('teamSize') == company_project_posting_object.team_size
    assert project_posting.get('compensation') == company_project_posting_object.compensation
    assert project_posting.get('projectFromDate') == '2021-08-01'
    assert project_posting.get('website') == company_project_posting_object.website
    assert project_posting.get('projectType').get('id') == to_global_id(
        'ProjectType', company_project_posting_object.project_type_id)
    assert int(project_posting.get('formStep')) == company_project_posting_object.form_step
    assert project_posting.get('company').get('id') == to_global_id('Company',
                                                                    user_employee.company.id)
    assert project_posting.get('employee').get('id') == to_global_id('Employee',
                                                                     user_employee.employee.id)
    assert project_posting.get('student') is None
    assert len(project_posting.get('keywords')) == len(
        company_project_posting_object.keywords.all())
    assert project_posting.get('state') == company_project_posting_object.state.upper()


@pytest.mark.django_db
def test_company_project_posting_draft(query_project_posting,
                                       company_project_posting_object: ProjectPosting,
                                       project_type_objects, keyword_objects, user_employee):
    company_project_posting_object.title = 'title'
    company_project_posting_object.slug = 'title'
    company_project_posting_object.description = 'description'
    company_project_posting_object.team_size = 5
    company_project_posting_object.compensation = 'to be discussed'
    company_project_posting_object.project_from_date = '2021-08-01'
    company_project_posting_object.website = 'http://www.project-posting.lo'
    company_project_posting_object.project_type = project_type_objects[0]
    company_project_posting_object.form_step = 3
    company_project_posting_object.company = user_employee.company
    company_project_posting_object.employee = user_employee.employee
    company_project_posting_object.student = None
    company_project_posting_object.state = ProjectPostingState.DRAFT
    company_project_posting_object.save()
    company_project_posting_object.keywords.set(keyword_objects)

    data, errors = query_project_posting(user_employee, company_project_posting_object.slug)

    assert errors is None
    assert data is not None
    project_posting = data.get('projectPosting')

    assert project_posting.get('title') == 'title'
    assert project_posting.get('displayTitle') == 'tit\xadle'
    assert project_posting.get('slug') == company_project_posting_object.slug
    assert project_posting.get('description') == company_project_posting_object.description
    assert project_posting.get('teamSize') == company_project_posting_object.team_size
    assert project_posting.get('compensation') == company_project_posting_object.compensation
    assert project_posting.get('projectFromDate') == '2021-08-01'
    assert project_posting.get('website') == company_project_posting_object.website
    assert project_posting.get('projectType').get('id') == to_global_id(
        'ProjectType', company_project_posting_object.project_type_id)
    assert int(project_posting.get('formStep')) == company_project_posting_object.form_step
    assert project_posting.get('company').get('id') == to_global_id('Company',
                                                                    user_employee.company.id)
    assert project_posting.get('employee').get('id') == to_global_id('Employee',
                                                                     user_employee.employee.id)
    assert project_posting.get('student') is None
    assert len(project_posting.get('keywords')) == len(
        company_project_posting_object.keywords.all())
    assert project_posting.get('state') == company_project_posting_object.state.upper()


@pytest.mark.django_db
def test_company_project_posting_by_id(query_project_posting_by_id,
                                       company_project_posting_object: ProjectPosting,
                                       project_type_objects, keyword_objects, user_employee):
    company_project_posting_object.title = 'title'
    company_project_posting_object.slug = 'title'
    company_project_posting_object.description = 'description'
    company_project_posting_object.team_size = 5
    company_project_posting_object.compensation = 'to be discussed'
    company_project_posting_object.project_from_date = '2021-08-01'
    company_project_posting_object.website = 'http://www.project-posting.lo'
    company_project_posting_object.project_type = project_type_objects[0]
    company_project_posting_object.form_step = 3
    company_project_posting_object.company = user_employee.company
    company_project_posting_object.employee = user_employee.employee
    company_project_posting_object.student = None
    company_project_posting_object.state = ProjectPostingState.PUBLIC
    company_project_posting_object.save()
    company_project_posting_object.keywords.set(keyword_objects)

    data, errors = query_project_posting_by_id(user_employee, company_project_posting_object.id)

    assert errors is None
    assert data is not None
    project_posting = data.get('projectPosting')

    assert project_posting.get('title') == 'title'
    assert project_posting.get('displayTitle') == 'tit\xadle'
    assert project_posting.get('slug') == company_project_posting_object.slug
    assert project_posting.get('description') == company_project_posting_object.description
    assert project_posting.get('teamSize') == company_project_posting_object.team_size
    assert project_posting.get('compensation') == company_project_posting_object.compensation
    assert project_posting.get('projectFromDate') == '2021-08-01'
    assert project_posting.get('website') == company_project_posting_object.website
    assert project_posting.get('projectType').get('id') == to_global_id(
        'ProjectType', company_project_posting_object.project_type_id)
    assert int(project_posting.get('formStep')) == company_project_posting_object.form_step
    assert project_posting.get('company').get('id') == to_global_id('Company',
                                                                    user_employee.company.id)
    assert project_posting.get('employee').get('id') == to_global_id('Employee',
                                                                     user_employee.employee.id)
    assert project_posting.get('student') is None
    assert len(project_posting.get('keywords')) == len(
        company_project_posting_object.keywords.all())
    assert project_posting.get('state') == company_project_posting_object.state.upper()


@pytest.mark.django_db
def test_student_project_posting_draft_not_accessible(
        query_project_posting, company_project_posting_object: ProjectPosting, project_type_objects,
        keyword_objects, user_student, user_employee):
    company_project_posting_object.title = 'title'
    company_project_posting_object.slug = 'title'
    company_project_posting_object.description = 'description'
    company_project_posting_object.project_from_date = '2021-08-01'
    company_project_posting_object.website = 'http://www.project-posting.lo'
    company_project_posting_object.project_type = project_type_objects[0]
    company_project_posting_object.form_step = 3
    company_project_posting_object.company = None
    company_project_posting_object.employee = None
    company_project_posting_object.student = user_student.student
    company_project_posting_object.state = ProjectPostingState.DRAFT
    company_project_posting_object.save()
    company_project_posting_object.keywords.set(keyword_objects)

    data, errors = query_project_posting(user_employee, company_project_posting_object.slug)

    assert errors is not None
    assert data is not None
    assert data.get('projectPosting') is None


@pytest.mark.django_db
def test_company_project_posting_draft_not_accessible(
        query_project_posting, company_project_posting_object: ProjectPosting, project_type_objects,
        keyword_objects, user_employee, user_student):
    company_project_posting_object.title = 'title'
    company_project_posting_object.slug = 'title'
    company_project_posting_object.description = 'description'
    company_project_posting_object.project_from_date = '2021-08-01'
    company_project_posting_object.website = 'http://www.project-posting.lo'
    company_project_posting_object.project_type = project_type_objects[0]
    company_project_posting_object.form_step = 3
    company_project_posting_object.company = user_employee.company
    company_project_posting_object.employee = user_employee.employee
    company_project_posting_object.student = None
    company_project_posting_object.state = ProjectPostingState.DRAFT
    company_project_posting_object.save()
    company_project_posting_object.keywords.set(keyword_objects)

    data, errors = query_project_posting(user_student, company_project_posting_object.slug)

    assert errors is not None
    assert data is not None
    assert data.get('projectPosting') is None


@pytest.mark.django_db
def test_project_postings(query_project_postings, company_project_posting_objects, user_employee):
    data, errors = query_project_postings(user_employee)
    assert errors is None
    assert data is not None

    edges = data.get('projectPostings').get('edges')
    assert edges is not None
    assert len(edges) == len(company_project_posting_objects) - 1
    assert_node_id(edges[0].get('node'), 'ProjectPosting', company_project_posting_objects[0].id)
    assert_node_id(edges[1].get('node'), 'ProjectPosting', company_project_posting_objects[1].id)
    assert_node_field(edges[0].get('node'), 'slug', company_project_posting_objects[0].slug)
    assert_node_field(edges[1].get('node'), 'slug', company_project_posting_objects[1].slug)


@pytest.mark.django_db
def test_node_query(query_project_posting_node, company_project_posting_objects, user_employee):
    data, errors = query_project_posting_node(user_employee, company_project_posting_objects[0].id)

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, 'ProjectPosting', company_project_posting_objects[0].id)
    assert_node_field(node, 'slug', company_project_posting_objects[0].slug)


@pytest.mark.django_db
def test_project_postings_without_login(query_project_postings, company_project_posting_objects):
    data, errors = query_project_postings(AnonymousUser())
    assert errors is None
    assert data is not None

    edges = data.get('projectPostings').get('edges')
    assert edges is not None
    assert len(edges) == len(company_project_posting_objects) - 1
    assert_node_id(edges[0].get('node'), 'ProjectPosting', company_project_posting_objects[0].id)
    assert_node_id(edges[1].get('node'), 'ProjectPosting', company_project_posting_objects[1].id)
    assert_node_field(edges[0].get('node'), 'slug', company_project_posting_objects[0].slug)
    assert_node_field(edges[1].get('node'), 'slug', company_project_posting_objects[1].slug)


@pytest.mark.django_db
def test_node_without_login(query_project_posting_node, company_project_posting_objects):
    data, errors = query_project_posting_node(AnonymousUser(),
                                              company_project_posting_objects[0].id)

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
    assert_node_id(node, 'ProjectPosting', company_project_posting_objects[0].id)
    assert_node_field(node, 'slug', company_project_posting_objects[0].slug)
