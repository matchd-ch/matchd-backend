import pytest

from db.models import Topic


def topics_query():
    return '''
    query {
        topics {
            id
            name
        }
    }
    '''


@pytest.fixture
def topic_objects():
    return [
        Topic.objects.create(name="Topic 2"),
        Topic.objects.create(name="Topic 1")
    ]


@pytest.fixture
def query_topics(execute):
    def closure(user):
        return execute(topics_query(), **{'user': user})
    return closure
