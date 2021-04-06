import pytest

from db.models import Benefit


def benefits_query():
    return '''
    query {
        benefits {
            id
            name
            icon
        }
    }
    '''


@pytest.fixture
def benefit_objects():
    return [
        Benefit.objects.create(name="Massage", icon='spa'),
        Benefit.objects.create(name="Laptop", icon='laptop')
    ]


@pytest.fixture
def query_benefits(execute):
    def closure(user):
        return execute(benefits_query(), **{'user': user})
    return closure
