import pytest

from db.models.keyword import Keyword


@pytest.fixture
def keyword_valid_args():
    return {'name': 'one'}


@pytest.fixture
def create_keyword():
    return Keyword.objects.create(name='fantastic')
