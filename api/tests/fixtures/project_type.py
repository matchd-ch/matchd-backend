import pytest

from api.tests.helpers.node_helper import b64encode_string

from db.models import ProjectType


def project_type_node_query(node_id):
    b64_encoded_id = b64encode_string(node_id)
    return '''
    query {
        node(id: "%s") {
            id
            ... on ProjectType {
                name
            }
        }
    }
    ''' % b64_encoded_id


def project_types_query():
    return '''
    query {
        projectTypes(first: 2) {
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
def project_type_objects():
    return [
        ProjectType.objects.create(name="Project Type 1"),
        ProjectType.objects.create(name="Project Type 2")
    ]


@pytest.fixture
def query_project_type_node(execute):
    def closure(user, node_id):
        return execute(project_type_node_query(node_id), **{'user': user})
    return closure


@pytest.fixture
def query_project_types(execute):
    def closure(user):
        return execute(project_types_query(), **{'user': user})
    return closure
