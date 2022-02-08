import pytest

from db.models.topic import Topic


@pytest.fixture
def topic_valid_args():
    return {'name': 'elixir'}


@pytest.fixture
def create_topic():
    return Topic.objects.create(name='phoenix')
