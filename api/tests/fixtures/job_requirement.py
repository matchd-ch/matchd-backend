import pytest

from db.models import JobRequirement


def job_requirements_query():
    return '''
    query {
        jobRequirements {
            id
            name
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
def query_job_requirements(execute):
    def closure(user):
        return execute(job_requirements_query(), **{'user': user})
    return closure
