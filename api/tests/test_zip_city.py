import pytest

from django.contrib.auth.models import AnonymousUser

from db.models import JobPostingState


@pytest.mark.django_db
def test_query(query_zip_city):
    data, errors = query_zip_city(AnonymousUser())
    assert errors is None
    assert data is not None

    objects = data.get('zipCity')
    assert objects is not None


@pytest.mark.django_db
def test_query_jobs(query_zip_city_jobs, job_posting_object, company_object, branch_objects, job_type_objects):

    company_object.zip = '9000'
    company_object.city = 'St. Gallen'
    company_object.save()

    job_posting_object.branches.set([branch_objects[0]])
    job_posting_object.job_type = job_type_objects[0]
    job_posting_object.company = company_object
    job_posting_object.state = JobPostingState.PUBLIC
    job_posting_object.save()

    data, errors = query_zip_city_jobs(AnonymousUser(), branch_objects[0], job_type_objects[0])
    assert errors is None
    assert data is not None

    objects = data.get('zipCityJobs')
    assert objects is not None
    assert len(objects) == 1
