import pytest

from db.models import CulturalFit


def cultural_fits_query():
    return '''
    query {
        culturalFits {
            id
            student
            company
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
        CulturalFit.objects.create(id=7, student="I like apples", company='You like apples')
    ]


@pytest.fixture
def query_cultural_fits(execute):
    def closure(user):
        return execute(cultural_fits_query(), **{'user': user})
    return closure
