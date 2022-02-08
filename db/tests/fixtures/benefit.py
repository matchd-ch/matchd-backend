import pytest


@pytest.fixture
def benefit_valid_args():
    return {
        'name': 'luck',
        'icon': 'heart',
    }
