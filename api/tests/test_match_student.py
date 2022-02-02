import pytest

from django.contrib.auth.models import AnonymousUser
from django.core import mail

from db.models import Match


@pytest.mark.django_db
def test_match_student(user_student, user_employee, job_posting_object, match_student, login):
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()
    login(user_employee)

    data, errors = match_student(user_employee, user_student.student.id, job_posting_object.id)
    assert errors is None
    assert data is not None

    match_student_data = data.get('matchStudent')
    assert match_student_data is not None
    assert match_student_data.get('success') is True
    assert match_student_data.get('errors') is None

    match_obj_exists = Match.objects.filter(student=user_student.student,
                                            job_posting=job_posting_object,
                                            initiator=user_employee.type,
                                            student_confirmed=False,
                                            company_confirmed=True).exists()
    assert match_obj_exists is True

    mail_to_student = mail.outbox[0]
    assert user_student.email in mail_to_student.recipients()

    mail_to_company = mail.outbox[1]
    assert user_employee.email in mail_to_company.recipients()


@pytest.mark.django_db
def test_match_student_without_login(user_employee, user_student, job_posting_object,
                                     match_student):
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()

    data, errors = match_student(AnonymousUser(), user_student.student.id, job_posting_object.id)
    assert errors is not None
    assert data is not None

    match_student_data = data.get('matchStudent')
    assert match_student_data is None


@pytest.mark.django_db
def test_match_student_as_student(user_student, user_employee, job_posting_object, match_student,
                                  login):
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()
    login(user_student)

    data, errors = match_student(user_student, user_student.student.id, job_posting_object.id)
    assert errors is None
    assert data is not None

    match_student_data = data.get('matchStudent')
    assert match_student_data is not None
    assert match_student_data.get('success') is False
    assert match_student_data.get('errors') is not None


@pytest.mark.django_db
def test_match_job_posting_with_invalid_job_posting(user_employee, match_student, login):
    login(user_employee)

    data, errors = match_student(user_employee, 1337, 1337)
    assert errors is None
    assert data is not None

    match_student_data = data.get('matchStudent')
    assert match_student_data is not None
    assert match_student_data.get('success') is False
    assert match_student_data.get('errors') is not None
