import pytest

from django.contrib.contenttypes.models import ContentType

from db.models.attachment import Attachment


@pytest.mark.django_db
def test_create_attachment(attachment_valid_args):
    attachment = Attachment.objects.create(**attachment_valid_args)

    assert isinstance(attachment, Attachment)


@pytest.mark.django_db
def test_get_attachment(attachment_valid_args):
    attachment = Attachment.objects.create(**attachment_valid_args)
    attachment = Attachment.objects.get(id=attachment.id)

    assert isinstance(attachment, Attachment)
    assert isinstance(attachment.object_id, int)
    assert isinstance(attachment.attachment_id, int)
    assert isinstance(attachment.key, str)
    assert isinstance(attachment.attachment_type, ContentType)
    assert isinstance(attachment.content_type, ContentType)

    assert attachment.object_id == attachment_valid_args.get('object_id')
    assert attachment.attachment_id == attachment_valid_args.get('attachment_id')
    assert attachment.key == attachment_valid_args.get('key')
    assert attachment.attachment_type == attachment_valid_args.get('attachment_type')
    assert attachment.content_type == attachment_valid_args.get('content_type')


@pytest.mark.django_db
def test_update_attachment(attachment_valid_args):
    new_object_id = 9
    attachment = Attachment.objects.create(**attachment_valid_args)
    Attachment.objects.filter(id=attachment.id).update(object_id=new_object_id)
    attachment.refresh_from_db()

    assert isinstance(attachment, Attachment)
    assert isinstance(attachment.object_id, int)

    assert attachment.object_id == new_object_id


@pytest.mark.django_db
def test_delete_attachment(attachment_valid_args):
    attachment = Attachment.objects.create(**attachment_valid_args)
    number_of_deletions, _ = attachment.delete()

    assert number_of_deletions == 1
