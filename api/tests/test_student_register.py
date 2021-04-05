import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail

from db.models import ProfileType, ProfileState


@pytest.mark.django_db
def test_register_student(register_student, verification_url_and_token, verify_account):
    username = 'student@matchd.test'
    data, errors = register_student(username, 'John', 'Doe', '+41791234567')
    assert errors is None
    assert data is not None
    assert data.get('registerStudent').get('success')
    assert data.get('registerStudent').get('errors') is None

    user = get_user_model().objects.get(email=username)
    assert user.first_name == 'John'
    assert user.last_name == 'Doe'
    assert user.email == username
    assert user.type == ProfileType.STUDENT
    assert user.student is not None
    assert user.student.mobile == '+41791234567'
    assert user.student.state == ProfileState.INCOMPLETE
    assert user.student.profile_step == 1
    assert user.status.verified is False

    activation_email = mail.outbox[0]
    assert username in activation_email.recipients()
    assert settings.EMAIL_SUBJECT_PREFIX in activation_email.subject
    assert 'MATCHD Registration Student' in activation_email.subject

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
def test_register_existing_username(register_student, user_student):
    data, errors = register_student(user_student.username, 'John', 'Doe', '+41791234567')
    assert errors is None
    assert data is not None
    assert data.get('registerStudent').get('success') is False

    errors = data.get('registerStudent').get('errors')
    assert errors is not None
    assert 'username' in errors


@pytest.mark.django_db
def test_register_with_weak_password(register_student, weak_passwords):
    for password, code in weak_passwords:
        username = 'student@matchd.test'
        data, errors = register_student(username, 'John', 'Doe', '+41791234567', password)
        assert errors is None
        assert data is not None
        assert data.get('registerStudent').get('success') is False

        errors = data.get('registerStudent').get('errors')
        assert errors is not None
        assert 'password2' in errors
        assert errors.get('password2')[0].get('code') == code


@pytest.mark.django_db
def test_register_student_with_invalid_data(register_student):
    username = 'invalid'
    data, errors = register_student(username, '', '', '')
    assert errors is None
    assert data is not None
    assert data.get('registerStudent').get('success') is False

    errors = data.get('registerStudent').get('errors')
    assert errors is not None
    assert 'email' in errors
    assert 'firstName' in errors
    assert 'lastName' in errors
    assert 'mobile' not in errors