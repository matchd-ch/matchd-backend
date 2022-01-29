import pytest

from graphql_relay import to_global_id

from db.models import Topic


def topic_node_query():
    return '''
    query ($id: ID!) {
        node(id: $id) {
            id
            ... on Topic {
                name
            }
        }
    }
    '''


def topics_query():
    return '''
    query {
        topics(first: 2) {
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
def topic_objects():
    return [
        Topic.objects.create(name="Topic 1"),
        Topic.objects.create(name="Topic 2")
    ]


@pytest.fixture
def query_topic_node(execute):
    def closure(user, id_value):
        return execute(
            topic_node_query(), variables={'id': to_global_id('Topic', id_value)}, **{'user': user}
        )
    return closure


@pytest.fixture
def query_topics(execute):
    def closure(user):
        return execute(topics_query(), **{'user': user})
    return closure
