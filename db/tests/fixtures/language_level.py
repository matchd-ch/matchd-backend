import pytest

from db.models.language_level import LanguageLevel


@pytest.fixture
def language_level_valid_args():
    return {'level': 'C1', 'description': 'Advanced', 'value': 5}


@pytest.fixture
def create_language_level():
    return LanguageLevel.objects.create(level='A1', description='Beginner', value=1)
