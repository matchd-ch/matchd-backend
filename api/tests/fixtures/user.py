import pytest

from django.contrib.auth import get_user_model


@pytest.fixture
def get_user():
    def closure(username, password, verified, user_type, company=None):
        # pylint: disable=W0612
        user, created = get_user_model().objects.get_or_create(
            username=username,
            email=username,
            type=user_type,
            company=company
        )
        user.set_password(password)
        user.save()
        user.status.verified = verified
        user.status.save()
        return user
    return closure
