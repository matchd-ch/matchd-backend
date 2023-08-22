import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from db.models import Branch, Benefit


@pytest.mark.django_db
def test_advantages(login, user_employee, company_advantages, branch_objects, benefit_objects):
    login(user_employee)
    data, errors = company_advantages(user_employee, branch_objects, benefit_objects)
    assert errors is None
    assert data is not None
    assert data.get('companyProfileAdvantages') is not None
    assert data.get('companyProfileAdvantages').get('success')

    user = get_user_model().objects.get(pk=user_employee.id)
    assert len(user.company.branches.all()) == len(branch_objects)
    assert len(user.company.benefits.all()) == len(benefit_objects)


@pytest.mark.django_db
def test_advantages_without_login(user_employee, company_advantages, branch_objects,
                                  benefit_objects):
    data, errors = company_advantages(AnonymousUser(), branch_objects, benefit_objects)
    assert errors is not None
    assert data is not None
    assert data.get('companyProfileAdvantages') is None

    user = get_user_model().objects.get(pk=user_employee.id)
    assert len(user.company.branches.all()) == 0
    assert len(user.company.benefits.all()) == 0


@pytest.mark.django_db
def test_advantages_as_student(login, user_student, company_advantages, branch_objects,
                               benefit_objects):
    login(user_student)
    data, errors = company_advantages(user_student, branch_objects, benefit_objects)
    assert errors is None
    assert data is not None
    assert data.get('companyProfileAdvantages') is not None

    errors = data.get('companyProfileAdvantages').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_advantages_invalid_data(login, user_employee, company_advantages):
    login(user_employee)
    data, errors = company_advantages(user_employee, [Branch(id=1337)], [Benefit(id=1337)])
    assert errors is None
    assert data is not None
    assert data.get('companyProfileAdvantages') is not None
    assert data.get('companyProfileAdvantages').get('success') is False

    errors = data.get('companyProfileAdvantages').get('errors')
    assert errors is not None
    assert 'branches' in errors
    assert 'benefits' in errors
