import pytest

from db.models import AttachmentKey, ProfileState

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
