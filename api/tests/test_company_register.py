import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail

from db.models import ProfileType, ProfileState, Company


@pytest.mark.django_db
def test_register_company(register_company, verification_url_and_token, verify_account):
    username = 'employee@matchd.test'
    data, errors = register_company(username, 'John', 'Doe', 'Role', 'Company name', 'CHE-999.999.999')
    assert errors is None
    assert data is not None
    assert data.get('registerCompany').get('success')
    assert data.get('registerCompany').get('errors') is None

    user = get_user_model().objects.get(email=username)
    assert user.first_name == 'John'
    assert user.last_name == 'Doe'
    assert user.email == username
    assert user.type == ProfileType.COMPANY
    assert user.company is not None
    assert user.company.name == 'Company name'
    assert user.company.state == ProfileState.INCOMPLETE
    assert user.company.profile_step == 1
    assert user.company.type == ProfileType.COMPANY

    activation_email = mail.outbox[0]
    assert username in activation_email.recipients()
    assert settings.EMAIL_SUBJECT_PREFIX in activation_email.subject
    assert 'MATCHD Registration Company' in activation_email.subject

    verification_url, token = verification_url_and_token(activation_email)
    verification_path = settings.GRAPHQL_AUTH.get('ACTIVATION_PATH_ON_EMAIL')
    assert f'https://{settings.FRONTEND_URL}/{verification_path}/' in verification_url
    assert token is not None

    data, errors = verify_account(token)
    assert errors is None
    assert data is not None
    assert data.get('verifyAccount') is not None
    assert data.get('verifyAccount').get('success')


@pytest.mark.django_db
def test_register_existing_username(register_company, user_employee):
    data, errors = register_company(user_employee.username, 'John', 'Doe', 'Role', 'Company name', 'CHE-999.999.999')
    assert errors is None
    assert data is not None
    assert data.get('registerCompany').get('success') is False

    errors = data.get('registerCompany').get('errors')
    assert errors is not None
    assert 'username' in errors


@pytest.mark.django_db
def test_register_with_same_company_name(register_company):
    data, errors = register_company('employee@matchd.test', 'John', 'Doe', 'Role', 'Company name', 'CHE-999.999.999')
    assert errors is None
    assert data is not None
    assert data.get('registerCompany').get('success')

    data, errors = register_company('employee-2@matchd.test', 'John', 'Doe', 'Role', 'Company name', 'CHE-999.999.999')
    assert errors is None
    assert data is not None
    assert data.get('registerCompany').get('success')

    companies = Company.objects.all().order_by('id')
    assert companies[0].slug == 'company-name'
    assert companies[1].slug == 'company-name-1'


@pytest.mark.django_db
def test_register_with_weak_password(register_company, weak_passwords):
    for password, code in weak_passwords:
        username = 'student@matchd.test'
        data, errors = register_company(username, 'John', 'Doe', 'Role', 'company name', 'CHE-999.999.999', password)
        assert errors is None
        assert data is not None
        assert data.get('registerCompany').get('success') is False

        errors = data.get('registerCompany').get('errors')
        assert errors is not None
        assert 'password2' in errors
        assert errors.get('password2')[0].get('code') == code


@pytest.mark.django_db
def test_register_company_with_invalid_data(register_company):
    username = 'invalid'
    data, errors = register_company(username, '', '', '', '', '')
    assert errors is None
    assert data is not None
    assert data.get('registerCompany').get('success') is False

    errors = data.get('registerCompany').get('errors')
    assert errors is not None
    assert 'email' in errors
    assert 'firstName' in errors
    assert 'lastName' in errors
    assert 'role' in errors
    assert 'name' in errors
    assert 'slug' in errors
    assert 'uid' in errors
