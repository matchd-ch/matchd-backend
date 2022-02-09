import pytest

from db.models.language import Language


@pytest.fixture
def language_valid_args():
    return {'name': 'German'}


@pytest.fixture
def create_language():

    def closure(name):
        return Language.objects.create(name=name)

    return closure
