import pytest

from api.tests.helpers.node_helper import b64encode_string

from db.models import Keyword


def keyword_node_query(node_id):
    b64_encoded_id = b64encode_string(node_id)
    return '''
    query {
        node(id: "%s") {
            id
            ... on Keyword {
                name
            }
        }
    }
    ''' % b64_encoded_id


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
    return [
        Keyword.objects.create(name="Keyword 2"),
        Keyword.objects.create(name="Keyword 1")
    ]


@pytest.fixture
def query_keyword_node(execute):
    def closure(user, node_id):
        return execute(keyword_node_query(node_id), **{'user': user})
    return closure


@pytest.fixture
def query_keywords(execute):
    def closure(user):
        return execute(keywords_query(), **{'user': user})
    return closure
