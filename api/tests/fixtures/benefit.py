import pytest

from graphql_relay import to_global_id

from db.models import Benefit


def benefit_node_query():
    return '''
    query ($id: ID!) {
        node(id: $id) {
            id
            ... on Benefit {
                name
            }
        }
    }
    '''


def benefits_query():
    return '''
    query {
        benefits(first: 2) {
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
def benefit_objects():
    return [
        Benefit.objects.create(name="Massage", icon='spa'),
        Benefit.objects.create(name="Laptop", icon='laptop')
    ]


@pytest.fixture
def query_benefits(execute):
    def closure(user):
        return execute(benefits_query(), **{'user': user})
    return closure

@pytest.fixture
def query_benefit_node(execute):
    def closure(user, id_value):
        return execute(
            benefit_node_query(), variables={'id': to_global_id('Benefit', id_value)}, **{'user': user}
        )
    return closure
