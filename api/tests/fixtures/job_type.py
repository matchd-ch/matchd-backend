import pytest

from graphql_relay import to_global_id

from db.models import JobType, DateMode

# pylint: disable=W0621


def job_type_node_query():
    return '''
    query ($id: ID!) {
        node(id: $id) {
            id
            ... on JobType {
                name
            }
        }
    }
    '''


def job_types_query():
    return '''
    query {
        jobTypes(first: 4) {
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
def job_type_objects():
    return [
        JobType.objects.create(id=1, name="Praktikum", mode=DateMode.DATE_FROM),
        JobType.objects.create(id=2, name="Lehrstelle", mode=DateMode.DATE_RANGE),
        JobType.objects.create(id=3, name="Lehrstelle 2", mode=DateMode.DATE_RANGE),
        JobType.objects.create(id=4, name="Praktikum 2", mode=DateMode.DATE_FROM)
    ]


@pytest.fixture
def query_job_type_node(execute):

    def closure(user, id_value):
        return execute(job_type_node_query(),
                       variables={'id': to_global_id('JobType', id_value)},
                       **{'user': user})

    return closure


@pytest.fixture
def query_job_types(execute):

    def closure(user):
        return execute(job_types_query(), **{'user': user})

    return closure


@pytest.fixture
def job_type_objects_date_from(job_type_objects):
    objects = []
    for obj in job_type_objects:
        if obj.mode == DateMode.DATE_FROM:
            objects.append(obj)
    return objects


@pytest.fixture
def job_type_objects_date_range(job_type_objects):
    objects = []
    for obj in job_type_objects:
        if obj.mode == DateMode.DATE_RANGE:
            objects.append(obj)
    return objects
