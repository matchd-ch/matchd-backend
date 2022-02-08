import pytest


@pytest.fixture
def user_request_valid_args():
    return {'name': 'Send Money', 'email': 'princeofworld@email.com', 'message': 'sendmoney'}
