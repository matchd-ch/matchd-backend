import pytest
from db.models import ProjectPosting, ProjectPostingState
# pylint: disable=R0913


@pytest.mark.django_db
def test_student_project_posting(query_project_posting, project_posting_object: ProjectPosting, project_type_objects,
                                 topic_objects, keyword_objects, user_student):
    project_posting_object.title = 'title'
    project_posting_object.slug = 'title'
    project_posting_object.description = 'description'
    project_posting_object.additional_information = 'additional information'
    project_posting_object.project_from_date = '2021-08-01'
    project_posting_object.website = 'http://www.project-posting.lo'
    project_posting_object.topic = topic_objects[0]
    project_posting_object.project_type = project_type_objects[0]
    project_posting_object.form_step = 3
    project_posting_object.company = None
    project_posting_object.employee = None
    project_posting_object.student = user_student.student
    project_posting_object.state = ProjectPostingState.PUBLIC
    project_posting_object.save()
    project_posting_object.keywords.set(keyword_objects)

    data, errors = query_project_posting(user_student, project_posting_object.slug)

    assert errors is None
    assert data is not None
    project_posting = data.get('projectPosting')

    assert project_posting.get('title') == 'title'
    assert project_posting.get('displayTitle') == 'tit\xadle'
    assert project_posting.get('slug') == project_posting_object.slug
    assert project_posting.get('description') == project_posting_object.description
    assert project_posting.get('additionalInformation') == project_posting_object.additional_information
    assert project_posting.get('projectFromDate') == '2021-08-01'
    assert project_posting.get('website') == project_posting_object.website
    assert int(project_posting.get('topic').get('id')) == project_posting_object.topic_id
    assert int(project_posting.get('projectType').get('id')) == project_posting_object.project_type_id
    assert int(project_posting.get('formStep')) == project_posting_object.form_step
    assert project_posting.get('company') is None
    assert project_posting.get('employee') is None
    assert int(project_posting.get('student').get('id')) == user_student.student.id
    assert len(project_posting.get('keywords')) == len(project_posting_object.keywords.all())
    assert project_posting.get('state') == project_posting_object.state.upper()

    match_status = project_posting.get('matchStatus')
    assert match_status is None

    match_hints = project_posting.get('matchHints')
    assert match_hints is not None
    assert match_hints.get('hasConfirmedMatch') is False
    assert match_hints.get('hasRequestedMatch') is False


@pytest.mark.django_db
def test_student_project_posting_draft(query_project_posting, project_posting_object: ProjectPosting,
                                       project_type_objects, topic_objects, keyword_objects, user_student):
    project_posting_object.title = 'title'
    project_posting_object.slug = 'title'
    project_posting_object.description = 'description'
    project_posting_object.additional_information = 'additional information'
    project_posting_object.project_from_date = '2021-08-01'
    project_posting_object.website = 'http://www.project-posting.lo'
    project_posting_object.topic = topic_objects[0]
    project_posting_object.project_type = project_type_objects[0]
    project_posting_object.form_step = 3
    project_posting_object.company = None
    project_posting_object.employee = None
    project_posting_object.student = user_student.student
    project_posting_object.state = ProjectPostingState.DRAFT
    project_posting_object.save()
    project_posting_object.keywords.set(keyword_objects)

    data, errors = query_project_posting(user_student, project_posting_object.slug)

    assert errors is None
    assert data is not None
    project_posting = data.get('projectPosting')

    assert project_posting.get('title') == 'title'
    assert project_posting.get('displayTitle') == 'tit\xadle'
    assert project_posting.get('slug') == project_posting_object.slug
    assert project_posting.get('description') == project_posting_object.description
    assert project_posting.get('additionalInformation') == project_posting_object.additional_information
    assert project_posting.get('projectFromDate') == '2021-08-01'
    assert project_posting.get('website') == project_posting_object.website
    assert int(project_posting.get('topic').get('id')) == project_posting_object.topic_id
    assert int(project_posting.get('projectType').get('id')) == project_posting_object.project_type_id
    assert int(project_posting.get('formStep')) == project_posting_object.form_step
    assert project_posting.get('company') is None
    assert project_posting.get('employee') is None
    assert int(project_posting.get('student').get('id')) == user_student.student.id
    assert len(project_posting.get('keywords')) == len(project_posting_object.keywords.all())
    assert project_posting.get('state') == project_posting_object.state.upper()

    match_status = project_posting.get('matchStatus')
    assert match_status is None

    match_hints = project_posting.get('matchHints')
    assert match_hints is not None
    assert match_hints.get('hasConfirmedMatch') is False
    assert match_hints.get('hasRequestedMatch') is False


