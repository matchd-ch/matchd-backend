import pytest

from graphql_relay import to_global_id

from db.models import LanguageLevel


def language_level_node_query():
    return '''
    query ($id: ID!) {
        node(id: $id) {
            id
            ... on LanguageLevel {
                level
            }
        }
    }
    '''


def language_levels_query():
    return '''
    query {
        languageLevels(first: 3) {
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
                    level
                    description
                }
            }
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
def query_language_level_node(execute):
    def closure(user, id_value):
        return execute(
            language_level_node_query(), variables={'id': to_global_id('LanguageLevel', id_value)}, **{'user': user}
        )
    return closure


@pytest.fixture
def query_language_levels(execute):
    def closure(user):
        return execute(language_levels_query(), **{'user': user})
    return closure
