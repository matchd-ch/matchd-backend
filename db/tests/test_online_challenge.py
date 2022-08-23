import pytest

from db.models.online_challenge import OnlineChallenge
from db.models.student import Student


@pytest.mark.django_db
def test_create_online_challenge(online_challenge_valid_args):
    online_challenge = OnlineChallenge.objects.create(**online_challenge_valid_args)

    assert isinstance(online_challenge, OnlineChallenge)


@pytest.mark.django_db
def test_get_online_challenge(online_challenge_valid_args):
    online_challenge = OnlineChallenge.objects.create(**online_challenge_valid_args)
    online_challenge = OnlineChallenge.objects.get(id=online_challenge.id)

    assert isinstance(online_challenge, OnlineChallenge)
    assert isinstance(online_challenge.url, str)
    assert isinstance(online_challenge.student, Student)

    assert online_challenge.url == online_challenge_valid_args.get('url')
    assert online_challenge.student.slug == online_challenge_valid_args.get('student').slug


@pytest.mark.django_db
def test_update_online_challenge(online_challenge_valid_args):
    new_url = 'www.awesomejob.ch'
    online_challenge = OnlineChallenge.objects.create(**online_challenge_valid_args)
    OnlineChallenge.objects.filter(id=online_challenge.id).update(url=new_url)
    online_challenge.refresh_from_db()

    assert isinstance(online_challenge, OnlineChallenge)
    assert isinstance(online_challenge.url, str)

    assert online_challenge.url == new_url


@pytest.mark.django_db
def test_delete_online_challenge(online_challenge_valid_args):
    online_challenge = OnlineChallenge.objects.create(**online_challenge_valid_args)
    number_of_deletions, _ = online_challenge.delete()

    assert number_of_deletions == 1
