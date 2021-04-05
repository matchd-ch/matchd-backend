import pytest
from django.conf import settings
from django.core import mail


@pytest.mark.django_db
def test_login_not_verified(login, user_student_not_verified):
    data, errors = login(user_student_not_verified)
    assert errors is None
    assert data is not None
    assert data.get('tokenAuth') is not None
    assert data.get('tokenAuth').get('success') is False


@pytest.mark.django_db
def test_login_wrong_password(login, user_student):
    data, errors = login(user_student, 'wrong password')
    assert errors is None
    assert data is not None
    assert data.get('tokenAuth') is not None
    assert data.get('tokenAuth').get('success') is False
    assert data.get('tokenAuth').get('token') is None


@pytest.mark.django_db
def test_login_logout(login, logout, user_student):
    data, errors = login(user_student)
    assert errors is None
    assert data is not None
    assert data.get('tokenAuth') is not None
    assert data.get('tokenAuth').get('success')
    assert data.get('tokenAuth').get('token') is not None
    # TODO test JWT cookie

    data, errors = logout()
    assert errors is None
    assert data is not None
    assert data.get('logout')
    # TODO test JWT cookie


@pytest.mark.django_db
def test_send_password_mail_and_reset_password(send_password_reset_mail, user_student, reset_url_and_token,
                                               reset_password, verify_password_reset_token):
    data, errors = send_password_reset_mail(user_student)
    assert errors is None
    assert data is not None
    assert data.get('sendPasswordResetEmail') is not None
    assert data.get('sendPasswordResetEmail').get('success')

    reset_email = mail.outbox[0]
    reset_url, token = reset_url_and_token(reset_email)
    verification_path = settings.GRAPHQL_AUTH.get('PASSWORD_RESET_PATH_ON_EMAIL')
    assert f'https://{settings.FRONTEND_URL}/{verification_path}/' in reset_url
    assert token is not None

    data, errors = verify_password_reset_token(token)
    assert errors is None
    assert data is not None
    assert data.get('verifyPasswordResetToken')

    data, errors = reset_password(token, 'weakPassword', 'weakPassword')
    assert errors is None
    assert data is not None
    assert data.get('passwordReset').get('success') is False

    errors = data.get('passwordReset').get('errors')
    assert errors is not None
    assert 'newPassword2' in errors

    data, errors = reset_password(token, 'weakPassword', 'weakPasswordButNotTheSame')
    assert errors is None
    assert data is not None
    assert data.get('passwordReset').get('success') is False

    errors = data.get('passwordReset').get('errors')
    assert errors is not None
    assert 'newPassword2' in errors

    data, errors = reset_password(token, 'superStrongPassword1!', 'superStrongPassword1!')
    assert errors is None
    assert data is not None
    assert data.get('passwordReset').get('success')


@pytest.mark.django_db
def test_reset_password_token_with_invalid_token(reset_password):
    data, errors = reset_password('invalid_token', 'superStrongPassword1!', 'superStrongPassword1!')
    assert errors is None
    assert data is not None
    assert data.get('passwordReset').get('success') is False

    errors = data.get('passwordReset').get('errors')
    assert errors is not None
    assert 'nonFieldErrors' in errors
    assert errors.get('nonFieldErrors')[0].get('code') == 'invalid_token'
