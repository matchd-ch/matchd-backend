import pytest
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_query(query_benefits, benefit_objects):
    data, errors = query_benefits(AnonymousUser())
    assert errors is None
    assert data is not None

    objects = data.get('benefits')
    assert objects is not None
    assert len(objects) == len(benefit_objects)
    assert objects[0].get('name') == 'Laptop'
    assert objects[1].get('name') == 'Massage'
