import pytest

from db.models import ProfileState, AttachmentKey


@pytest.mark.django_db
def test_delete_attachment(login, delete_attachment, upload, file_image_jpg, attachments_for_user, user_employee):
    user_employee.company.state = ProfileState.INCOMPLETE
    user_employee.company.save()
    login(user_employee)
    data, errors = upload(user_employee, AttachmentKey.COMPANY_AVATAR, file_image_jpg)
    assert data is not None

    attachments = attachments_for_user(user_employee, AttachmentKey.COMPANY_AVATAR)
    assert len(attachments) == 1

    attachment_id = attachments[0].id
    data, errors = delete_attachment(user_employee, attachment_id)
    assert errors is None
    assert data is not None
    assert data.get('deleteAttachment').get('success') is True
    assert data.get('deleteAttachment').get('errors') is None


@pytest.mark.django_db
def test_delete_attachment_with_another_user(login, delete_attachment, upload, file_image_jpg, attachments_for_user,
                                             user_employee, user_student):
    user_employee.company.state = ProfileState.INCOMPLETE
    user_employee.company.save()
    login(user_employee)
    data, errors = upload(user_employee, AttachmentKey.COMPANY_AVATAR, file_image_jpg)
    assert data is not None

    attachments = attachments_for_user(user_employee, AttachmentKey.COMPANY_AVATAR)
    assert len(attachments) == 1

    attachment_id = attachments[0].id
    login(user_student)
    data, errors = delete_attachment(user_student, attachment_id)
    assert errors is None
    assert data is not None
    assert data.get('deleteAttachment').get('success') is False
    assert data.get('deleteAttachment').get('errors') is not None
