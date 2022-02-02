import pytest

from graphql_relay import to_global_id

from db.models import JobRequirement


def job_requirement_node_query():
    return '''
    query ($id: ID!) {
        node(id: $id) {
            id
            ... on JobRequirement {
                name
            }
        }
    }
    '''


def job_requirements_query():
    return '''
    query {
        jobRequirements(first: 2) {
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
def job_requirement_objects():
    return [
        JobRequirement.objects.create(name="Berufsmaturität (BMS)", ),
        JobRequirement.objects.create(name="abgeschlossene Volksschule", )
    ]


@pytest.fixture
def query_job_requirement_node(execute):

    def closure(user, id_value):
        return execute(job_requirement_node_query(),
                       variables={'id': to_global_id('JobRequirement', id_value)},
                       **{'user': user})

    return closure


@pytest.fixture
def query_job_requirements(execute):

    def closure(user):
        return execute(job_requirements_query(), **{'user': user})

    return closure
