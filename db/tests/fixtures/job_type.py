import pytest

from db.models.job_type import JobType


@pytest.fixture
def job_type_valid_args():
    return {'name': 'Smart work', 'mode': 'Remote'}


@pytest.fixture
def create_job_type():
    return JobType.objects.create(name='Work and travel', mode='remote')
