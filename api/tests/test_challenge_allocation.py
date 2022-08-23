import pytest

from graphql_relay import from_global_id

from django.contrib.auth.models import AnonymousUser

from db.models import ChallengeState, Challenge

# pylint: disable=R0913


@pytest.mark.django_db
def test_allocation_as_company(user_employee, company_challenge_object, login,
                               challenge_allocation):
    _test_allocation(user_employee, user_employee.employee, user_employee.company, None,
                     company_challenge_object, login, challenge_allocation)


@pytest.mark.django_db
def test_allocation_as_student(user_student, company_challenge_object, login, challenge_allocation):
    _test_allocation(user_student, None, None, user_student.student, company_challenge_object,
                     login, challenge_allocation)


def _test_allocation(user, employee, company, student, company_challenge_object, login,
                     challenge_allocation):
    login(user)
    company_challenge_object.form_step = 3
    company_challenge_object.company = company
    company_challenge_object.employee = None
    company_challenge_object.student = student
    company_challenge_object.state = ChallengeState.DRAFT
    company_challenge_object.save()
    data, errors = challenge_allocation(user, company_challenge_object.id, ChallengeState.PUBLIC,
                                        employee)
    assert errors is None
    assert data is not None
    assert data.get('challengeAllocation') is not None
    assert data.get('challengeAllocation').get('success')

    slug = data.get('challengeAllocation').get('slug')
    element_id = from_global_id(data.get('challengeAllocation').get('challengeId'))[1]

    challenge_slug = Challenge.objects.get(slug=slug)
    challenge = Challenge.objects.get(pk=element_id)
    assert challenge_slug == challenge
    if employee is not None:
        assert challenge.employee.id == employee.id
        assert challenge.company.id == employee.user.company.id
        assert challenge.student is None
    if student is not None:
        assert challenge.student.id == student.id
        assert challenge.employee is None
        assert challenge.company is None
    assert challenge.state == ChallengeState.PUBLIC
    assert challenge.date_published is not None
    assert challenge.form_step == 4


@pytest.mark.django_db
def test_allocation_with_invalid_job_posting_id(user_employee, login, challenge_allocation):
    login(user_employee)
    data, errors = challenge_allocation(user_employee, 1337, ChallengeState.PUBLIC,
                                        user_employee.employee)
    assert errors is not None
    assert data is not None
    assert data.get('challengeAllocation') is None


@pytest.mark.django_db
def test_allocation_without_login(user_employee, company_challenge_object, challenge_allocation):
    data, errors = challenge_allocation(AnonymousUser(), company_challenge_object.id,
                                        ChallengeState.PUBLIC, user_employee.employee)
    assert errors is not None
    assert data is not None
    assert data.get('challengeAllocation') is None


@pytest.mark.django_db
def test_allocation_with_invalid_step(user_employee, company_challenge_object, login,
                                      challenge_allocation):
    login(user_employee)
    company_challenge_object.form_step = 1
    company_challenge_object.save()
    data, errors = challenge_allocation(user_employee, company_challenge_object.id,
                                        ChallengeState.PUBLIC, user_employee.employee)
    assert errors is None
    assert data is not None
    assert data.get('challengeAllocation') is not None
    assert data.get('challengeAllocation').get('success') is False

    errors = data.get('challengeAllocation').get('errors')
    assert errors is not None
    assert 'challengeStep' in errors


@pytest.mark.django_db
def test_allocation_as_employee_from_another_company(user_employee, user_employee_2,
                                                     company_challenge_object, login,
                                                     challenge_allocation):
    login(user_employee)
    company_challenge_object.form_step = 3
    company_challenge_object.company = user_employee.company
    company_challenge_object.employee = None
    company_challenge_object.student = None
    company_challenge_object.save()
    data, errors = challenge_allocation(user_employee_2, company_challenge_object.id,
                                        ChallengeState.PUBLIC, user_employee.employee)
    assert errors is None
    assert data is not None
    assert data.get('challengeAllocation') is not None
    assert data.get('challengeAllocation').get('success') is False

    errors = data.get('challengeAllocation').get('errors')
    assert 'employee' in errors


@pytest.mark.django_db
def test_allocation_as_student_with_challenge_of_company(user_employee, user_student,
                                                         company_challenge_object, login,
                                                         challenge_allocation):
    login(user_employee)
    company_challenge_object.form_step = 3
    company_challenge_object.company = user_employee.company
    company_challenge_object.employee = None
    company_challenge_object.student = None
    company_challenge_object.save()
    data, errors = challenge_allocation(user_student, company_challenge_object.id,
                                        ChallengeState.PUBLIC, user_employee.employee)
    assert errors is None
    assert data is not None
    assert data.get('challengeAllocation') is not None
    assert data.get('challengeAllocation').get('success') is False

    errors = data.get('challengeAllocation').get('errors')
    assert 'employee' in errors


@pytest.mark.django_db
def test_allocation_as_company_with_challenge_of_student(user_employee, user_student,
                                                         company_challenge_object, login,
                                                         challenge_allocation):
    login(user_employee)
    company_challenge_object.form_step = 3
    company_challenge_object.company = None
    company_challenge_object.employee = None
    company_challenge_object.student = user_student.student
    company_challenge_object.save()
    data, errors = challenge_allocation(user_employee, company_challenge_object.id,
                                        ChallengeState.PUBLIC, user_employee.employee)
    assert errors is None
    assert data is not None
    assert data.get('challengeAllocation') is not None
    assert data.get('challengeAllocation').get('success') is False

    errors = data.get('challengeAllocation').get('errors')
    assert 'employee' in errors


@pytest.mark.django_db
def test_allocation_as_company_with_challenge_of_student_without_employee(
        user_employee, user_student, company_challenge_object, login, challenge_allocation):
    login(user_employee)
    company_challenge_object.form_step = 3
    company_challenge_object.company = None
    company_challenge_object.employee = None
    company_challenge_object.student = user_student.student
    company_challenge_object.save()
    data, errors = challenge_allocation(user_employee, company_challenge_object.id,
                                        ChallengeState.PUBLIC, None)
    assert errors is None
    assert data is not None
    assert data.get('challengeAllocation') is not None
    assert data.get('challengeAllocation').get('success') is False

    errors = data.get('challengeAllocation').get('errors')
    assert 'employee' in errors
