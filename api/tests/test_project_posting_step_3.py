import pytest
from django.contrib.auth.models import AnonymousUser

from db.models import ProjectPostingState, ProjectPosting

# pylint: disable=R0913


@pytest.mark.django_db
def test_step_3_as_company(user_employee, company_project_posting_object, login, project_posting_step_3):
    _test_step_3(user_employee, user_employee.employee, user_employee.company, None, company_project_posting_object,
                 login, project_posting_step_3)


@pytest.mark.django_db
def test_step_3_as_student(user_student, company_project_posting_object, login, project_posting_step_3):
    _test_step_3(user_student, None, None, user_student.student, company_project_posting_object, login,
                 project_posting_step_3)


def _test_step_3(user, employee, company, student, company_project_posting_object, login, project_posting_step_3):
    login(user)
    company_project_posting_object.form_step = 3
    company_project_posting_object.company = company
    company_project_posting_object.employee = None
    company_project_posting_object.student = student
    company_project_posting_object.save()
    data, errors = project_posting_step_3(user, company_project_posting_object.id, ProjectPostingState.PUBLIC, employee)
    assert errors is None
    assert data is not None
    assert data.get('projectPostingStep3') is not None
    assert data.get('projectPostingStep3').get('success')

    project_posting_slug = ProjectPosting.objects.get(slug=data.get('projectPostingStep3').get('slug'))
    project_posting = ProjectPosting.objects.get(pk=data.get('projectPostingStep3').get('projectPostingId'))
    assert project_posting_slug == project_posting
    if employee is not None:
        assert project_posting.employee.id == employee.id
        assert project_posting.company.id == employee.user.company.id
        assert project_posting.student is None
    if student is not None:
        assert project_posting.student.id == student.id
        assert project_posting.employee is None
        assert project_posting.company is None
    assert project_posting.state == ProjectPostingState.PUBLIC
    assert project_posting.form_step == 4


@pytest.mark.django_db
def test_step_3_with_invalid_job_posting_id(user_employee, login, project_posting_step_3):
    login(user_employee)
    data, errors = project_posting_step_3(user_employee, 1337, ProjectPostingState.PUBLIC, user_employee.employee)
    assert errors is not None
    assert data is not None
    assert data.get('projectPostingStep3') is None


@pytest.mark.django_db
def test_step_3_without_login(user_employee, company_project_posting_object, project_posting_step_3):
    data, errors = project_posting_step_3(AnonymousUser(), company_project_posting_object.id,
                                          ProjectPostingState.PUBLIC, user_employee.employee)
    assert errors is not None
    assert data is not None
    assert data.get('projectPostingStep3') is None


@pytest.mark.django_db
def test_step_3_with_invalid_step(user_employee, company_project_posting_object, login, project_posting_step_3):
    login(user_employee)
    company_project_posting_object.form_step = 1
    company_project_posting_object.save()
    data, errors = project_posting_step_3(user_employee, company_project_posting_object.id, ProjectPostingState.PUBLIC,
                                          user_employee.employee)
    assert errors is None
    assert data is not None
    assert data.get('projectPostingStep3') is not None
    assert data.get('projectPostingStep3').get('success') is False

    errors = data.get('projectPostingStep3').get('errors')
    assert errors is not None
    assert 'projectPostingStep' in errors


@pytest.mark.django_db
def test_step_3_as_employee_from_another_company(user_employee, user_employee_2, company_project_posting_object, login,
                                                 project_posting_step_3):
    login(user_employee)
    company_project_posting_object.form_step = 3
    company_project_posting_object.company = user_employee.company
    company_project_posting_object.employee = None
    company_project_posting_object.student = None
    company_project_posting_object.save()
    data, errors = project_posting_step_3(user_employee_2, company_project_posting_object.id,
                                          ProjectPostingState.PUBLIC, user_employee.employee)
    assert errors is None
    assert data is not None
    assert data.get('projectPostingStep3') is not None
    assert data.get('projectPostingStep3').get('success') is False

    errors = data.get('projectPostingStep3').get('errors')
    assert 'employee' in errors


@pytest.mark.django_db
def test_step_3_as_student_with_project_of_company(user_employee, user_student, company_project_posting_object, login,
                                                   project_posting_step_3):
    login(user_employee)
    company_project_posting_object.form_step = 3
    company_project_posting_object.company = user_employee.company
    company_project_posting_object.employee = None
    company_project_posting_object.student = None
    company_project_posting_object.save()
    data, errors = project_posting_step_3(user_student, company_project_posting_object.id, ProjectPostingState.PUBLIC,
                                          user_employee.employee)
    assert errors is None
    assert data is not None
    assert data.get('projectPostingStep3') is not None
    assert data.get('projectPostingStep3').get('success') is False

    errors = data.get('projectPostingStep3').get('errors')
    assert 'employee' in errors


@pytest.mark.django_db
def test_step_3_as_company_with_project_of_student(user_employee, user_student, company_project_posting_object, login,
                                                   project_posting_step_3):
    login(user_employee)
    company_project_posting_object.form_step = 3
    company_project_posting_object.company = None
    company_project_posting_object.employee = None
    company_project_posting_object.student = user_student.student
    company_project_posting_object.save()
    data, errors = project_posting_step_3(user_employee, company_project_posting_object.id, ProjectPostingState.PUBLIC,
                                          user_employee.employee)
    assert errors is None
    assert data is not None
    assert data.get('projectPostingStep3') is not None
    assert data.get('projectPostingStep3').get('success') is False

    errors = data.get('projectPostingStep3').get('errors')
    assert 'employee' in errors


@pytest.mark.django_db
def test_step_3_as_company_with_project_of_student_without_employee(user_employee, user_student,
                                                                    company_project_posting_object, login,
                                                                    project_posting_step_3):
    login(user_employee)
    company_project_posting_object.form_step = 3
    company_project_posting_object.company = None
    company_project_posting_object.employee = None
    company_project_posting_object.student = user_student.student
    company_project_posting_object.save()
    data, errors = project_posting_step_3(user_employee, company_project_posting_object.id, ProjectPostingState.PUBLIC,
                                          None)
    assert errors is None
    assert data is not None
    assert data.get('projectPostingStep3') is not None
    assert data.get('projectPostingStep3').get('success') is False

    errors = data.get('projectPostingStep3').get('errors')
    assert 'employee' in errors