@pytest.mark.django_db
def test_student_project_posting_by_id(query_project_posting_by_id, project_posting_object: ProjectPosting,
                                       project_type_objects, topic_objects, keyword_objects, user_student):
    project_posting_object.title = 'title'
    project_posting_object.slug = 'title'
    project_posting_object.description = 'description'
    project_posting_object.additional_information = 'additional information'
    project_posting_object.project_from_date = '2021-08-01'
    project_posting_object.website = 'http://www.project-posting.lo'
    project_posting_object.topic = topic_objects[0]
    project_posting_object.project_type = project_type_objects[0]
    project_posting_object.form_step = 3
    project_posting_object.company = None
    project_posting_object.employee = None
    project_posting_object.student = user_student.student
    project_posting_object.state = ProjectPostingState.PUBLIC
    project_posting_object.save()
    project_posting_object.keywords.set(keyword_objects)

    data, errors = query_project_posting_by_id(user_student, project_posting_object.id)

    assert errors is None
    assert data is not None
    project_posting = data.get('projectPosting')

    assert project_posting.get('title') == 'title'
    assert project_posting.get('displayTitle') == 'tit\xadle'
    assert project_posting.get('slug') == project_posting_object.slug
    assert project_posting.get('description') == project_posting_object.description
    assert project_posting.get('additionalInformation') == project_posting_object.additional_information
    assert project_posting.get('projectFromDate') == '2021-08-01'
    assert project_posting.get('website') == project_posting_object.website
    assert int(project_posting.get('topic').get('id')) == project_posting_object.topic_id
    assert int(project_posting.get('projectType').get('id')) == project_posting_object.project_type_id
    assert int(project_posting.get('formStep')) == project_posting_object.form_step
    assert project_posting.get('company') is None
    assert project_posting.get('employee') is None
    assert int(project_posting.get('student').get('id')) == user_student.student.id
    assert len(project_posting.get('keywords')) == len(project_posting_object.keywords.all())
    assert project_posting.get('state') == project_posting_object.state.upper()

    match_status = project_posting.get('matchStatus')
    assert match_status is None

    match_hints = project_posting.get('matchHints')
    assert match_hints is not None
    assert match_hints.get('hasConfirmedMatch') is False
    assert match_hints.get('hasRequestedMatch') is False


