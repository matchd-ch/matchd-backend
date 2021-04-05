import pytest
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_query(query_language_levels, language_level_objects):
    data, errors = query_language_levels(AnonymousUser())
    assert errors is None
    assert data is not None

    objects = data.get('languageLevels')
    assert objects is not None
    assert len(objects) == len(language_level_objects)
    assert 'A1' == objects[0].get('level')
    assert 'A2' == objects[1].get('level')
    assert 'B1' == objects[2].get('level')
