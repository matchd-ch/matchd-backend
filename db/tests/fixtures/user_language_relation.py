import pytest


@pytest.fixture
def user_language_relation_valid_args(create_student, create_language, create_language_level):
    return {
        'student': create_student,
        'language': create_language('German'),
        'language_level': create_language_level
    }
