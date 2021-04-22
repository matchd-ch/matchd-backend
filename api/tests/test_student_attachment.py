import pytest

from db.models import AttachmentKey, ProfileState, Match


# pylint: disable=R0913


@pytest.mark.django_db
def test_incomplete_attachments(login, user_student, upload, file_image_jpg, attachments_for_user, logout,
                                user_employee, query_attachments_for_slug):
    user_student.student.state = ProfileState.INCOMPLETE
    user_student.student.save()
    login(user_student)
    data, errors = upload(user_student, AttachmentKey.STUDENT_AVATAR, file_image_jpg)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success')

    attachments = attachments_for_user(user_student, AttachmentKey.STUDENT_AVATAR)
    assert len(attachments) == 1

    data, errors = query_attachments_for_slug(user_student, user_student.student.slug)
    assert errors is None
    assert data is not None
    assert len(data.get('studentAvatar')) == 1

    logout()
    login(user_employee)

    data, errors = query_attachments_for_slug(user_employee, user_student.student.slug)
    assert errors is None
    assert data is not None
    assert len(data.get('studentAvatar')) == 0


@pytest.mark.django_db
def test_anonymous_attachments(login, user_student, upload, file_image_jpg, attachments_for_user, logout, user_employee,
                               query_attachments_for_slug):
    user_student.student.state = ProfileState.ANONYMOUS
    user_student.student.save()
    login(user_student)
    data, errors = upload(user_student, AttachmentKey.STUDENT_AVATAR, file_image_jpg)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success')

    attachments = attachments_for_user(user_student, AttachmentKey.STUDENT_AVATAR)
    assert len(attachments) == 1

    data, errors = query_attachments_for_slug(user_student, user_student.student.slug)
    assert errors is None
    assert data is not None
    assert len(data.get('studentAvatar')) == 1

    logout()
    login(user_employee)

    data, errors = query_attachments_for_slug(user_employee, user_student.student.slug)
    assert errors is None
    assert data is not None
    assert len(data.get('studentAvatar')) == 0


@pytest.mark.django_db
def test_public_attachments(login, user_student, upload, file_image_jpg, attachments_for_user, logout, user_employee,
                            query_attachments_for_slug):
    user_student.student.state = ProfileState.PUBLIC
    user_student.student.save()
    login(user_student)
    data, errors = upload(user_student, AttachmentKey.STUDENT_AVATAR, file_image_jpg)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success')

    attachments = attachments_for_user(user_student, AttachmentKey.STUDENT_AVATAR)
    assert len(attachments) == 1

    data, errors = query_attachments_for_slug(user_student, user_student.student.slug)
    assert errors is None
    assert data is not None
    assert len(data.get('studentAvatar')) == 1

    logout()
    login(user_employee)

    data, errors = query_attachments_for_slug(user_employee, user_student.student.slug)
    assert errors is None
    assert data is not None
    assert len(data.get('studentAvatar')) == 1


@pytest.mark.django_db
def test_protected_attachments(login, user_student, upload, file_document_pdf, attachments_for_user, logout,
                                user_employee, query_attachments_for_slug, job_posting_object):
    user_student.student.state = ProfileState.PUBLIC
    user_student.student.save()
    login(user_student)
    data, errors = upload(user_student, AttachmentKey.STUDENT_DOCUMENTS, file_document_pdf)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success')

    attachments = attachments_for_user(user_student, AttachmentKey.STUDENT_DOCUMENTS)
    assert len(attachments) == 1

    data, errors = query_attachments_for_slug(user_student, user_student.student.slug)
    assert errors is None
    assert data is not None
    assert len(data.get('studentDocuments')) == 1

    logout()
    login(user_employee)

    data, errors = query_attachments_for_slug(user_employee, user_student.student.slug)
    assert errors is None
    assert data is not None
    assert len(data.get('studentDocuments')) == 0

    job_posting_object.employee = user_employee.employee
    job_posting_object.company = user_employee.company
    job_posting_object.save()

    match_obj = Match.objects.create(student=user_student.student, job_posting=job_posting_object,
                                     company_confirmed=True, initiator=user_employee.type)

    # employee should still have no access to student documents
    data, errors = query_attachments_for_slug(user_employee, user_student.student.slug)
    assert errors is None
    assert data is not None
    assert len(data.get('studentDocuments')) == 0

    match_obj.delete()

    Match.objects.create(student=user_student.student, job_posting=job_posting_object, student_confirmed=True,
                         initiator=user_student.type)

    # employee should have access to student documents
    data, errors = query_attachments_for_slug(user_employee, user_student.student.slug)
    assert errors is None
    assert data is not None
    assert len(data.get('studentDocuments')) == 1