@pytest.mark.django_db
def test_company_project_posting(query_project_posting, project_posting_object: ProjectPosting, project_type_objects,
                                 topic_objects, keyword_objects, user_employee):
    project_posting_object.title = 'title'
    project_posting_object.slug = 'title'
    project_posting_object.description = 'description'
    project_posting_object.additional_information = 'additional information'
    project_posting_object.project_from_date = '2021-08-01'
    project_posting_object.website = 'http://www.project-posting.lo'
    project_posting_object.topic = topic_objects[0]
    project_posting_object.project_type = project_type_objects[0]
    project_posting_object.form_step = 3
    project_posting_object.company = user_employee.company
    project_posting_object.employee = user_employee.employee
    project_posting_object.student = None
    project_posting_object.state = ProjectPostingState.PUBLIC
    project_posting_object.save()
    project_posting_object.keywords.set(keyword_objects)

    data, errors = query_project_posting(user_employee, project_posting_object.slug)

    assert errors is None
    assert data is not None
    project_posting = data.get('projectPosting')

    assert project_posting.get('title') == 'title'
    assert project_posting.get('displayTitle') == 'tit\xadle'
    assert project_posting.get('slug') == project_posting_object.slug
    assert project_posting.get('description') == project_posting_object.description
    assert project_posting.get('additionalInformation') == project_posting_object.additional_information
    assert project_posting.get('projectFromDate') == '2021-08-01'
    assert project_posting.get('website') == project_posting_object.website
    assert int(project_posting.get('topic').get('id')) == project_posting_object.topic_id
    assert int(project_posting.get('projectType').get('id')) == project_posting_object.project_type_id
    assert int(project_posting.get('formStep')) == project_posting_object.form_step
    assert int(project_posting.get('company').get('id')) == user_employee.company.id
    assert int(project_posting.get('employee').get('id')) == user_employee.employee.id
    assert project_posting.get('student') is None
    assert len(project_posting.get('keywords')) == len(project_posting_object.keywords.all())
    assert project_posting.get('state') == project_posting_object.state.upper()

    match_status = project_posting.get('matchStatus')
    assert match_status is None

    match_hints = project_posting.get('matchHints')
    assert match_hints is not None
    assert match_hints.get('hasConfirmedMatch') is False
    assert match_hints.get('hasRequestedMatch') is False


@pytest.mark.django_db
def test_company_project_posting_draft(query_project_posting, project_posting_object: ProjectPosting,
                                       project_type_objects, topic_objects, keyword_objects, user_employee):
    project_posting_object.title = 'title'
    project_posting_object.slug = 'title'
    project_posting_object.description = 'description'
    project_posting_object.additional_information = 'additional information'
    project_posting_object.project_from_date = '2021-08-01'
    project_posting_object.website = 'http://www.project-posting.lo'
    project_posting_object.topic = topic_objects[0]
    project_posting_object.project_type = project_type_objects[0]
    project_posting_object.form_step = 3
    project_posting_object.company = user_employee.company
    project_posting_object.employee = user_employee.employee
    project_posting_object.student = None
    project_posting_object.state = ProjectPostingState.DRAFT
    project_posting_object.save()
    project_posting_object.keywords.set(keyword_objects)

    data, errors = query_project_posting(user_employee, project_posting_object.slug)

    assert errors is None
    assert data is not None
    project_posting = data.get('projectPosting')

    assert project_posting.get('title') == 'title'
    assert project_posting.get('displayTitle') == 'tit\xadle'
    assert project_posting.get('slug') == project_posting_object.slug
    assert project_posting.get('description') == project_posting_object.description
    assert project_posting.get('additionalInformation') == project_posting_object.additional_information
    assert project_posting.get('projectFromDate') == '2021-08-01'
    assert project_posting.get('website') == project_posting_object.website
    assert int(project_posting.get('topic').get('id')) == project_posting_object.topic_id
    assert int(project_posting.get('projectType').get('id')) == project_posting_object.project_type_id
    assert int(project_posting.get('formStep')) == project_posting_object.form_step
    assert int(project_posting.get('company').get('id')) == user_employee.company.id
    assert int(project_posting.get('employee').get('id')) == user_employee.employee.id
    assert project_posting.get('student') is None
    assert len(project_posting.get('keywords')) == len(project_posting_object.keywords.all())
    assert project_posting.get('state') == project_posting_object.state.upper()

    match_status = project_posting.get('matchStatus')
    assert match_status is None

    match_hints = project_posting.get('matchHints')
    assert match_hints is not None
    assert match_hints.get('hasConfirmedMatch') is False
    assert match_hints.get('hasRequestedMatch') is False


