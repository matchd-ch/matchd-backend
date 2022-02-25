import pytest

from django.contrib.auth.models import AnonymousUser
from django.test import Client

from db.models import ProfileType

# pylint: disable=W0621


@pytest.fixture
def export_csv(default_password):

    def closure(user):
        client = Client()
        client.login(username=user.username, password=default_password)
        response = client.get('/admin/users/export')

        return response

    return closure


@pytest.mark.django_db
def test_export_users_csv(get_user, export_csv, default_password, create_user):
    user = get_user('internal-1@matchd.test', default_password, True, ProfileType.INTERNAL, None)
    response = export_csv(user)
    content = list(response.streaming_content)

    assert response.status_code == 200
    assert len(content) > 2    # First row metadata, second table header, third data row


@pytest.mark.django_db
def test_unauthorised_export_users_csv(export_csv):
    user = AnonymousUser()
    response = export_csv(user)

    assert response.status_code == 302
