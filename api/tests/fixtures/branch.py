import pytest

from db.models import Branch


def branches_query():
    return '''
    query {
        branches {
            id
            name
        }
    }
    '''


@pytest.fixture
def branch_objects():
    return [
        Branch.objects.create(name="Systemtechnik", ),
        Branch.objects.create(name="Applikationsentwicklung", )
    ]


@pytest.fixture
def query_branches(execute):
    def closure(user):
        return execute(branches_query(), **{'user': user})
    return closure
