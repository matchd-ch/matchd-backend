import pytest

from db.models import JobPosition


def job_positions_query():
    return '''
    query {
        jobPositions {
            id
            name
        }
    }
    '''


@pytest.fixture
def job_position_objects():
    return [
        JobPosition.objects.create(name="Systemtechniker*in"),
        JobPosition.objects.create(name="Applikationsentwickler*in")
    ]


@pytest.fixture
def query_job_positions(execute):
    def closure(user):
        return execute(job_positions_query(), **{'user': user})
    return closure
