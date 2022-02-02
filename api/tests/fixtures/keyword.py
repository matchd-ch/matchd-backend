import pytest

from graphql_relay import to_global_id

from db.models import Keyword


def keyword_node_query():
    return '''
    query ($id: ID!) {
        node(id: $id) {
            id
            ... on Keyword {
                name
            }
        }
    }
    '''


def keywords_query():
    return '''
    query {
        keywords(first: 2) {
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
def keyword_objects():
    return [Keyword.objects.create(name="Keyword 2"), Keyword.objects.create(name="Keyword 1")]


@pytest.fixture
def query_keyword_node(execute):

    def closure(user, id_value):
        return execute(keyword_node_query(),
                       variables={'id': to_global_id('Keyword', id_value)},
                       **{'user': user})

    return closure


@pytest.fixture
def query_keywords(execute):

    def closure(user):
        return execute(keywords_query(), **{'user': user})

    return closure
