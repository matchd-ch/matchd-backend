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
    assert objects[0].get('level') == 'A1'
    assert objects[1].get('level') == 'A2'
    assert objects[2].get('level') == 'B1'
