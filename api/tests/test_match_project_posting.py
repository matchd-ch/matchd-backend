import pytest
from django.contrib.auth.models import AnonymousUser
from django.core import mail

from db.models import Match


@pytest.mark.django_db
def test_company_match_student_project_posting(user_student, user_employee, company_project_posting_object, match_project_posting, login):
    company_project_posting_object.employee = user_employee.employee
    company_project_posting_object.save()
    login(user_student)

    data, errors = match_project_posting(user_student, company_project_posting_object)
    assert errors is None
    assert data is not None

    match_project_posting_data = data.get('matchProjectPosting')
    assert match_project_posting_data is not None
    assert match_project_posting_data.get('success') is True
    assert match_project_posting_data.get('errors') is None

    match_obj_exists = Match.objects.filter(student=user_student.student, project_posting=company_project_posting_object,
                                            initiator=user_student.type, student_confirmed=True,
                                            company_confirmed=True).exists()
    assert match_obj_exists is True

    mail_to_company = mail.outbox[0]
    assert user_employee.email in mail_to_company.recipients()


@pytest.mark.django_db
def test_company_match_student_project_posting_with_invalid_project_posting(user_employee, student_project_posting_object, match_project_posting, login):
    login(user_employee)
    student_project_posting_object.id = 1337

    data, errors = match_project_posting(user_employee, student_project_posting_object)
    assert errors is None
    assert data is not None

    match_project_posting_data = data.get('matchProjectPosting')
    assert match_project_posting_data is not None
    assert match_project_posting_data.get('success') is False
    assert match_project_posting_data.get('errors') is not None


@pytest.mark.django_db
def test_company_match_student_project_posting_without_login(company_project_posting_object, match_project_posting):
    data, errors = match_project_posting(AnonymousUser(), company_project_posting_object)
    assert errors is not None
    assert data is not None

    match_project_posting_data = data.get('matchProjectPosting')
    assert match_project_posting_data is None


@pytest.mark.django_db
def test_student_match_company_project_posting(user_student, user_employee, student_project_posting_object, match_project_posting, login):
    login(user_employee)

    data, errors = match_project_posting(user_employee, student_project_posting_object)
    assert errors is None
    assert data is not None

    match_project_posting_data = data.get('matchProjectPosting')
    assert match_project_posting_data is not None
    assert match_project_posting_data.get('success') is True
    assert match_project_posting_data.get('errors') is None

    match_obj_exists = Match.objects.filter(company=user_employee.company, project_posting=student_project_posting_object,
                                            initiator=user_employee.type, student_confirmed=True,
                                            company_confirmed=True).exists()
    assert match_obj_exists is True

    mail_to_student = mail.outbox[0]
    assert user_student.email in mail_to_student.recipients()


@pytest.mark.django_db
def test_student_match_company_project_posting_with_invalid_project_posting(user_student, user_employee, company_project_posting_object, match_project_posting, login):
    company_project_posting_object.employee = user_employee.employee
    company_project_posting_object.save()
    login(user_student)
    company_project_posting_object.id = 1337

    data, errors = match_project_posting(user_student, company_project_posting_object)
    assert errors is None
    assert data is not None

    match_project_posting_data = data.get('matchProjectPosting')
    assert match_project_posting_data is not None
    assert match_project_posting_data.get('success') is False
    assert match_project_posting_data.get('errors') is not None


@pytest.mark.django_db
def test_student_match_company_project_posting_without_login(company_project_posting_object, match_project_posting):
    data, errors = match_project_posting(AnonymousUser(), company_project_posting_object)
    assert errors is not None
    assert data is not None

    match_project_posting_data = data.get('matchProjectPosting')
    assert match_project_posting_data is None
