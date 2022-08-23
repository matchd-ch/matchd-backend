import pytest

from db.models import AttachmentKey

# pylint: disable=R0913


@pytest.mark.django_db
def test_upload_student_challenge_image(login, user_student, upload_for_challenge, file_image_jpg,
                                        attachments_for_challenge, student_challenge_object):
    login(user_student)
    data, errors = upload_for_challenge(user_student, student_challenge_object,
                                        AttachmentKey.CHALLENGE_IMAGES, file_image_jpg)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success')

    attachments = attachments_for_challenge(student_challenge_object,
                                            AttachmentKey.CHALLENGE_IMAGES)
    assert len(attachments) == 1


@pytest.mark.django_db
def test_upload_student_challenge_image_wrong_type(login, user_student, upload_for_challenge,
                                                   file_document_pdf, attachments_for_challenge,
                                                   student_challenge_object):
    login(user_student)
    data, errors = upload_for_challenge(user_student, student_challenge_object,
                                        AttachmentKey.CHALLENGE_IMAGES, file_document_pdf)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success') is False

    errors = data.get('upload').get('errors')
    assert errors is not None
    assert 'file' in errors

    attachments = attachments_for_challenge(student_challenge_object,
                                            AttachmentKey.CHALLENGE_IMAGES)
    assert len(attachments) == 0


@pytest.mark.django_db
def test_upload_student_challenge_document(login, user_student, upload_for_challenge,
                                           file_document_pdf, attachments_for_challenge,
                                           student_challenge_object):
    login(user_student)
    data, errors = upload_for_challenge(user_student, student_challenge_object,
                                        AttachmentKey.CHALLENGE_DOCUMENTS, file_document_pdf)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success')

    attachments = attachments_for_challenge(student_challenge_object,
                                            AttachmentKey.CHALLENGE_DOCUMENTS)
    assert len(attachments) == 1


@pytest.mark.django_db
def test_upload_student_challenge_document_wrong_type(login, user_student, upload_for_challenge,
                                                      file_image_jpg, attachments_for_challenge,
                                                      student_challenge_object):
    login(user_student)
    data, errors = upload_for_challenge(user_student, student_challenge_object,
                                        AttachmentKey.CHALLENGE_DOCUMENTS, file_image_jpg)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success') is False

    errors = data.get('upload').get('errors')
    assert errors is not None
    assert 'file' in errors

    attachments = attachments_for_challenge(student_challenge_object,
                                            AttachmentKey.CHALLENGE_DOCUMENTS)
    assert len(attachments) == 0


@pytest.mark.django_db
def test_upload_challenge_student_not_owner(login, user_student, upload_for_challenge,
                                            file_image_jpg, attachments_for_challenge,
                                            company_challenge_object):
    login(user_student)
    data, errors = upload_for_challenge(user_student, company_challenge_object,
                                        AttachmentKey.CHALLENGE_IMAGES, file_image_jpg)
    assert data is not None
    assert errors is not None
    assert data.get('upload') is None

    attachments = attachments_for_challenge(company_challenge_object,
                                            AttachmentKey.CHALLENGE_IMAGES)
    assert len(attachments) == 0


@pytest.mark.django_db
def test_upload_challenge_employee_not_owner(login, user_employee, upload_for_challenge,
                                             file_image_jpg, attachments_for_challenge,
                                             student_challenge_object):
    login(user_employee)
    data, errors = upload_for_challenge(user_employee, student_challenge_object,
                                        AttachmentKey.CHALLENGE_IMAGES, file_image_jpg)
    assert data is not None
    assert errors is not None
    assert data.get('upload') is None

    attachments = attachments_for_challenge(student_challenge_object,
                                            AttachmentKey.CHALLENGE_IMAGES)
    assert len(attachments) == 0
