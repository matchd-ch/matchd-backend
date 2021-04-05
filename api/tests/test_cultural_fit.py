import pytest
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_query(query_cultural_fits, cultural_fit_objects):
    data, errors = query_cultural_fits(AnonymousUser())
    assert errors is None
    assert data is not None

    objects = data.get('culturalFits')
    assert objects is not None
    assert len(objects) == len(cultural_fit_objects)
    assert 'I like working' == objects[0].get('student')
    assert 'You like working' == objects[0].get('company')
    assert 'I like things' == objects[1].get('student')
    assert 'You like things' == objects[1].get('company')
