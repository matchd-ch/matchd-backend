import pytest

from db.models.employee import Employee


@pytest.fixture
def employee_valid_args(create_user):
    return {'user': create_user, 'role': 'Director'}


@pytest.fixture
def create_employee(create_user):
    return Employee.objects.create(user=create_user, role='developer')
