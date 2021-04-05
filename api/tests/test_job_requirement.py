import pytest
from django.contrib.auth.models import AnonymousUser


@pytest.mark.django_db
def test_query(query_job_requirements, job_requirement_objects):
    data, errors = query_job_requirements(AnonymousUser())
    assert errors is None
    assert data is not None

    objects = data.get('jobRequirements')
    assert objects is not None
    assert len(objects) == len(job_requirement_objects)
    assert objects[0].get('name') == 'abgeschlossene Volksschule'
    assert objects[1].get('name') == 'Berufsmaturität (BMS)'
