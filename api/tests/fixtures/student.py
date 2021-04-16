import pytest

from db.models import Student, ProfileType


@pytest.fixture
def user_student(get_user, default_password):
    username = 'student@matchd.test'
    user = get_user(username, default_password, True, ProfileType.STUDENT)
    Student.objects.create(user=user)
    return user


@pytest.fixture
def user_student_2(get_user, default_password):
    username = 'student2@matchd.test'
    user = get_user(username, default_password, True, ProfileType.STUDENT)
    Student.objects.create(user=user)
    return user


@pytest.fixture
def user_student_not_verified(get_user, default_password):
    username = 'student@matchd.test'
    user = get_user(username, default_password, False, ProfileType.STUDENT)
    Student.objects.create(user=user)
    return user
