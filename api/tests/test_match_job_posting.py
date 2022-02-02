import pytest

from django.contrib.auth.models import AnonymousUser
from django.core import mail

from db.models import Match


@pytest.mark.django_db
def test_match_job_posting(user_student, user_employee, job_posting_object, match_job_posting,
                           login):
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()
    login(user_student)

    data, errors = match_job_posting(user_student, job_posting_object.id)
    assert errors is None
    assert data is not None

    match_job_posting_data = data.get('matchJobPosting')
    assert match_job_posting_data is not None
    assert match_job_posting_data.get('success') is True
    assert match_job_posting_data.get('errors') is None

    match_obj_exists = Match.objects.filter(student=user_student.student,
                                            job_posting=job_posting_object,
                                            initiator=user_student.type,
                                            student_confirmed=True,
                                            company_confirmed=False).exists()
    assert match_obj_exists is True

    mail_to_company = mail.outbox[0]
    assert user_employee.email in mail_to_company.recipients()

    mail_to_student = mail.outbox[1]
    assert user_student.email in mail_to_student.recipients()


@pytest.mark.django_db
def test_match_job_posting_without_login(user_employee, job_posting_object, match_job_posting):
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()

    data, errors = match_job_posting(AnonymousUser(), job_posting_object.id)
    assert errors is not None
    assert data is not None

    match_job_posting_data = data.get('matchJobPosting')
    assert match_job_posting_data is None


@pytest.mark.django_db
def test_match_job_posting_as_employee(user_employee, job_posting_object, match_job_posting, login):
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()
    login(user_employee)

    data, errors = match_job_posting(user_employee, job_posting_object.id)
    assert errors is None
    assert data is not None

    match_job_posting_data = data.get('matchJobPosting')
    assert match_job_posting_data is not None
    assert match_job_posting_data.get('success') is False
    assert match_job_posting_data.get('errors') is not None


@pytest.mark.django_db
def test_match_job_posting_with_invalid_job_posting(user_student, match_job_posting, login):
    login(user_student)

    data, errors = match_job_posting(user_student, 1337)
    assert errors is None
    assert data is not None

    match_job_posting_data = data.get('matchJobPosting')
    assert match_job_posting_data is not None
    assert match_job_posting_data.get('success') is False
    assert match_job_posting_data.get('errors') is not None
