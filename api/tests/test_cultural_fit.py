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
    assert objects[0].get('student') == 'I like working'
    assert objects[0].get('company') == 'You like working'
    assert objects[1].get('student') == 'I like things'
    assert objects[1].get('company') == 'You like things'
