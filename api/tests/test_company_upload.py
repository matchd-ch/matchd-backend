import pytest
from django.contrib.auth.models import AnonymousUser

from db.models import AttachmentKey


@pytest.mark.django_db
def test_upload_company_image(login, user_employee, upload, file_image_jpg, attachments_for_user):
    login(user_employee)
    data, errors = upload(user_employee, AttachmentKey.COMPANY_AVATAR, file_image_jpg)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success')

    attachments = attachments_for_user(user_employee, AttachmentKey.COMPANY_AVATAR)
    assert len(attachments) == 1


@pytest.mark.django_db
def test_upload_company_document(login, user_employee, upload, file_document_pdf, attachments_for_user):
    login(user_employee)
    data, errors = upload(user_employee, AttachmentKey.COMPANY_DOCUMENTS, file_document_pdf)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success') is False

    errors = data.get('upload').get('errors')
    assert errors is not None
    assert 'file' in errors

    attachments = attachments_for_user(user_employee, AttachmentKey.COMPANY_DOCUMENTS)
    assert len(attachments) == 0


@pytest.mark.django_db
def test_upload_company_video(login, user_employee, upload, file_video_mp4, attachments_for_user):
    login(user_employee)
    data, errors = upload(user_employee, AttachmentKey.COMPANY_DOCUMENTS, file_video_mp4)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success')

    attachments = attachments_for_user(user_employee, AttachmentKey.COMPANY_DOCUMENTS)
    assert len(attachments) == 1


@pytest.mark.django_db
def test_upload_company_without_login(upload, file_image_jpg):
    data, errors = upload(AnonymousUser(), AttachmentKey.COMPANY_AVATAR, file_image_jpg)
    assert data is not None
    assert errors is not None
    assert data.get('upload') is None


@pytest.mark.django_db
def test_upload_student_avatar_as_company(login, user_employee, upload, file_image_jpg, attachments_for_user):
    login(user_employee)
    data, errors = upload(user_employee, AttachmentKey.STUDENT_AVATAR, file_image_jpg)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success') is False

    errors = data.get('upload').get('errors')
    assert errors is not None
    assert 'key' in errors

    attachments = attachments_for_user(user_employee, AttachmentKey.STUDENT_AVATAR)
    assert len(attachments) == 0


@pytest.mark.django_db
def test_upload_too_many_uploads(login, user_employee, upload, file_image_jpg, attachments_for_user):
    login(user_employee)
    upload(user_employee, AttachmentKey.COMPANY_AVATAR, file_image_jpg)
    data, errors = upload(user_employee, AttachmentKey.COMPANY_AVATAR, file_image_jpg)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success') is False

    errors = data.get('upload').get('errors')
    assert errors is not None
    assert 'key' in errors

    attachments = attachments_for_user(user_employee, AttachmentKey.COMPANY_AVATAR)
    assert len(attachments) == 1
