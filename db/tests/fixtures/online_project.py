import pytest


@pytest.fixture
def online_project_valid_args(create_student):
    return {'url': 'www.project.ch', 'student': create_student}
