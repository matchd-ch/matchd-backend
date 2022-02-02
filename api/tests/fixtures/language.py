import pytest

from graphql_relay import to_global_id

from db.models import Language

# pylint: disable=W0621


def language_node_query():
    return '''
    query ($id: ID!) {
        node(id: $id) {
            id
            ... on Language {
                name
            }
        }
    }
    '''


def languages_query():
    return '''
    query {
        languages(first: 4) {
            pageInfo {
                startCursor
                endCursor
                hasNextPage
                hasPreviousPage
            }
            edges {
                cursor
                node {
                    id
                    name
                }
            }
        }
    }
    '''


def languages_shortlist_query():
    return '''
    query {
        languages(first: 4, shortList: true) {
            pageInfo {
                startCursor
                endCursor
                hasNextPage
                hasPreviousPage
            }
            edges {
                cursor
                node {
                    id
                    name
                }
            }
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
def query_language_node(execute):

    def closure(user, id_value):
        return execute(language_node_query(),
                       variables={'id': to_global_id('Language', id_value)},
                       **{'user': user})

    return closure


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
