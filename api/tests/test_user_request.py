import pytest
from django.conf import settings
from django.core import mail

from db.models import UserRequest


@pytest.mark.django_db
def test_user_request(user_request):
    data, errors = user_request('John Doe', 'test@matchd.test', 'Some message')
    assert errors is None
    assert data is not None
    assert data.get('userRequest') is not None
    assert data.get('userRequest').get('success')

    entries = UserRequest.objects.all()
    assert 1 == len(entries)
    assert entries[0].email == 'test@matchd.test'
    assert entries[0].name == 'John Doe'
    assert entries[0].message == 'Some message'

    request_email_copy = mail.outbox[0]
    assert 'test@matchd.test' in request_email_copy.recipients()
    assert 'John Doe', request_email_copy.body
    assert 'test@matchd.test' in request_email_copy.body
    assert 'Some message' in request_email_copy.body
    assert settings.EMAIL_SUBJECT_PREFIX, request_email_copy.subject

    request_email = mail.outbox[1]
    for recipient in settings.USER_REQUEST_FORM_RECIPIENTS:
        assert recipient in request_email.recipients()
    assert 'John Doe', request_email.body
    assert 'test@matchd.test' in request_email.body
    assert 'Some message' in request_email.body
    assert settings.EMAIL_SUBJECT_PREFIX, request_email.subject


@pytest.mark.django_db
def test_user_request_without_data(user_request):
    data, errors = user_request('', '', '')
    assert errors is None
    assert data is not None
    assert data.get('userRequest') is not None
    assert data.get('userRequest').get('success') is False

    errors = data.get('userRequest').get('errors')
    assert errors is not None
    assert 'name' in errors
    assert 'email' in errors
    assert 'message' in errors


@pytest.mark.django_db
def test_user_request_with_invalid_data(user_request):
    data, errors = user_request('', 'invalid', '')
    assert errors is None
    assert data is not None
    assert data.get('userRequest') is not None
    assert data.get('userRequest').get('success') is False

    errors = data.get('userRequest').get('errors')
    assert errors is not None
    assert 'name' in errors
    assert 'email' in errors
    assert 'message' in errors
