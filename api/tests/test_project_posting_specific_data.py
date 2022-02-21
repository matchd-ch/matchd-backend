import pytest

from django.contrib.auth.models import AnonymousUser

from db.helper.forms import convert_date
from db.models import ProjectPosting, ProfileType

# pylint: disable=R0913
# pylint: disable=C0301


@pytest.mark.django_db
def test_specific_data_as_company(user_employee, login, project_posting_specific_data,
                                  company_project_posting_object):
    _test_specific_data(user_employee, user_employee.company, None, company_project_posting_object,
                        login, project_posting_specific_data)


@pytest.mark.django_db
def test_specific_data_as_student(user_student, login, project_posting_specific_data,
                                  company_project_posting_object):
    _test_specific_data(user_student, None, user_student.student, company_project_posting_object,
                        login, project_posting_specific_data)


def _test_specific_data(user, company, student, company_project_posting_object, login,
                        project_posting_specific_data):
    login(user)
    company_project_posting_object.form_step = 2
    company_project_posting_object.company = company
    company_project_posting_object.employee = None
    company_project_posting_object.student = student
    company_project_posting_object.save()
    data, errors = project_posting_specific_data(user, company_project_posting_object.id, '03.2021',
                                                 'www.project-posting.lo')
    assert errors is None
    assert data is not None
    assert data.get('projectPostingSpecificData') is not None
    assert data.get('projectPostingSpecificData').get('success')

    project_posting = ProjectPosting.objects.get(
        pk=data.get('projectPostingSpecificData').get('projectPostingId'))
    assert project_posting.project_from_date == convert_date('03.2021', '%m.%Y')
    assert project_posting.website == 'http://www.project-posting.lo'
    if user.type in ProfileType.valid_company_types():
        assert project_posting.employee.id == user.employee.id
        assert project_posting.company.id == user.company.id
        assert project_posting.student is None
    if user.type in ProfileType.valid_student_types():
        assert project_posting.student.id == user.student.id
        assert project_posting.employee is None
        assert project_posting.company is None
    assert project_posting.form_step == 3


@pytest.mark.django_db
def test_specific_data_without_login(project_posting_specific_data, company_project_posting_object):
    data, errors = project_posting_specific_data(AnonymousUser(), company_project_posting_object.id,
                                                 '03.2021', 'www.project-posting.lo')
    assert errors is not None
    assert data is not None
    assert data.get('projectPostingSpecificData') is None


@pytest.mark.django_db
def test_specific_data_with_invalid_data(user_employee, login, project_posting_specific_data,
                                         company_project_posting_object):
    login(user_employee)
    data, errors = project_posting_specific_data(user_employee, company_project_posting_object.id,
                                                 '78.2021', 'invalid-url')
    assert errors is None
    assert data is not None
    assert data.get('projectPostingSpecificData') is not None
    assert data.get('projectPostingSpecificData').get('success') is False
    assert data.get('projectPostingSpecificData').get('slug') is None

    errors = data.get('projectPostingSpecificData').get('errors')
    assert errors is not None
    assert 'projectFromDate' in errors
    assert 'website' in errors


@pytest.mark.django_db
def test_specific_data_as_employee_from_another_company(user_employee, user_employee_2,
                                                        company_project_posting_object, login,
                                                        project_posting_specific_data):
    login(user_employee)
    company_project_posting_object.form_step = 2
    company_project_posting_object.company = user_employee.company
    company_project_posting_object.employee = None
    company_project_posting_object.student = None
    company_project_posting_object.save()
    data, errors = project_posting_specific_data(user_employee_2, company_project_posting_object.id,
                                                 '03.2021', 'www.project-posting.lo')
    assert errors is None
    assert data is not None
    assert data.get('projectPostingSpecificData') is not None
    assert data.get('projectPostingSpecificData').get('success') is False

    errors = data.get('projectPostingSpecificData').get('errors')
    assert 'employee' in errors


@pytest.mark.django_db
def test_specific_data_as_student_with_project_of_company(user_employee, user_student,
                                                          company_project_posting_object, login,
                                                          project_posting_specific_data):
    login(user_employee)
    company_project_posting_object.form_step = 2
    company_project_posting_object.company = user_employee.company
    company_project_posting_object.employee = None
    company_project_posting_object.student = None
    company_project_posting_object.save()
    data, errors = project_posting_specific_data(user_student, company_project_posting_object.id,
                                                 '03.2021', 'www.project-posting.lo')
    assert errors is None
    assert data is not None
    assert data.get('projectPostingSpecificData') is not None
    assert data.get('projectPostingSpecificData').get('success') is False

    errors = data.get('projectPostingSpecificData').get('errors')
    assert 'employee' in errors


@pytest.mark.django_db
def test_specific_data_as_company_with_project_of_student_without_employee(
        user_employee, user_student, company_project_posting_object, login,
        project_posting_specific_data):
    login(user_employee)
    company_project_posting_object.form_step = 2
    company_project_posting_object.company = None
    company_project_posting_object.employee = None
    company_project_posting_object.student = user_student.student
    company_project_posting_object.save()
    data, errors = project_posting_specific_data(user_employee, company_project_posting_object.id,
                                                 '03.2021', 'www.project-posting.lo')
    assert errors is None
    assert data is not None
    assert data.get('projectPostingSpecificData') is not None
    assert data.get('projectPostingSpecificData').get('success') is False

    errors = data.get('projectPostingSpecificData').get('errors')
    assert 'employee' in errors
