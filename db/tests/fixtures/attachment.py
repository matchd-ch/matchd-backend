import pytest

from django.contrib.contenttypes.models import ContentType

from db.models.attachment import AttachmentKey


@pytest.fixture
def attachment_valid_args():
    return {
        'object_id': 1,
        'attachment_id': 1,
        'key': AttachmentKey.STUDENT_AVATAR,
        'attachment_type': ContentType.objects.get(app_label='db', model='image'),
        'content_type': ContentType.objects.get(app_label='db', model='user'),
    }
