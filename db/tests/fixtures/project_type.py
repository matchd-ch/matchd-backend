import pytest

from db.models.project_type import ProjectType


@pytest.fixture
def project_type_valid_args():
    return {'name': 'Smart'}


@pytest.fixture
def create_project_type():
    return ProjectType.objects.create(name='Interesting')
