import pytest

from django.contrib.auth.models import AnonymousUser

from db.models import Challenge
# pylint: disable=R0913


@pytest.mark.django_db
def test_student_challenge_delete_succeeds_as_student_owner(delete_challenge,
                                                            student_challenge_object: Challenge,
                                                            user_student):
    student_challenge_object.student = user_student.student
    student_challenge_object.save()

    data, errors = delete_challenge(user_student, student_challenge_object.id)
    assert errors is None
    assert data is not None

    assert data.get('deleteChallenge').get('success')


@pytest.mark.django_db
def test_student_challenge_delete_fails_as_employee(delete_challenge,
                                                    student_challenge_object: Challenge,
                                                    user_student, user_employee):
    student_challenge_object.student = user_student.student
    student_challenge_object.save()

    data, errors = delete_challenge(user_employee, student_challenge_object.id)
    assert errors is None
    assert data is not None

    assert not data.get('deleteChallenge').get('success')
    error_message = data.get('deleteChallenge').get('errors').get('student')[0].get('message')
    assert error_message == 'You are not a student'


@pytest.mark.django_db
def test_student_challenge_delete_fails_as_student_not_owner(delete_challenge,
                                                             student_challenge_object: Challenge,
                                                             user_student, user_student_2):
    student_challenge_object.student = user_student.student
    student_challenge_object.save()

    data, errors = delete_challenge(user_student_2, student_challenge_object.id)
    assert errors is None
    assert data is not None

    assert not data.get('deleteChallenge').get('success')
    error_message = data.get('deleteChallenge').get('errors').get('id')[0].get('message')
    assert error_message == 'You are not the owner of the challenge'


@pytest.mark.django_db
def test_student_challenge_delete_fails_as_anonymous(delete_challenge,
                                                     student_challenge_object: Challenge,
                                                     user_student):
    student_challenge_object.student = user_student.student
    student_challenge_object.save()

    data, errors = delete_challenge(AnonymousUser(), student_challenge_object.id)
    assert errors is not None
    assert data is not None

    error = errors[0].get('message')
    node = data.get('node')
    assert node is None
    assert error == "You do not have permission to perform this action"


@pytest.mark.django_db
def test_company_challenge_delete_succeeds_as_right_employee(delete_challenge,
                                                             company_challenge_object: Challenge,
                                                             user_employee):
    company_challenge_object.company = user_employee.company
    company_challenge_object.employee = user_employee.employee
    company_challenge_object.save()

    data, errors = delete_challenge(user_employee, company_challenge_object.id)
    assert errors is None
    assert data is not None

    assert data.get('deleteChallenge').get('success')


@pytest.mark.django_db
def test_company_challenge_delete_fails_as_student(delete_challenge,
                                                   company_challenge_object: Challenge,
                                                   user_employee, user_student):
    company_challenge_object.company = user_employee.company
    company_challenge_object.employee = user_employee.employee
    company_challenge_object.save()

    data, errors = delete_challenge(user_student, company_challenge_object.id)
    assert errors is None
    assert data is not None

    assert not data.get('deleteChallenge').get('success')
    error_message = data.get('deleteChallenge').get('errors').get('company')[0].get('message')
    assert error_message == 'You are not part of a company'


@pytest.mark.django_db
def test_company_challenge_delete_fails_as_unrelated_employee(delete_challenge,
                                                              company_challenge_object: Challenge,
                                                              user_employee, user_employee_2):
    company_challenge_object.company = user_employee.company
    company_challenge_object.employee = user_employee.employee
    company_challenge_object.save()

    data, errors = delete_challenge(user_employee_2, company_challenge_object.id)
    assert errors is None
    assert data is not None

    assert not data.get('deleteChallenge').get('success')
    error_message = data.get('deleteChallenge').get('errors').get('id')[0].get('message')
    assert error_message == 'The challenge is not part of your company'


@pytest.mark.django_db
def test_company_challenge_delete_fails_as_anonymous(delete_challenge,
                                                     company_challenge_object: Challenge,
                                                     user_employee):
    company_challenge_object.company = user_employee.company
    company_challenge_object.employee = user_employee.employee
    company_challenge_object.save()

    data, errors = delete_challenge(AnonymousUser(), company_challenge_object.id)
    assert errors is not None
    assert data is not None

    error = errors[0].get('message')
    node = data.get('node')
    assert node is None
    assert error == "You do not have permission to perform this action"
