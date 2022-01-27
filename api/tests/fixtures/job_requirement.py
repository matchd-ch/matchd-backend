import pytest

from api.tests.helpers.node_helper import b64encode_string

from db.models import JobRequirement


def job_requirement_node_query(node_id):
    b64_encoded_id = b64encode_string(node_id)
    return '''
    query {
        node(id: "%s") {
            id
            ... on JobRequirement {
                name
            }
        }
    }
    ''' % b64_encoded_id


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
    def closure(user, node_id):
        return execute(job_requirement_node_query(node_id), **{'user': user})
    return closure


@pytest.fixture
def query_job_requirements(execute):
    def closure(user):
        return execute(job_requirements_query(), **{'user': user})
    return closure
