import pytest
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_query(query_branches, branch_objects):
    data, errors = query_branches(AnonymousUser())
    assert errors is None
    assert data is not None

    objects = data.get('branches')
    assert objects is not None
    assert len(objects) == len(branch_objects)
    assert objects[0].get('name') == 'Applikationsentwicklung'
    assert objects[1].get('name') == 'Systemtechnik'
