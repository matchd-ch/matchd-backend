import pytest

from db.models import ProjectType


def project_types_query():
    return '''
    query {
        projectTypes {
            id
            name
        }
    }
    '''


@pytest.fixture
def project_type_objects():
    return [
        ProjectType.objects.create(name="Project Type 2"),
        ProjectType.objects.create(name="Project Type 1")
    ]


@pytest.fixture
def query_project_types(execute):
    def closure(user):
        return execute(project_types_query(), **{'user': user})
    return closure
