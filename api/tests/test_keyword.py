import pytest
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_query(query_keywords, keyword_objects):
    data, errors = query_keywords(AnonymousUser())
    assert errors is None
    assert data is not None

    print(data)
    print(errors)

    objects = data.get('keywords')
    assert objects is not None
    assert len(objects) == len(keyword_objects)
    assert objects[0].get('name') == 'Keyword 1'
    assert objects[1].get('name') == 'Keyword 2'
