import pytest
from django.contrib.auth import get_user_model

from db.models import User


@pytest.mark.django_db
def test_custom_user_model():
    user_model = get_user_model()
    assert user_model == User
