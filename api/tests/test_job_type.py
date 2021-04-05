import pytest
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_query(query_job_types, job_type_objects):
    data, errors = query_job_types(AnonymousUser())
    assert errors is None
    assert data is not None

    objects = data.get('jobTypes')
    assert objects is not None
    assert len(objects) == len(job_type_objects)
    assert objects[0].get('name') == 'Lehrstelle'
    assert objects[1].get('name') == 'Praktikum'
