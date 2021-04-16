import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from db.models import Branch, Benefit


@pytest.mark.django_db
def test_step_3(login, user_employee, company_step_3, branch_objects, benefit_objects):
    user_employee.company.profile_step = 3
    user_employee.company.save()
    login(user_employee)
    data, errors = company_step_3(user_employee, branch_objects, benefit_objects)
    assert errors is None
    assert data is not None
    assert data.get('companyProfileStep3') is not None
    assert data.get('companyProfileStep3').get('success')

    user = get_user_model().objects.get(pk=user_employee.id)
    assert len(user.company.branches.all()) == len(branch_objects)
    assert len(user.company.benefits.all()) == len(benefit_objects)
    assert user.company.profile_step == 4


@pytest.mark.django_db
def test_step_3_without_login(user_employee, company_step_3, branch_objects, benefit_objects):
    data, errors = company_step_3(AnonymousUser(), branch_objects, benefit_objects)
    assert errors is not None
    assert data is not None
    assert data.get('companyProfileStep3') is None

    user = get_user_model().objects.get(pk=user_employee.id)
    assert len(user.company.branches.all()) == 0
    assert len(user.company.benefits.all()) == 0
    assert user.company.profile_step == 1


@pytest.mark.django_db
def test_step_3_as_student(login, user_student, company_step_3, branch_objects, benefit_objects):
    login(user_student)
    data, errors = company_step_3(user_student, branch_objects, benefit_objects)
    assert errors is None
    assert data is not None
    assert data.get('companyProfileStep3') is not None

    errors = data.get('companyProfileStep3').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_step_3_invalid_step(login, user_employee, company_step_3, branch_objects, benefit_objects):
    user_employee.company.profile_step = 0
    user_employee.company.save()
    login(user_employee)
    data, errors = company_step_3(user_employee, branch_objects, benefit_objects)
    assert errors is None
    assert data is not None
    assert data.get('companyProfileStep3') is not None
    assert data.get('companyProfileStep3').get('success') is False

    errors = data.get('companyProfileStep3').get('errors')
    assert errors is not None
    assert 'profileStep' in errors

    user = get_user_model().objects.get(pk=user_employee.id)
    assert user.company.profile_step == 0


@pytest.mark.django_db
def test_step_3_invalid_data(login, user_employee, company_step_3):
    user_employee.company.profile_step = 3
    user_employee.company.save()
    login(user_employee)
    data, errors = company_step_3(user_employee, [Branch(id=1337)], [Benefit(id=1337)])
    assert errors is None
    assert data is not None
    assert data.get('companyProfileStep3') is not None
    assert data.get('companyProfileStep3').get('success') is False

    errors = data.get('companyProfileStep3').get('errors')
    assert errors is not None
    assert 'branches' in errors
    assert 'benefits' in errors

    user = get_user_model().objects.get(pk=user_employee.id)
    assert user.company.profile_step == 3
