import pytest

from graphql_relay import to_global_id

from db.models import Branch


def branch_node_query():
    return '''
    query ($id: ID!) {
        node(id: $id) {
            id
            ... on Branch {
                name
            }
        }
    }
    '''

def branches_query():
    return '''
    query {
        branches(first: 2) {
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
def branch_objects():
    return [
        Branch.objects.create(name="Systemtechnik", ),
        Branch.objects.create(name="Applikationsentwicklung", )
    ]


@pytest.fixture
def query_branch_node(execute):
    def closure(user, id_value):
        return execute(
            branch_node_query(), variables={'id': to_global_id('Branch', id_value)}, **{'user': user}
        )
    return closure


@pytest.fixture
def query_branches(execute):
    def closure(user):
        return execute(branches_query(), **{'user': user})
    return closure
