import pytest

from db.models import Keyword


def keywords_query():
    return '''
    query {
        keywords {
            id
            name
        }
    }
    '''


@pytest.fixture
def keyword_objects():
    return [
        Keyword.objects.create(name="Keyword 2"),
        Keyword.objects.create(name="Keyword 1")
    ]


@pytest.fixture
def query_keywords(execute):
    def closure(user):
        return execute(keywords_query(), **{'user': user})
    return closure
