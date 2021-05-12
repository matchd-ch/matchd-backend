import pytest

from db.models import AttachmentKey, ProfileState


# pylint: disable=R0913
@pytest.mark.django_db
def test_incomplete_attachments(login, user_student, upload, file_image_jpg, attachments_for_user, logout,
                                user_employee, query_attachments_for_slug):
    user_employee.company.state = ProfileState.INCOMPLETE
    user_employee.company.save()
    login(user_employee)
    data, errors = upload(user_employee, AttachmentKey.COMPANY_AVATAR, file_image_jpg)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success')

    attachments = attachments_for_user(user_employee, AttachmentKey.COMPANY_AVATAR)
    assert len(attachments) == 1

    logout()
    login(user_student)

    data, errors = query_attachments_for_slug(user_student, user_employee.company.slug)
    assert errors is None
    assert data is not None
    assert len(data.get('companyAvatar')) == 0
    assert len(data.get('companyAvatarFallback')) == 1


@pytest.mark.django_db
def test_anonymous_attachments(login, user_student, upload, file_image_jpg, attachments_for_user, logout, user_employee,
                               query_attachments_for_slug):
    user_employee.company.state = ProfileState.ANONYMOUS
    user_employee.company.save()
    login(user_employee)
    data, errors = upload(user_employee, AttachmentKey.COMPANY_AVATAR, file_image_jpg)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success')

    attachments = attachments_for_user(user_employee, AttachmentKey.COMPANY_AVATAR)
    assert len(attachments) == 1

    logout()
    login(user_student)

    data, errors = query_attachments_for_slug(user_student, user_employee.company.slug)
    assert errors is None
    assert data is not None
    assert len(data.get('companyAvatar')) == 1
    assert len(data.get('companyAvatarFallback')) == 1


@pytest.mark.django_db
def test_public_attachments(login, user_student, upload, file_image_jpg, attachments_for_user, logout, user_employee,
                            query_attachments_for_slug):
    user_employee.company.state = ProfileState.PUBLIC
    user_employee.company.save()
    login(user_employee)
    data, errors = upload(user_employee, AttachmentKey.COMPANY_AVATAR, file_image_jpg)
    assert data is not None
    assert errors is None
    assert data.get('upload') is not None
    assert data.get('upload').get('success')

    attachments = attachments_for_user(user_employee, AttachmentKey.COMPANY_AVATAR)
    assert len(attachments) == 1

    logout()
    login(user_student)

    data, errors = query_attachments_for_slug(user_student, user_employee.company.slug)
    assert errors is None
    assert data is not None
    assert len(data.get('companyAvatar')) == 1
    assert len(data.get('companyAvatarFallback')) == 1
