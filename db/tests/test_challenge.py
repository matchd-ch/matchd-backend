from datetime import datetime

import pytest

from db.models.company import Company
from db.models.employee import Employee
from db.models.challenge_type import ChallengeType
from db.models.challenge import Challenge
from db.models.student import Student


@pytest.mark.django_db
def test_create_challenge(challenge_valid_args):
    challenge = Challenge.objects.create(**challenge_valid_args)

    assert isinstance(challenge, Challenge)


@pytest.mark.django_db
def test_get_challenge(challenge_valid_args):
    challenge = Challenge.objects.create(**challenge_valid_args)
    challenge = Challenge.objects.get(id=challenge.id)

    assert isinstance(challenge, Challenge)
    assert isinstance(challenge.challenge_type, ChallengeType)
    assert isinstance(challenge.employee, Employee)
    assert isinstance(challenge.student, Student)
    assert isinstance(challenge.company, Company)
    assert isinstance(challenge.date_created, datetime)

    assert challenge.title == challenge_valid_args.get('title')
    assert challenge.slug == challenge_valid_args.get('slug')
    assert challenge.team_size == challenge_valid_args.get('team_size')
    assert challenge.compensation == challenge_valid_args.get('compensation')
    assert challenge.keywords.count() == 0


@pytest.mark.django_db
def test_update_challenge(challenge_valid_args):
    new_title = 'A challenge'
    challenge = Challenge.objects.create(**challenge_valid_args)
    Challenge.objects.filter(id=challenge.id).update(title=new_title)
    challenge.refresh_from_db()

    assert isinstance(challenge, Challenge)
    assert isinstance(challenge.title, str)

    assert challenge.title == new_title


@pytest.mark.django_db
def test_delete_challenge(challenge_valid_args):
    challenge = Challenge.objects.create(**challenge_valid_args)
    number_of_deletions, _ = challenge.delete()

    assert number_of_deletions == 1
