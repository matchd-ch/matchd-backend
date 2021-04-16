import pytest
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_query(query_languages, language_objects):
    data, errors = query_languages(AnonymousUser())
    assert errors is None
    assert data is not None

    objects = data.get('languages')
    assert objects is not None
    assert len(objects) == len(language_objects)
    assert objects[0].get('name') == 'Deutsch'
    assert objects[1].get('name') == 'Englisch'
    assert objects[2].get('name') == 'Spanisch'
    assert objects[3].get('name') == 'Zulu'


@pytest.mark.django_db
def test_shortlist_query(query_languages_shortlist, language_shortlist_objects):
    data, errors = query_languages_shortlist(AnonymousUser())
    assert errors is None
    assert data is not None

    objects = data.get('languages')
    assert objects is not None
    assert len(objects) == len(language_shortlist_objects)
    assert objects[0].get('name') == 'Deutsch'
    assert objects[1].get('name') == 'Spanisch'
