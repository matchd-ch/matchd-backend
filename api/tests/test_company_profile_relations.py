import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_relations(login, user_employee, company_relations):
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
def test_relations_empty_data(login, user_employee, company_relations):
    login(user_employee)
    data, errors = company_relations(user_employee, '', '', '', False)
    assert errors is None
    assert data is not None
    assert data.get('companyProfileRelations') is not None
    assert data.get('companyProfileRelations').get('success') is True

    errors = data.get('companyProfileRelations').get('errors')
    assert errors is None
