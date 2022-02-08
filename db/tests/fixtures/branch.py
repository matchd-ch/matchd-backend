import pytest

from db.models.branch import Branch


@pytest.fixture
def branch_valid_args():
    return {'name': 'smart'}


@pytest.fixture
def create_branch():
    return Branch.objects.create(name='tech')
