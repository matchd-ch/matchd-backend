import pytest

from django.contrib.auth import get_user_model

from db.models.profile_type import ProfileType


@pytest.fixture
def user_valid_args(create_university):
    return {
        'type': ProfileType.INTERNAL,
        'first_name': 'John',
        'last_name': 'Doe',
        'company': create_university
    }


@pytest.fixture
def create_user(create_university):
    company = create_university
    return get_user_model().objects.create(username='test',
                                           email='test@email.com',
                                           type=ProfileType.STUDENT,
                                           company=company)
