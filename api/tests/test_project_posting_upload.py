import pytest

from db.models import AttachmentKey

# pylint: disable=R0913


@pytest.mark.django_db
def test_upload_student_project_posting_image(login, user_student, upload_for_project_posting, file_image_jpg,
                                              attachments_for_project_posting, student_project_posting_object):
    login(user_student)
    data, errors = upload_for_project_posting(user_student, student_project_posting_object,
                                              AttachmentKey.PROJECT_POSTING_IMAGES, file_image_jpg)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success')

    attachments = attachments_for_project_posting(student_project_posting_object, AttachmentKey.PROJECT_POSTING_IMAGES)
    assert len(attachments) == 1


@pytest.mark.django_db
def test_upload_student_project_posting_image_wrong_type(login, user_student, upload_for_project_posting,
                                                         file_document_pdf, attachments_for_project_posting,
                                                         student_project_posting_object):
    login(user_student)
    data, errors = upload_for_project_posting(user_student, student_project_posting_object,
                                              AttachmentKey.PROJECT_POSTING_IMAGES, file_document_pdf)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success') is False

    errors = data.get('upload').get('errors')
    assert errors is not None
    assert 'file' in errors

    attachments = attachments_for_project_posting(student_project_posting_object, AttachmentKey.PROJECT_POSTING_IMAGES)
    assert len(attachments) == 0


@pytest.mark.django_db
def test_upload_student_project_posting_document(login, user_student, upload_for_project_posting, file_document_pdf,
                                                 attachments_for_project_posting, student_project_posting_object):
    login(user_student)
    data, errors = upload_for_project_posting(user_student, student_project_posting_object,
                                              AttachmentKey.PROJECT_POSTING_DOCUMENTS, file_document_pdf)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success')

    attachments = attachments_for_project_posting(student_project_posting_object,
                                                  AttachmentKey.PROJECT_POSTING_DOCUMENTS)
    assert len(attachments) == 1


@pytest.mark.django_db
def test_upload_student_project_posting_document_wrong_type(login, user_student, upload_for_project_posting,
                                                            file_image_jpg, attachments_for_project_posting,
                                                            student_project_posting_object):
    login(user_student)
    data, errors = upload_for_project_posting(user_student, student_project_posting_object,
                                              AttachmentKey.PROJECT_POSTING_DOCUMENTS, file_image_jpg)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success') is False

    errors = data.get('upload').get('errors')
    assert errors is not None
    assert 'file' in errors

    attachments = attachments_for_project_posting(student_project_posting_object,
                                                  AttachmentKey.PROJECT_POSTING_DOCUMENTS)
    assert len(attachments) == 0


@pytest.mark.django_db
def test_upload_project_posting_student_not_owner(login, user_student, upload_for_project_posting, file_image_jpg,
                                                  attachments_for_project_posting, company_project_posting_object):
    login(user_student)
    data, errors = upload_for_project_posting(user_student, company_project_posting_object,
                                              AttachmentKey.PROJECT_POSTING_IMAGES, file_image_jpg)
    assert data is not None
    assert errors is not None
    assert data.get('upload') is None

    attachments = attachments_for_project_posting(company_project_posting_object, AttachmentKey.PROJECT_POSTING_IMAGES)
    assert len(attachments) == 0


@pytest.mark.django_db
def test_upload_project_posting_employee_not_owner(login, user_employee, upload_for_project_posting, file_image_jpg,
                                                   attachments_for_project_posting, student_project_posting_object):
    login(user_employee)
    data, errors = upload_for_project_posting(user_employee, student_project_posting_object,
                                              AttachmentKey.PROJECT_POSTING_IMAGES, file_image_jpg)
    assert data is not None
    assert errors is not None
    assert data.get('upload') is None

    attachments = attachments_for_project_posting(student_project_posting_object, AttachmentKey.PROJECT_POSTING_IMAGES)
    assert len(attachments) == 0
