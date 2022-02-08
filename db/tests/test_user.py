import pytest

from django.contrib.auth import get_user_model

from db.models import User
from db.models.company import Company


@pytest.mark.django_db
def test_custom_user_model():
    user_model = get_user_model()
    assert user_model == User


@pytest.mark.django_db
def test_create_user(user_valid_args):
    user = User.objects.create(**user_valid_args)

    assert isinstance(user, User)


@pytest.mark.django_db
def test_get_user(user_valid_args):
    user = User.objects.create(**user_valid_args)
    user = User.objects.get(id=user.id)

    assert isinstance(user, User)
    assert isinstance(user.first_name, str)
    assert isinstance(user.last_name, str)
    assert isinstance(user.company, Company)

    assert user.first_name == user_valid_args.get('first_name')
    assert user.last_name == user_valid_args.get('last_name')
    assert user.company.name == user_valid_args.get('company').name


@pytest.mark.django_db
def test_update_user(user_valid_args):
    new_first_name = 'Mario'
    user = User.objects.create(**user_valid_args)
    User.objects.filter(id=user.id).update(first_name=new_first_name)
    user.refresh_from_db()

    assert isinstance(user, User)
    assert isinstance(user.first_name, str)

    assert user.first_name == new_first_name


@pytest.mark.django_db
def test_delete_user(user_valid_args):
    user = User.objects.create(**user_valid_args)
    number_of_deletions, _ = user.delete()

    assert number_of_deletions == 2
