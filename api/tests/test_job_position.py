import pytest
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_query(query_job_positions, job_position_objects):
    data, errors = query_job_positions(AnonymousUser())
    assert errors is None
    assert data is not None

    objects = data.get('jobPositions')
    assert objects is not None
    assert len(objects) == len(job_position_objects)
    assert objects[0].get('name') == 'Applikationsentwickler*in'
    assert objects[1].get('name') == 'Systemtechniker*in'
