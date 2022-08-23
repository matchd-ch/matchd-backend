import pytest

from db.models.challenge_type import ChallengeType


@pytest.mark.django_db
def test_create_challenge_isinstance(challenge_type_valid_args):
    challenge_type = ChallengeType.objects.create(**challenge_type_valid_args)

    assert isinstance(challenge_type, ChallengeType)


@pytest.mark.django_db
def test_get_challenge_isinstance(challenge_type_valid_args):
    challenge_type = ChallengeType.objects.create(**challenge_type_valid_args)
    challenge_type = ChallengeType.objects.get(id=challenge_type.id)

    assert isinstance(challenge_type, ChallengeType)
    assert isinstance(challenge_type.name, str)

    assert challenge_type.name == challenge_type_valid_args.get('name')


@pytest.mark.django_db
def test_update_challenge_isinstance(challenge_type_valid_args):
    new_name = 'rich'
    challenge_type = ChallengeType.objects.create(**challenge_type_valid_args)
    ChallengeType.objects.filter(id=challenge_type.id).update(name=new_name)
    challenge_type.refresh_from_db()

    assert isinstance(challenge_type, ChallengeType)
    assert isinstance(challenge_type.name, str)

    assert challenge_type.name == new_name


@pytest.mark.django_db
def test_delete_challenge_isinstance(challenge_type_valid_args):
    challenge_type = ChallengeType.objects.create(**challenge_type_valid_args)
    number_of_deletions, _ = challenge_type.delete()

    assert number_of_deletions == 1
