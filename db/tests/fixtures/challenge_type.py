import pytest

from db.models.challenge_type import ChallengeType


@pytest.fixture
def challenge_type_valid_args():
    return {'name': 'Smart'}


@pytest.fixture
def create_challenge_type():
    return ChallengeType.objects.create(name='Interesting')
