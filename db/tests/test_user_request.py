from datetime import datetime
import pytest

from db.models.user_request import UserRequest


@pytest.mark.django_db
def test_create_user_request(user_request_valid_args):
    user_request = UserRequest.objects.create(**user_request_valid_args)

    assert isinstance(user_request, UserRequest)


@pytest.mark.django_db
def test_get_user_request(user_request_valid_args):
    user_request = UserRequest.objects.create(**user_request_valid_args)
    user_request = UserRequest.objects.get(id=user_request.id)

    assert isinstance(user_request, UserRequest)
    assert isinstance(user_request.created_at, datetime)

    assert user_request.name == user_request_valid_args.get('name')
    assert user_request.email == user_request_valid_args.get('email')
    assert user_request.message == user_request_valid_args.get('message')


@pytest.mark.django_db
def test_update_user_request(user_request_valid_args):
    new_name = 'Take money'
    user_request = UserRequest.objects.create(**user_request_valid_args)
    UserRequest.objects.filter(id=user_request.id).update(name=new_name)
    user_request.refresh_from_db()

    assert isinstance(user_request, UserRequest)
    assert isinstance(user_request.name, str)

    assert user_request.name == new_name


@pytest.mark.django_db
def test_delete_user_request(user_request_valid_args):
    user_request = UserRequest.objects.create(**user_request_valid_args)
    number_of_deletions, _ = user_request.delete()

    assert number_of_deletions == 1
