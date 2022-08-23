import pytest

from graphql_relay import from_global_id

from django.contrib.auth.models import AnonymousUser

from db.helper.forms import convert_date
from db.models import Challenge, ProfileType

# pylint: disable=R0913
# pylint: disable=C0301


@pytest.mark.django_db
def test_specific_data_as_company(user_employee, login, challenge_specific_data,
                                  company_challenge_object):
    _test_specific_data(user_employee, user_employee.company, None, company_challenge_object, login,
                        challenge_specific_data)


@pytest.mark.django_db
def test_specific_data_as_student(user_student, login, challenge_specific_data,
                                  company_challenge_object):
    _test_specific_data(user_student, None, user_student.student, company_challenge_object, login,
                        challenge_specific_data)


def _test_specific_data(user, company, student, company_challenge_object, login,
                        challenge_specific_data):
    login(user)
    company_challenge_object.form_step = 2
    company_challenge_object.company = company
    company_challenge_object.employee = None
    company_challenge_object.student = student
    company_challenge_object.save()
    data, errors = challenge_specific_data(user, company_challenge_object.id, '03.2021',
                                           'www.challenge-posting.lo')
    assert errors is None
    assert data is not None
    assert data.get('challengeSpecificData') is not None
    assert data.get('challengeSpecificData').get('success')

    element_id = from_global_id(data.get('challengeSpecificData').get('challengeId'))[1]

    challenge = Challenge.objects.get(pk=element_id)
    assert challenge.challenge_from_date == convert_date('03.2021', '%m.%Y')
    assert challenge.website == 'http://www.challenge-posting.lo'
    if user.type in ProfileType.valid_company_types():
        assert challenge.employee.id == user.employee.id
        assert challenge.company.id == user.company.id
        assert challenge.student is None
    if user.type in ProfileType.valid_student_types():
        assert challenge.student.id == user.student.id
        assert challenge.employee is None
        assert challenge.company is None
    assert challenge.form_step == 3


@pytest.mark.django_db
def test_specific_data_without_login(challenge_specific_data, company_challenge_object):
    data, errors = challenge_specific_data(AnonymousUser(), company_challenge_object.id, '03.2021',
                                           'www.challenge-posting.lo')
    assert errors is not None
    assert data is not None
    assert data.get('challengeSpecificData') is None


@pytest.mark.django_db
def test_specific_data_with_invalid_data(user_employee, login, challenge_specific_data,
                                         company_challenge_object):
    login(user_employee)
    data, errors = challenge_specific_data(user_employee, company_challenge_object.id, '78.2021',
                                           'invalid-url')
    assert errors is None
    assert data is not None
    assert data.get('challengeSpecificData') is not None
    assert data.get('challengeSpecificData').get('success') is False
    assert data.get('challengeSpecificData').get('slug') is None

    errors = data.get('challengeSpecificData').get('errors')
    assert errors is not None
    assert 'challengeFromDate' in errors
    assert 'website' in errors


@pytest.mark.django_db
def test_specific_data_as_employee_from_another_company(user_employee, user_employee_2,
                                                        company_challenge_object, login,
                                                        challenge_specific_data):
    login(user_employee)
    company_challenge_object.form_step = 2
    company_challenge_object.company = user_employee.company
    company_challenge_object.employee = None
    company_challenge_object.student = None
    company_challenge_object.save()
    data, errors = challenge_specific_data(user_employee_2, company_challenge_object.id, '03.2021',
                                           'www.challenge-posting.lo')
    assert errors is None
    assert data is not None
    assert data.get('challengeSpecificData') is not None
    assert data.get('challengeSpecificData').get('success') is False

    errors = data.get('challengeSpecificData').get('errors')
    assert 'employee' in errors


@pytest.mark.django_db
def test_specific_data_as_student_with_challenge_of_company(user_employee, user_student,
                                                            company_challenge_object, login,
                                                            challenge_specific_data):
    login(user_employee)
    company_challenge_object.form_step = 2
    company_challenge_object.company = user_employee.company
    company_challenge_object.employee = None
    company_challenge_object.student = None
    company_challenge_object.save()
    data, errors = challenge_specific_data(user_student, company_challenge_object.id, '03.2021',
                                           'www.challenge-posting.lo')
    assert errors is None
    assert data is not None
    assert data.get('challengeSpecificData') is not None
    assert data.get('challengeSpecificData').get('success') is False

    errors = data.get('challengeSpecificData').get('errors')
    assert 'employee' in errors


@pytest.mark.django_db
def test_specific_data_as_company_with_challenge_of_student_without_employee(
        user_employee, user_student, company_challenge_object, login, challenge_specific_data):
    login(user_employee)
    company_challenge_object.form_step = 2
    company_challenge_object.company = None
    company_challenge_object.employee = None
    company_challenge_object.student = user_student.student
    company_challenge_object.save()
    data, errors = challenge_specific_data(user_employee, company_challenge_object.id, '03.2021',
                                           'www.challenge-posting.lo')
    assert errors is None
    assert data is not None
    assert data.get('challengeSpecificData') is not None
    assert data.get('challengeSpecificData').get('success') is False

    errors = data.get('challengeSpecificData').get('errors')
    assert 'employee' in errors
