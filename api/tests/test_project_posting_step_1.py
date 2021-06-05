import pytest
from django.contrib.auth.models import AnonymousUser

from db.helper.forms import convert_date
from db.models import ProjectPosting, Topic, ProjectType, Keyword, ProfileType


@pytest.mark.django_db
def test_step_1_as_company(user_employee, login, project_posting_step_1, topic_objects, project_type_objects,
                           keyword_objects):
    _test_step_1(user_employee, login, project_posting_step_1, topic_objects, project_type_objects, keyword_objects)


@pytest.mark.django_db
def test_step_1_as_student(user_student, login, project_posting_step_1, topic_objects, project_type_objects,
                           keyword_objects):
    _test_step_1(user_student, login, project_posting_step_1, topic_objects, project_type_objects, keyword_objects)


def _test_step_1(user, login, project_posting_step_1, topic_objects, project_type_objects,
                 keyword_objects):
    login(user)
    data, errors = project_posting_step_1(user, 'title', 'description', 'additional information', '03.2021',
                                          'www.project-posting.lo', topic_objects[0], project_type_objects[0],
                                          keyword_objects)
    assert errors is None
    assert data is not None
    assert data.get('projectPostingStep1') is not None
    assert data.get('projectPostingStep1').get('success')

    project_posting_slug = ProjectPosting.objects.get(slug=data.get('projectPostingStep1').get('slug'))
    project_posting = ProjectPosting.objects.get(pk=data.get('projectPostingStep1').get('projectPostingId'))
    assert project_posting_slug == project_posting
    assert project_posting.title == 'title'
    assert project_posting.slug == f'title-{str(project_posting.id)}'
    assert project_posting.description == 'description'
    assert project_posting.additional_information == 'additional information'
    assert project_posting.project_from_date == convert_date('03.2021', '%m.%Y')
    assert project_posting.website == 'http://www.project-posting.lo'
    assert project_posting.topic == topic_objects[0]
    assert project_posting.project_type == project_type_objects[0]
    assert len(project_posting.keywords.all()) == len(keyword_objects)
    if user.type in ProfileType.valid_company_types():
        assert project_posting.employee.id == user.employee.id
        assert project_posting.company.id == user.company.id
        assert project_posting.student is None
    if user.type in ProfileType.valid_student_types():
        assert project_posting.student.id == user.student.id
        assert project_posting.employee is None
        assert project_posting.company is None
    assert project_posting.form_step == 2


@pytest.mark.django_db
def test_step_1_without_login(project_posting_step_1, topic_objects, project_type_objects,
                              keyword_objects):
    data, errors = project_posting_step_1(AnonymousUser(), 'title', 'description', 'additional information', '03.2021',
                                          'www.project-posting.lo', topic_objects[0], project_type_objects[0],
                                          keyword_objects)
    assert errors is not None
    assert data is not None
    assert data.get('projectPostingStep1') is None


@pytest.mark.django_db
def test_step_1_with_invalid_data(user_employee, login, project_posting_step_1):
    login(user_employee)
    data, errors = project_posting_step_1(user_employee, '', '', '', '78.2021', 'invalid-url', Topic(id=1337),
                                          ProjectType(id=1337), [Keyword(id=1337)])
    assert errors is None
    assert data is not None
    assert data.get('projectPostingStep1') is not None
    assert data.get('projectPostingStep1').get('success') is False
    assert data.get('projectPostingStep1').get('slug') is None

    errors = data.get('projectPostingStep1').get('errors')
    assert errors is not None
    assert 'title' in errors
    assert 'description' in errors
    assert 'additionalInformation' not in errors
    assert 'projectFromDate' in errors
    assert 'website' in errors
    assert 'topic' in errors
    assert 'projectType' in errors
    assert 'keywords' in errors
