import pytest

from django.contrib.auth.models import AnonymousUser

from db.models import AttachmentKey


@pytest.mark.django_db
def test_upload_student_image(login, user_student, upload, file_image_jpg, attachments_for_user):
    login(user_student)
    data, errors = upload(user_student, AttachmentKey.STUDENT_AVATAR, file_image_jpg)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success')

    attachments = attachments_for_user(user_student, AttachmentKey.STUDENT_AVATAR)
    assert len(attachments) == 1


@pytest.mark.django_db
def test_upload_student_document(login, user_student, upload, file_document_pdf,
                                 attachments_for_user):
    login(user_student)
    data, errors = upload(user_student, AttachmentKey.STUDENT_DOCUMENTS, file_document_pdf)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success')

    attachments = attachments_for_user(user_student, AttachmentKey.STUDENT_DOCUMENTS)
    assert len(attachments) == 1


@pytest.mark.django_db
def test_upload_student_video(login, user_student, upload, file_video_mp4, attachments_for_user):
    login(user_student)
    data, errors = upload(user_student, AttachmentKey.STUDENT_DOCUMENTS, file_video_mp4)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success') is False

    errors = data.get('upload').get('errors')
    assert errors is not None
    assert 'file' in errors

    attachments = attachments_for_user(user_student, AttachmentKey.STUDENT_DOCUMENTS)
    assert len(attachments) == 0


@pytest.mark.django_db
def test_upload_without_login(upload, file_image_jpg):
    data, errors = upload(AnonymousUser(), AttachmentKey.STUDENT_AVATAR, file_image_jpg)
    assert data is not None
    assert errors is not None
    assert data.get('upload') is None


@pytest.mark.django_db
def test_upload_company_avatar_as_student(login, user_student, upload, file_image_jpg,
                                          attachments_for_user):
    login(user_student)
    data, errors = upload(user_student, AttachmentKey.COMPANY_AVATAR, file_image_jpg)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success') is False

    errors = data.get('upload').get('errors')
    assert errors is not None
    assert 'key' in errors

    attachments = attachments_for_user(user_student, AttachmentKey.COMPANY_AVATAR)
    assert len(attachments) == 0


@pytest.mark.django_db
def test_upload_too_many_uploads(login, user_student, upload, file_image_jpg, attachments_for_user):
    login(user_student)
    upload(user_student, AttachmentKey.STUDENT_AVATAR, file_image_jpg)
    data, errors = upload(user_student, AttachmentKey.STUDENT_AVATAR, file_image_jpg)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success') is False

    errors = data.get('upload').get('errors')
    assert errors is not None
    assert 'key' in errors

    attachments = attachments_for_user(user_student, AttachmentKey.STUDENT_AVATAR)
    assert len(attachments) == 1
