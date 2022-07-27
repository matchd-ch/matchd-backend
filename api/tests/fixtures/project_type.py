import pytest

from graphql_relay import to_global_id

from db.models import ProjectType


def project_type_node_query():
    return '''
    query ($id: ID!) {
        node(id: $id) {
            id
            ... on ProjectType {
                name
            }
        }
    }
    '''


def project_types_query():
    return '''
    query {
        projectTypes(first: 3) {
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
        ProjectType.objects.create(name="Project Type 2"),
        ProjectType.objects.create(name="Project Type 3")
    ]


@pytest.fixture
def query_project_type_node(execute):

    def closure(user, id_value):
        return execute(project_type_node_query(),
                       variables={'id': to_global_id('ProjectType', id_value)},
                       **{'user': user})

    return closure


@pytest.fixture
def query_project_types(execute):

    def closure(user):
        return execute(project_types_query(), **{'user': user})

    return closure
