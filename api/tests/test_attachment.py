import pytest

from db.models import AttachmentKey


@pytest.mark.django_db
def test_query(query_attachments, login, upload, file_image_jpg, user_employee):
    login(user_employee)
    data, errors = upload(user_employee, AttachmentKey.COMPANY_AVATAR, file_image_jpg)
    assert data is not None
    assert data.get('upload').get('success')

    data, errors = query_attachments(user_employee, 'COMPANY_AVATAR')
    assert errors is None
    assert data is not None

    edges = data.get('attachments').get('edges')
    assert edges is not None
    assert len(edges) == 1


@pytest.mark.django_db
def test_node_query(query_attachment_node_by_node_id, login, upload, file_image_jpg, user_employee):
    login(user_employee)
    data, errors = upload(user_employee, AttachmentKey.COMPANY_AVATAR, file_image_jpg)
    assert data is not None
    assert data.get('upload').get('success')

    attachment = data.get('upload').get('attachment')
    assert attachment is not None

    data, errors = query_attachment_node_by_node_id(user_employee, attachment.get('id'))

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
