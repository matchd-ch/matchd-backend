import pytest

from graphql_relay import from_global_id

from django.contrib.auth.models import AnonymousUser

from db.models import ProjectPosting, ProjectType, Keyword, ProfileType

# pylint: disable=R0913
# pylint: disable=C0301


@pytest.mark.django_db
def test_base_data_as_company(user_employee, login, project_posting_base_data, project_type_objects,
                              keyword_objects):
    _test_base_data(user_employee, login, project_posting_base_data, project_type_objects,
                    keyword_objects)


@pytest.mark.django_db
def test_base_data_as_student(user_student, login, project_posting_base_data, project_type_objects,
                              keyword_objects):
    _test_base_data(user_student, login, project_posting_base_data, project_type_objects,
                    keyword_objects)


def _test_base_data(user, login, project_posting_base_data, project_type_objects, keyword_objects):
    login(user)
    data, errors = project_posting_base_data(user, 'title', 'description', 5, 'to be defined',
                                             project_type_objects[0], keyword_objects)

    assert errors is None
    assert data is not None
    assert data.get('projectPostingBaseData') is not None
    assert data.get('projectPostingBaseData').get('success')

    slug = data.get('projectPostingBaseData').get('slug')
    element_id = from_global_id(data.get('projectPostingBaseData').get('projectPostingId'))[1]

    project_posting_slug = ProjectPosting.objects.get(slug=slug)
    project_posting = ProjectPosting.objects.get(pk=element_id)

    assert project_posting_slug == project_posting
    assert project_posting.title == 'title'
    assert project_posting.slug == f'title-{str(project_posting.id)}'
    assert project_posting.description == 'description'
    assert project_posting.team_size == 5
    assert project_posting.compensation == 'to be defined'
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
def test_base_data_without_login(project_posting_base_data, project_type_objects, keyword_objects):
    data, errors = project_posting_base_data(AnonymousUser(), 'title', 'description', 5,
                                             'No description', project_type_objects[0],
                                             keyword_objects)
    assert errors is not None
    assert data is not None
    assert data.get('projectPostingBaseData') is None


@pytest.mark.django_db
def test_base_data_with_invalid_data(user_employee, login, project_posting_base_data):
    login(user_employee)
    data, errors = project_posting_base_data(user_employee, '', '', 0, '', ProjectType(id=1337),
                                             [Keyword(id=1337)])
    assert errors is None
    assert data is not None
    assert data.get('projectPostingBaseData') is not None
    assert data.get('projectPostingBaseData').get('success') is False
    assert data.get('projectPostingBaseData').get('slug') is None

    errors = data.get('projectPostingBaseData').get('errors')
    assert errors is not None
    assert 'title' in errors
    assert 'description' in errors
    assert 'teamSize' in errors
    assert 'compensation' in errors
    assert 'projectType' in errors
    assert 'keywords' in errors
