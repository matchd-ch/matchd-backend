import pytest

from graphql_relay import to_global_id

from db.models import CulturalFit


def cultural_fit_node_query():
    return '''
    query ($id: ID!) {
        node(id: $id) {
            id
            ... on CulturalFit {
                company
                student
            }
        }
    }
    '''


def cultural_fits_query():
    return '''
    query {
        culturalFits(first: 12) {
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
                    company
                    student
                }
            }
        }
    }
    '''


@pytest.fixture
def cultural_fit_objects():
    return [
        CulturalFit.objects.create(id=1, student="I like working", company='You like working'),
        CulturalFit.objects.create(id=2, student="I like things", company='You like things'),
        CulturalFit.objects.create(id=3, student="I like stuff", company='You like stuff'),
        CulturalFit.objects.create(id=4, student="I like beer", company='You like beer'),
        CulturalFit.objects.create(id=5, student="I like honey", company='You like honey'),
        CulturalFit.objects.create(id=6, student="I like flowers", company='You like flowers'),
        CulturalFit.objects.create(id=7, student="I like apples", company='You like apples'),
        CulturalFit.objects.create(id=8, student="I like bushes", company='You like bushes'),
        CulturalFit.objects.create(id=9, student="I like ants", company='You like ants'),
        CulturalFit.objects.create(id=10, student="I like lions", company='You like lions'),
        CulturalFit.objects.create(id=11,
                                   student="I like everything",
                                   company='You like everything'),
        CulturalFit.objects.create(id=12, student="I like nothing", company='You like nothing')
    ]


@pytest.fixture
def query_cultural_fit_node(execute):

    def closure(user, id_value):
        return execute(cultural_fit_node_query(),
                       variables={'id': to_global_id('CulturalFit', id_value)},
                       **{'user': user})

    return closure


@pytest.fixture
def query_cultural_fits(execute):

    def closure(user):
        return execute(cultural_fits_query(), **{'user': user})

    return closure
