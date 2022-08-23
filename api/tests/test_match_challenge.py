import pytest

from django.contrib.auth.models import AnonymousUser
from django.core import mail

from db.models import Match


@pytest.mark.django_db
def test_company_match_student_challenge(user_student, user_employee, company_challenge_object,
                                         match_challenge, login):
    company_challenge_object.employee = user_employee.employee
    company_challenge_object.save()
    login(user_student)

    data, errors = match_challenge(user_student, company_challenge_object)
    assert errors is None
    assert data is not None

    match_challenge_data = data.get('matchChallenge')
    assert match_challenge_data is not None
    assert match_challenge_data.get('success') is True
    assert match_challenge_data.get('errors') is None

    match_obj_exists = Match.objects.filter(student=user_student.student,
                                            challenge=company_challenge_object,
                                            initiator=user_student.type,
                                            student_confirmed=True,
                                            company_confirmed=True).exists()
    assert match_obj_exists is True

    mail_to_company = mail.outbox[0]
    assert user_employee.email in mail_to_company.recipients()


@pytest.mark.django_db
def test_company_match_student_challenge_with_invalid_challenge(user_employee,
                                                                student_challenge_object,
                                                                match_challenge, login):
    login(user_employee)
    student_challenge_object.id = 1337

    data, errors = match_challenge(user_employee, student_challenge_object)
    assert errors is None
    assert data is not None

    match_challenge_data = data.get('matchChallenge')
    assert match_challenge_data is not None
    assert match_challenge_data.get('success') is False
    assert match_challenge_data.get('errors') is not None


@pytest.mark.django_db
def test_company_match_student_challenge_without_login(company_challenge_object, match_challenge):
    data, errors = match_challenge(AnonymousUser(), company_challenge_object)
    assert errors is not None
    assert data is not None

    match_challenge_data = data.get('matchChallenge')
    assert match_challenge_data is None


@pytest.mark.django_db
def test_student_match_company_challenge(user_student, user_employee, student_challenge_object,
                                         match_challenge, login):
    login(user_employee)

    data, errors = match_challenge(user_employee, student_challenge_object)
    assert errors is None
    assert data is not None

    match_challenge_data = data.get('matchChallenge')
    assert match_challenge_data is not None
    assert match_challenge_data.get('success') is True
    assert match_challenge_data.get('errors') is None

    match_obj_exists = Match.objects.filter(company=user_employee.company,
                                            challenge=student_challenge_object,
                                            initiator=user_employee.type,
                                            student_confirmed=True,
                                            company_confirmed=True).exists()
    assert match_obj_exists is True

    mail_to_student = mail.outbox[0]
    assert user_student.email in mail_to_student.recipients()


@pytest.mark.django_db
def test_student_match_company_challenge_with_invalid_challenge(user_student, user_employee,
                                                                company_challenge_object,
                                                                match_challenge, login):
    company_challenge_object.employee = user_employee.employee
    company_challenge_object.save()
    login(user_student)
    company_challenge_object.id = 1337

    data, errors = match_challenge(user_student, company_challenge_object)
    assert errors is None
    assert data is not None

    match_challenge_data = data.get('matchChallenge')
    assert match_challenge_data is not None
    assert match_challenge_data.get('success') is False
    assert match_challenge_data.get('errors') is not None


@pytest.mark.django_db
def test_student_match_company_challenge_without_login(company_challenge_object, match_challenge):
    data, errors = match_challenge(AnonymousUser(), company_challenge_object)
    assert errors is not None
    assert data is not None

    match_challenge_data = data.get('matchChallenge')
    assert match_challenge_data is None
