import pytest

from django.core.exceptions import ValidationError

from db.models import AttachmentKey


@pytest.mark.django_db
def test_student_key(attachment_key_validator, user_student):
    with pytest.raises(ValidationError, match='The key you provided is invalid'):
        attachment_key_validator.validate(AttachmentKey.COMPANY_AVATAR, user_student)

    with pytest.raises(ValidationError, match='The key you provided is invalid'):
        attachment_key_validator.validate(AttachmentKey.COMPANY_DOCUMENTS, user_student)

    try:
        attachment_key_validator.validate(AttachmentKey.STUDENT_AVATAR, user_student)
        attachment_key_validator.validate(AttachmentKey.STUDENT_DOCUMENTS, user_student)
    except ValidationError:
        pytest.fail('attachment key validator test failed')


@pytest.mark.django_db
def test_company_key(attachment_key_validator, user_employee):
    with pytest.raises(ValidationError, match='The key you provided is invalid'):
        attachment_key_validator.validate(AttachmentKey.STUDENT_AVATAR, user_employee)

    with pytest.raises(ValidationError, match='The key you provided is invalid'):
        attachment_key_validator.validate(AttachmentKey.STUDENT_DOCUMENTS, user_employee)

    try:
        attachment_key_validator.validate(AttachmentKey.COMPANY_AVATAR, user_employee)
        attachment_key_validator.validate(AttachmentKey.COMPANY_DOCUMENTS, user_employee)
    except ValidationError:
        pytest.fail('attachment key validator test failed')
