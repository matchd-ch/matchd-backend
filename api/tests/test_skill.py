import pytest
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_query(query_skills, skill_objects):
    data, errors = query_skills(AnonymousUser())
    assert errors is None
    assert data is not None

    objects = data.get('skills')
    assert objects is not None
    assert len(objects) == len(skill_objects)
    assert 'css' == objects[0].get('name')
    assert 'java' == objects[1].get('name')
    assert 'php' == objects[2].get('name')