@pytest.mark.django_db
def test_company_project_posting_by_id(query_project_posting_by_id, project_posting_object: ProjectPosting,
                                       project_type_objects, topic_objects, keyword_objects, user_employee):
    project_posting_object.title = 'title'
    project_posting_object.slug = 'title'
    project_posting_object.description = 'description'
    project_posting_object.additional_information = 'additional information'
    project_posting_object.project_from_date = '2021-08-01'
    project_posting_object.website = 'http://www.project-posting.lo'
    project_posting_object.topic = topic_objects[0]
    project_posting_object.project_type = project_type_objects[0]
    project_posting_object.form_step = 3
    project_posting_object.company = user_employee.company
    project_posting_object.employee = user_employee.employee
    project_posting_object.student = None
    project_posting_object.state = ProjectPostingState.PUBLIC
    project_posting_object.save()
    project_posting_object.keywords.set(keyword_objects)

    data, errors = query_project_posting_by_id(user_employee, project_posting_object.id)

    assert errors is None
    assert data is not None
    project_posting = data.get('projectPosting')

    assert project_posting.get('title') == 'title'
    assert project_posting.get('displayTitle') == 'tit\xadle'
    assert project_posting.get('slug') == project_posting_object.slug
    assert project_posting.get('description') == project_posting_object.description
    assert project_posting.get('additionalInformation') == project_posting_object.additional_information
    assert project_posting.get('projectFromDate') == '2021-08-01'
    assert project_posting.get('website') == project_posting_object.website
    assert int(project_posting.get('topic').get('id')) == project_posting_object.topic_id
    assert int(project_posting.get('projectType').get('id')) == project_posting_object.project_type_id
    assert int(project_posting.get('formStep')) == project_posting_object.form_step
    assert int(project_posting.get('company').get('id')) == user_employee.company.id
    assert int(project_posting.get('employee').get('id')) == user_employee.employee.id
    assert project_posting.get('student') is None
    assert len(project_posting.get('keywords')) == len(project_posting_object.keywords.all())
    assert project_posting.get('state') == project_posting_object.state.upper()

    match_status = project_posting.get('matchStatus')
    assert match_status is None

    match_hints = project_posting.get('matchHints')
    assert match_hints is not None
    assert match_hints.get('hasConfirmedMatch') is False
    assert match_hints.get('hasRequestedMatch') is False


@pytest.mark.django_db
def test_student_project_posting_draft_not_accessible(query_project_posting, project_posting_object: ProjectPosting,
                                                      project_type_objects, topic_objects, keyword_objects,
                                                      user_student, user_employee):
    project_posting_object.title = 'title'
    project_posting_object.slug = 'title'
    project_posting_object.description = 'description'
    project_posting_object.additional_information = 'additional information'
    project_posting_object.project_from_date = '2021-08-01'
    project_posting_object.website = 'http://www.project-posting.lo'
    project_posting_object.topic = topic_objects[0]
    project_posting_object.project_type = project_type_objects[0]
    project_posting_object.form_step = 3
    project_posting_object.company = None
    project_posting_object.employee = None
    project_posting_object.student = user_student.student
    project_posting_object.state = ProjectPostingState.DRAFT
    project_posting_object.save()
    project_posting_object.keywords.set(keyword_objects)

    data, errors = query_project_posting(user_employee, project_posting_object.slug)

    assert errors is not None
    assert data is not None
    assert data.get('projectPosting') is None


@pytest.mark.django_db
def test_company_project_posting_draft_not_accessible(query_project_posting, project_posting_object: ProjectPosting,
                                                      project_type_objects, topic_objects, keyword_objects,
                                                      user_employee, user_student):
    project_posting_object.title = 'title'
    project_posting_object.slug = 'title'
    project_posting_object.description = 'description'
    project_posting_object.additional_information = 'additional information'
    project_posting_object.project_from_date = '2021-08-01'
    project_posting_object.website = 'http://www.project-posting.lo'
    project_posting_object.topic = topic_objects[0]
    project_posting_object.project_type = project_type_objects[0]
    project_posting_object.form_step = 3
    project_posting_object.company = user_employee.company
    project_posting_object.employee = user_employee.employee
    project_posting_object.student = None
    project_posting_object.state = ProjectPostingState.DRAFT
    project_posting_object.save()
    project_posting_object.keywords.set(keyword_objects)

    data, errors = query_project_posting(user_student, project_posting_object.slug)

    assert errors is not None
    assert data is not None
    assert data.get('projectPosting') is None