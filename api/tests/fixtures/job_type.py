import pytest

from db.models import JobType, DateMode

# pylint: disable=W0621


def job_types_query():
    return '''
    query {
        jobTypes {
            id
            name
        }
    }
    '''


@pytest.fixture
def job_type_objects():
    return [
        JobType.objects.create(id=1, name="Praktikum", mode=DateMode.DATE_FROM),
        JobType.objects.create(id=2, name="Lehrstelle", mode=DateMode.DATE_RANGE)
    ]


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
