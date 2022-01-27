import pytest

from api.tests.helpers.node_helper import b64encode_string

from db.models import Topic


def topic_node_query(node_id):
    b64_encoded_id = b64encode_string(node_id)
    return '''
    query {
        node(id: "%s") {
            id
            ... on Topic {
                name
            }
        }
    }
    ''' % b64_encoded_id


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
    def closure(user, node_id):
        return execute(topic_node_query(node_id), **{'user': user})
    return closure


@pytest.fixture
def query_topics(execute):
    def closure(user):
        return execute(topics_query(), **{'user': user})
    return closure
