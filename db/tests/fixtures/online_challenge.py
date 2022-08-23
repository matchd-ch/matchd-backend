import pytest


@pytest.fixture
def online_challenge_valid_args(create_student):
    return {'url': 'www.challenge.ch', 'student': create_student}
