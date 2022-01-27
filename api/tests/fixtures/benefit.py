import pytest

from api.tests.helpers.node_helper import b64encode_string

from db.models import Benefit


def benefit_node_query(node_id):
    b64_encoded_id = b64encode_string(node_id)
    return '''
    query {
        node(id: "%s") {
            id
            ... on Benefit {
                name
            }
        }
    }
    ''' % b64_encoded_id


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
    def closure(user, node_id):
        return execute(benefit_node_query(node_id), **{'user': user})
    return closure
