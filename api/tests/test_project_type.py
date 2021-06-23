import pytest
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_query(query_project_types, project_type_objects):
    data, errors = query_project_types(AnonymousUser())
    assert errors is None
    assert data is not None

    objects = data.get('projectTypes')
    assert objects is not None
    assert len(objects) == len(project_type_objects)
    assert objects[0].get('name') == 'Project Type 1'
    assert objects[1].get('name') == 'Project Type 2'
