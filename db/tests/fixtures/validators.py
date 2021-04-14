import pytest

from db.validators import PasswordValidator, AttachmentKeyValidator


@pytest.fixture
def password_validator():
    return PasswordValidator()


@pytest.fixture
def attachment_key_validator():
    return AttachmentKeyValidator()
