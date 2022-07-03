import pytest

from django.conf import settings
from django.core import mail
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_update_user_student(login, user_student_full_profile, verification_url_and_token,
                             verify_account, update_user):
    login(user_student_full_profile)

    new_email = "changed@mail.com"

    user_data = {"email": new_email}

    data, errors = update_user(user_student_full_profile, user_data)
    assert errors is None
    assert data is not None
    assert data.get('updateUser').get('success')

    user = get_user_model().objects.get(email=new_email)
    assert user.email == new_email
    assert user.status.verified is False

    activation_email = mail.outbox[0]
    assert new_email in activation_email.recipients()
    assert settings.EMAIL_SUBJECT_PREFIX in activation_email.subject
    assert 'MATCHD Activation email' in activation_email.subject

    verification_url, token = verification_url_and_token(activation_email)
    verification_path = settings.GRAPHQL_AUTH.get('ACTIVATION_PATH_ON_EMAIL')
    assert f'{settings.FRONTEND_URL}/{verification_path}/' in verification_url
    assert token is not None

    data, errors = verify_account(token)
    assert errors is None
    assert data is not None
    assert data.get('verifyAccount') is not None
    assert data.get('verifyAccount').get('success')


@pytest.mark.django_db
def test_resend_email_activation(resend_activation_email, user_student_not_verified,
                                 verification_url_and_token, verify_account, data_protection_url):
    data, errors = resend_activation_email(user_student_not_verified.email)
    assert errors is None
    assert data is not None

    activation_email = mail.outbox[0]
    print(activation_email.recipients())
    assert user_student_not_verified.email in activation_email.recipients()
    assert settings.EMAIL_SUBJECT_PREFIX in activation_email.subject
    assert 'MATCHD Activation email' in activation_email.subject

    verification_url, token = verification_url_and_token(activation_email)
    verification_path = settings.GRAPHQL_AUTH.get('ACTIVATION_PATH_ON_EMAIL')
    assert f'{settings.FRONTEND_URL}/{verification_path}/' in verification_url
    assert token is not None

    data_protection_url = data_protection_url(activation_email)
    assert settings.DATA_PROTECTION_URL == data_protection_url

    data, errors = verify_account(token)
    assert errors is None
    assert data is not None
    assert data.get('verifyAccount') is not None
    assert data.get('verifyAccount').get('success')


@pytest.mark.django_db
def test_change_user_password(login, logout, user_student_full_profile, change_user_password,
                              default_password):
    login(user_student_full_profile)

    old_password = default_password
    new_password = "changedpassword1$"

    data, errors = change_user_password(user_student_full_profile, old_password, new_password)
    assert errors is None
    assert data is not None
    assert data.get('passwordChange').get('success') is True

    logout()

    data, errors = login(user_student_full_profile, new_password)
    assert errors is None
    assert data is not None

    assert data.get('tokenAuth') is not None
    assert data.get('tokenAuth').get('success') is True
    assert data.get('tokenAuth').get('token') is not None
