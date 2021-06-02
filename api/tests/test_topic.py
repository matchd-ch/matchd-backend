import pytest
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_query(query_topics, topic_objects):
    data, errors = query_topics(AnonymousUser())
    assert errors is None
    assert data is not None

    print(data)
    print(errors)

    objects = data.get('topics')
    assert objects is not None
    assert len(objects) == len(topic_objects)
    assert objects[0].get('name') == 'Topic 1'
    assert objects[1].get('name') == 'Topic 2'
