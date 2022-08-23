import pytest

from graphql_relay import to_global_id

from db.models import ChallengeType


def challenge_type_node_query():
    return '''
    query ($id: ID!) {
        node(id: $id) {
            id
            ... on ChallengeType {
                name
            }
        }
    }
    '''


def challenge_types_query():
    return '''
    query {
        challengeTypes(first: 3) {
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
def challenge_type_objects():
    return [
        ChallengeType.objects.create(name="Challenge Type 1"),
        ChallengeType.objects.create(name="Challenge Type 2"),
        ChallengeType.objects.create(name="Challenge Type 3")
    ]


@pytest.fixture
def query_challenge_type_node(execute):

    def closure(user, id_value):
        return execute(challenge_type_node_query(),
                       variables={'id': to_global_id('ChallengeType', id_value)},
                       **{'user': user})

    return closure


@pytest.fixture
def query_challenge_types(execute):

    def closure(user):
        return execute(challenge_types_query(), **{'user': user})

    return closure
