import pytest


@pytest.fixture
def hobby_valid_args(create_student):
    return {'name': 'fishing', 'student': create_student}
