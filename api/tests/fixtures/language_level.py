import pytest

from db.models import LanguageLevel


def language_levels_query():
    return '''
    query {
        languageLevels {
            id
            level
            description
        }
    }
    '''


@pytest.fixture
def language_level_objects():
    return [
        LanguageLevel.objects.create(id=1, level="A1", value=1),
        LanguageLevel.objects.create(id=2, level="B1", value=2),
        LanguageLevel.objects.create(id=3, level="A2", value=3)
    ]


@pytest.fixture
def query_language_levels(execute):
    def closure(user):
        return execute(language_levels_query(), **{'user': user})
    return closure
