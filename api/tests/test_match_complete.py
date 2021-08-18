import pytest
from django.core import mail

from db.models import Match


# pylint: disable=R0913
@pytest.mark.django_db
def test_match_starting_with_student_match(user_student, user_employee, job_posting_object, match_student, login,
                                           match_job_posting):
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()
    login(user_employee)

    data, errors = match_student(user_employee, user_student.student.id, job_posting_object.id)
    assert errors is None
    assert data is not None

    login(user_student)
    data, errors = match_job_posting(user_student, job_posting_object.id)
    assert errors is None
    assert data is not None

    match_obj_exists = Match.objects.filter(student=user_student.student, job_posting=job_posting_object,
                                            initiator=user_employee.type, student_confirmed=True,
                                            company_confirmed=True, complete_mail_sent=True).exists()
    assert match_obj_exists is True

    mail_to_company = mail.outbox[2]
    assert user_employee.email in mail_to_company.recipients()


# pylint: disable=R0913
@pytest.mark.django_db
def test_match_starting_with_job_posting_match(user_student, user_employee, job_posting_object, match_student, login,
                                               match_job_posting):
    job_posting_object.employee = user_employee.employee
    job_posting_object.save()

    login(user_student)
    data, errors = match_job_posting(user_student, job_posting_object.id)
    assert errors is None
    assert data is not None

    login(user_employee)

    data, errors = match_student(user_employee, user_student.student.id, job_posting_object.id)
    assert errors is None
    assert data is not None

    match_obj_exists = Match.objects.filter(student=user_student.student, job_posting=job_posting_object,
                                            initiator=user_student.type, student_confirmed=True,
                                            company_confirmed=True, complete_mail_sent=True).exists()
    assert match_obj_exists is True

    mail_to_student = mail.outbox[2]
    assert user_student.email in mail_to_student.recipients()
