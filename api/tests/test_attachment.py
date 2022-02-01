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
def test_node_query(query_attachment_node, login, upload, file_image_jpg, user_employee):
    login(user_employee)
    data, errors = upload(user_employee, AttachmentKey.COMPANY_AVATAR, file_image_jpg)
    assert data is not None
    assert data.get('upload').get('success')

    data, errors = query_attachment_node(user_employee, 10)

    assert errors is None
    assert data is not None

    node = data.get('node')
    assert node is not None
