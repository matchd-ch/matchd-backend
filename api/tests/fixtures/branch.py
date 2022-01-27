import pytest

from api.tests.helpers.node_helper import b64encode_string

from db.models import Branch


def branch_node_query(node_id):
    b64_encoded_id = b64encode_string(node_id)
    return '''
    query {
        node(id: "%s") {
            id
            ... on Branch {
                name
            }
        }
    }
    ''' % b64_encoded_id

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
    def closure(user, node_id):
        return execute(branch_node_query(node_id), **{'user': user})
    return closure


@pytest.fixture
def query_branches(execute):
    def closure(user):
        return execute(branches_query(), **{'user': user})
    return closure
