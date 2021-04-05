import pytest

from db.models import Language


def languages_query():
    return '''
    query {
        languages {
            id
            name
        }
    }
    '''


def languages_shortlist_query():
    return '''
    query {
        languages(shortList: true) {
            id
            name
        }
    }
    '''


@pytest.fixture
def language_objects():
    return [
        Language.objects.create(id=1, name='Zulu'),
        Language.objects.create(id=2, name='Deutsch', short_list=True),
        Language.objects.create(id=3, name='Englisch'),
        Language.objects.create(id=4, name='Spanisch', short_list=True)
    ]


@pytest.fixture
def query_languages(execute):
    def closure(user):
        return execute(languages_query(), **{'user': user})
    return closure


@pytest.fixture
def query_languages_shortlist(execute):
    def closure(user):
        return execute(languages_shortlist_query(), **{'user': user})
    return closure


@pytest.fixture
def language_shortlist_objects(language_objects):
    short_list = []
    for language in language_objects:
        if language.short_list:
            short_list.append(language)
    return short_list


@pytest.fixture
def language_no_shortlist_objects(language_objects):
    short_list = []
    for language in language_objects:
        if not language.short_list:
            short_list.append(language)
    return short_list
