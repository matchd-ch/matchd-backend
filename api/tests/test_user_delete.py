import pytest

from django.contrib.auth.models import AnonymousUser

from db.models import Company, User


@pytest.mark.django_db
def test_delete_user_student(delete_user, user_student_full_profile):
    data, errors = delete_user(user_student_full_profile)
    assert errors is None
    assert data is not None
    assert data.get('deleteUser').get('success')

    assert not User.objects.filter(pk=user_student_full_profile.id).exists()


@pytest.mark.django_db
def test_delete_user_employee(delete_user, user_employee):
    company = user_employee.company

    data, errors = delete_user(user_employee)
    assert errors is None
    assert data is not None

    assert data.get('deleteUser').get('success')
    assert not User.objects.filter(pk=user_employee.id).exists()
    assert not Company.objects.filter(pk=company.id).exists()


@pytest.mark.django_db
def test_delete_user_anonymous_fails(delete_user):
    data, errors = delete_user(AnonymousUser())
    assert errors is not None
    assert data is not None

    error = errors[0].get('message')
    node = data.get('node')
    assert node is None
    assert error == "You do not have permission to perform this action"
