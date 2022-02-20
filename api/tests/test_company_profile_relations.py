import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_relations(login, user_employee, company_relations):
    user_employee.company.profile_step = 2
    user_employee.company.save()
    login(user_employee)
    data, errors = company_relations(user_employee, 'http://www.1337.lo', 'description', 'services',
                                     True)
    assert errors is None
    assert data is not None
    assert data.get('companyProfileRelations') is not None
    assert data.get('companyProfileRelations').get('success')

    user = get_user_model().objects.get(pk=user_employee.id)
    assert user.company.website == 'http://www.1337.lo'
    assert user.company.description == 'description'
    assert user.company.services == 'services'
    assert user.company.member_it_st_gallen
    assert user.company.profile_step == 3


@pytest.mark.django_db
def test_relations_without_login(user_employee, company_relations):
    data, errors = company_relations(AnonymousUser(), 'http://www.1337.lo', 'description',
                                     'services', True)
    assert errors is not None
    assert data is not None
    assert data.get('companyProfileRelations') is None

    user = get_user_model().objects.get(pk=user_employee.id)
    assert user.company.website == ''
    assert user.company.description == ''
    assert user.company.services == ''
    assert user.company.member_it_st_gallen is False
    assert user.company.profile_step == 1


@pytest.mark.django_db
def test_relations_as_student(login, user_student, company_relations):
    login(user_student)
    data, errors = company_relations(user_student, 'http://www.1337.lo', 'description', 'services',
                                     True)
    assert errors is None
    assert data is not None
    assert data.get('companyProfileRelations') is not None

    errors = data.get('companyProfileRelations').get('errors')
    assert errors is not None
    assert 'type' in errors


@pytest.mark.django_db
def test_relations_invalid_step(login, user_employee, company_relations):
    user_employee.company.profile_step = 0
    user_employee.company.save()
    login(user_employee)
    data, errors = company_relations(user_employee, 'http://www.1337.lo', 'description', 'services',
                                     True)
    assert errors is None
    assert data is not None
    assert data.get('companyProfileRelations') is not None
    assert data.get('companyProfileRelations').get('success') is False

    errors = data.get('companyProfileRelations').get('errors')
    assert errors is not None
    assert 'profileStep' in errors

    user = get_user_model().objects.get(pk=user_employee.id)
    assert user.company.profile_step == 0


@pytest.mark.django_db
def test_relations_invalid_data(login, user_employee, company_relations):
    user_employee.company.profile_step = 2
    user_employee.company.save()
    login(user_employee)
    data, errors = company_relations(user_employee, '', '', '', '')
    assert errors is None
    assert data is not None
    assert data.get('companyProfileRelations') is not None
    assert data.get('companyProfileRelations').get('success') is False

    errors = data.get('companyProfileRelations').get('errors')
    assert errors is not None
    assert 'website' in errors

    user = get_user_model().objects.get(pk=user_employee.id)
    assert user.company.profile_step == 2
